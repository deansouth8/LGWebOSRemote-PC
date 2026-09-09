import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import QApplication

from src.config_manager import ConfigManager
from src.webos_client import LGWebOSClient
from src.remote_ui import RemoteMainWindow

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setApplicationName("LG WebOS Remote")
    
    # Enable high DPI scaling
    assets_dir = Path(__file__).parent / "assets"
    icon_path = assets_dir / "icon.ico"
    if icon_path.exists():
        from PyQt6.QtGui import QIcon
        app.setWindowIcon(QIcon(str(icon_path)))
        
    config_mgr = ConfigManager()
    webos_client = LGWebOSClient(config_mgr)
    
    # Auto connect to TV in background
    webos_client.connect_async()
    
    window = RemoteMainWindow(config_mgr, webos_client)
    
    # Show main window on start
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
