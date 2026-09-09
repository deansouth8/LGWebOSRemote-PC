# 📺 LG WebOS Magic Remote PC Widget

A sleek, lightweight desktop remote control for **LG WebOS Smart TVs** inspired by the **2020 MR20 Magic Remote**. It floats seamlessly in the lower-right corner of your Windows desktop, docks into the system tray, and provides pixel-accurate button controls with full hardware-level TV integration.

---

## ✨ Features

- **📍 Desktop & System Tray Integration**: Lives in the Windows notification area (system tray). Double-clicking the tray icon toggles the remote window right above your taskbar.
- **🎨 6 Photorealistic Visual Themes**:
  1. **Classic Black**: High-definition studio finish of the original MR20 remote.
  2. **Silver Metallic**: Brushed aluminum finish with chrome accents.
  3. **USA Patriotic**: American Flag stars and stripes design.
  4. **Space Nebula**: Deep purple cosmic galaxy theme.
  5. **Mecha Robot**: Industrial titanium mecha armor with orange LED accents.
  6. **Gold Carbon**: 24k gold trim with woven carbon fiber texture.
- **⚙ Embedded Top-Tip COG Button**: An integrated gear button at the top tip of the remote for quick access to TV IP and pairing settings.
- **⌄ Bottom-Chin Minimize Bar**: A modern frosted-glass capsule on the bottom chin to smoothly dismiss the remote back into the taskbar / system tray.
- **🎯 Pixel-Accurate Hotspots**: Precise button bounding boxes and circular perspective highlights for Power, STB, Number Pad (0-9), Volume/Channel rockers, D-Pad cardinal directions, Wheel Click (OK), Back, Guide, Streaming Shortcuts (Netflix, Prime Video), Color feature keys, and Media playback controls.
- **⚡ Dual-Socket WebOS Engine**:
  - **SSAP WebSocket API**: Power, Volume +/-, Channel +/-, Mute/Unmute toggling, Quick Settings, External Inputs, and App Launchers.
  - **NetInput Pointer Socket**: Direct real-time byte-stream event streaming for responsive D-Pad arrow keys, Back, and Enter confirmations.

---

## 🚀 Quick Start (Running the Standalone Executable)

1. Download `LG_WebOS_Remote.exe` from the latest **[Releases](https://github.com/deansouth8/LGWebOSRemote-PC/releases)** page.
2. Double-click `LG_WebOS_Remote.exe`.
3. The remote will appear in the lower-right corner of your desktop, and a remote icon will appear in your system tray.
4. Click the **⚙ COG button** at the very top tip of the remote (or right-click the system tray icon ➔ **Connection Settings**).
5. Enter your LG TV's local IP address (e.g. `192.168.1.154`) and click **Connect / Pair TV**.
6. A one-time pairing prompt will pop up on your TV screen asking to allow the app. Click **"Allow"** on your TV using your physical remote.
7. You're done! The pairing key is securely saved in your user profile (`%APPDATA%\LG_Remote_App\config.json`) and automatically connects from then on.

---

## 🛠️ Building & Running from Source

### Requirements
- Windows 10 or 11
- Python 3.10+
- LG WebOS Smart TV connected to the same local Wi-Fi / LAN network

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/deansouth8/LGWebOSRemote-PC.git
   cd LGWebOSRemote-PC
   ```

2. **Create and activate a virtual environment**:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the application**:
   ```bash
   python main.py
   ```

### Packaging into a Standalone `.exe`

To compile the application into a single standalone `.exe` with all themes, icons, and dependencies embedded:

```bash
python build_exe.py
```

The compiled binary will be placed in `dist/LG_WebOS_Remote.exe`.

---

## 📺 LG TV Prerequisites

For the TV to accept network remote commands:
1. Turn on your TV.
2. Go to **Settings ➔ Connection / Network**.
3. Ensure **"Mobile TV On"** and **"LG Connect Apps"** (or **"External Device Connection"**) are toggled **ON**.

---

## 📂 Project Structure

```
LGWebOSRemote-PC/
├── assets/
│   ├── icon.ico                 # App & System tray icon
│   ├── mr20_remote.png          # Default remote asset
│   └── themes/                  # 6 switchable photorealistic themes
│       ├── classic_black.png
│       ├── silver_metallic.png
│       ├── usa_patriotic.png
│       ├── space_nebula.png
│       ├── mecha_robot.png
│       └── gold_carbon.png
├── src/
│   ├── LGTV/                    # Core WebOS SSAP & Pointer socket protocol engine
│   ├── button_mapping.py        # Pixel-calibrated button coordinates & shapes
│   ├── config_manager.py        # Persistent JSON configuration manager in %APPDATA%
│   ├── remote_ui.py             # PyQt6 borderless floating window & system tray logic
│   ├── settings_dialog.py       # Configuration & TV pairing dialog
│   └── webos_client.py          # High-level dual-socket client controller
├── build_exe.py                 # Automated PyInstaller packaging script
├── main.py                      # Application entry point
├── requirements.txt             # Python project dependencies
├── .gitignore                   # Git ignore configuration
└── README.md                    # Project documentation
```

---

## 🙏 Kudos & Acknowledgements

- **[klattimer/LGWebOSRemote](https://github.com/klattimer/LGWebOSRemote)**: Huge kudos and gratitude to Colin Klattimer and contributors for pioneering the reverse-engineered LG WebOS command structure, authentication handshake protocols, and SSAP payload specifications.
- **[ws4py](https://github.com/Lawouach/WebSocket-for-Python)**: Robust WebSocket client handling persistent connections to WebOS TV services.
- **[PyQt6](https://riverbankcomputing.com/software/pyqt/)**: Powerful framework providing hardware-accelerated translucent borderless windows and native Windows system tray integration.
- **LG Electronics**: For the iconic, ergonomic MR20 Magic Remote industrial design.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
