import threading
import time
from wakeonlan import send_magic_packet
from ws4py.client.threadedclient import WebSocketClient
from src.LGTV.auth import LGTVAuth
from src.LGTV.remote import LGTVRemote

def _noop(res):
    pass

class PointerSocketClient(WebSocketClient):
    """WebSocket client connected to WebOS NetInput Pointer Socket for real-time key events."""
    def __init__(self, url):
        super().__init__(url, exclude_headers=["Origin"])
        self.is_ready = False

    def opened(self):
        self.is_ready = True

    def closed(self, code, reason=None):
        self.is_ready = False


class LGWebOSClient:
    """LG WebOS TV client managing SSAP services and NetInput Pointer Socket."""

    def __init__(self, config_manager, status_callback=None):
        self.config_manager = config_manager
        self.status_callback = status_callback
        self.remote = None
        self.pointer_socket = None
        self.connected = False
        self.is_muted = False
        self._lock = threading.Lock()

    def update_status(self, message: str, is_connected: bool = False):
        self.connected = is_connected
        if self.status_callback:
            self.status_callback(message, is_connected)

    def _on_pointer_socket_ready(self, res):
        with self._lock:
            if res and isinstance(res, dict) and "payload" in res:
                socket_path = res["payload"].get("socketPath")
                if socket_path:
                    try:
                        self.pointer_socket = PointerSocketClient(socket_path)
                        self.pointer_socket.connect()
                    except Exception as e:
                        print(f"Error opening pointer socket: {e}")
                        self.pointer_socket = None

    def get_remote(self):
        with self._lock:
            tv_ip = self.config_manager.get("tv_ip", "192.168.1.154")
            key = self.config_manager.get("client_key", "")
            mac = self.config_manager.get("tv_mac", "F8:B9:5A:A6:14:50")

            if not tv_ip or not key:
                return None

            if not self.remote:
                try:
                    self.remote = LGTVRemote(name="LG_Remote_PC", ip=tv_ip, mac=mac, key=key, ssl=True)
                    self.remote.connect()
                    self.connected = True
                    # Request pointer input socket for arrow keys, back, enter
                    threading.Thread(target=self._init_pointer_socket, daemon=True).start()
                except Exception as e:
                    print(f"Error creating LGTVRemote: {e}")
                    self.remote = None
                    self.connected = False
            return self.remote

    def _init_pointer_socket(self):
        time.sleep(1)
        with self._lock:
            if self.remote:
                try:
                    self.remote.getCursorSocket(callback=self._on_pointer_socket_ready)
                except Exception as e:
                    print(f"Error requesting cursor socket: {e}")

    def send_pointer_key(self, key_name: str):
        """Send key to the TV via the Pointer Input Socket."""
        with self._lock:
            sock = self.pointer_socket

        if sock and sock.is_ready:
            try:
                sock.send(f"type:button\nname:{key_name}\n\n")
                return True
            except Exception as e:
                print(f"Pointer socket send error: {e}")

        # If not ready, attempt reconnect
        self._init_pointer_socket()
        time.sleep(0.5)
        with self._lock:
            sock = self.pointer_socket
        if sock and sock.is_ready:
            try:
                sock.send(f"type:button\nname:{key_name}\n\n")
                return True
            except Exception as e:
                print(f"Pointer retry send error: {e}")
        return False

    def connect_async(self, on_finish=None):
        """Connect or pair to TV in a background thread."""
        thread = threading.Thread(target=self._connect_thread, args=(on_finish,), daemon=True)
        thread.start()

    def _connect_thread(self, on_finish=None):
        tv_ip = self.config_manager.get("tv_ip", "192.168.1.154")
        key = self.config_manager.get("client_key", "")
        
        if not tv_ip:
            self.update_status("No TV IP configured", False)
            if on_finish: on_finish(False, "No TV IP configured")
            return

        self.update_status(f"Connecting to {tv_ip}...", False)

        if not key:
            try:
                auth = LGTVAuth("LG_Remote_PC", tv_ip, ssl=True)
                auth.connect()
                for _ in range(15):
                    time.sleep(1)
                    k = auth.serialise().get("key")
                    if k:
                        self.config_manager.set("client_key", k)
                        key = k
                        self.update_status("Pairing successful!", True)
                        break
            except Exception as e:
                print(f"Auth error: {e}")

        if key:
            try:
                r = self.get_remote()
                if r:
                    self.update_status("Connected to LG WebOS TV", True)
                    if on_finish: on_finish(True, "Connected")
                    return
            except Exception as e:
                print(f"Remote connect error: {e}")

        self.update_status("Connection failed", False)
        if on_finish: on_finish(False, "Connection failed")

    def send_button(self, button_name: str):
        """Execute command based on MR20 button name."""
        def _send():
            name = button_name.upper()
            
            # Power & WoL
            if name in ("POWER", "POWER_OFF"):
                r = self.get_remote()
                if r:
                    r._LGTVRemote__send_command("request", "ssap://system/turnOff", None, callback=_noop)
                return
            elif name == "POWER_ON":
                mac = self.config_manager.get("tv_mac", "")
                if mac:
                    send_magic_packet(mac)
                return

            r = self.get_remote()
            if not r:
                print("Remote not connected")
                return

            # Volume & Mute (Toggle mute state)
            if name in ("VOL_UP", "VOLUME_UP", "+"):
                r.volumeUp(callback=_noop)
            elif name in ("VOL_DOWN", "VOLUME_DOWN", "-"):
                r.volumeDown(callback=_noop)
            elif name == "MUTE":
                self.is_muted = not self.is_muted
                r.mute(self.is_muted, callback=_noop)

            # Channels
            elif name in ("CH_UP", "CHANNEL_UP"):
                r.inputChannelUp(callback=_noop)
            elif name in ("CH_DOWN", "CHANNEL_DOWN"):
                r.inputChannelDown(callback=_noop)

            # Settings & Apps
            elif name in ("SETTINGS", "QSETTINGS"):
                r.startApp("com.palm.app.settings", callback=_noop)
            elif name in ("HOME", "HOUSE"):
                # Pointer HOME key provides native overlay
                if not self.send_pointer_key("HOME"):
                    r.startApp("com.webos.app.home", callback=_noop)
            elif name == "NETFLIX":
                r.startApp("netflix", callback=_noop)
            elif name in ("PRIME", "AMAZON"):
                r.startApp("amazon", callback=_noop)
            elif name == "MOVIES":
                r.startApp("com.webos.app.discovery", callback=_noop)
            elif name in ("INPUT"):
                r.listInputs(callback=_noop)
            elif name in ("VOICE"):
                r.startApp("com.webos.service.ai.voice", callback=_noop)
            elif name in ("GUIDE"):
                if not self.send_pointer_key("GUIDE"):
                    r._LGTVRemote__send_command("request", "ssap://tv/openProgramGuide", None, callback=_noop)

            # Media Controls
            elif name == "PLAY":
                if not self.send_pointer_key("PLAY"):
                    r.inputMediaPlay(callback=_noop)
            elif name == "PAUSE":
                if not self.send_pointer_key("PAUSE"):
                    r.inputMediaPause(callback=_noop)

            # Hardware D-Pad Arrow Keys (Up, Down, Left, Right)
            elif name in ("UP", "DOWN", "LEFT", "RIGHT"):
                self.send_pointer_key(name)

            # Wheel Select / OK / Enter
            elif name in ("OK", "ENTER"):
                if not self.send_pointer_key("ENTER"):
                    r.sendEnterKey(callback=_noop)

            # Back Button
            elif name in ("BACK", "EXIT"):
                self.send_pointer_key("BACK")

            # Color Buttons (Red, Green, Yellow, Blue)
            elif name in ("RED", "GREEN", "YELLOW", "BLUE"):
                self.send_pointer_key(name)

            # Number Pad Keys (0-9, Dash/List, More)
            elif name.isdigit():
                self.send_pointer_key(name)
            elif name in ("LIST", "DASH"):
                self.send_pointer_key("DASH")
            elif name in ("MORE", "MORE_ACTIONS"):
                self.send_pointer_key("ASTERISK")
            elif name == "STB_PWR":
                self.send_pointer_key("POWER")
            else:
                self.send_pointer_key(name)

        threading.Thread(target=_send, daemon=True).start()
