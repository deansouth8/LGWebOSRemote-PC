import json
import os
from pathlib import Path

class ConfigManager:
    """Manages application configuration stored in APPDATA."""
    
    def __init__(self):
        self.app_dir = Path(os.environ.get("APPDATA", Path.home())) / "LG_Remote_App"
        self.app_dir.mkdir(parents=True, exist_ok=True)
        self.config_path = self.app_dir / "config.json"
        
        self.defaults = {
            "tv_ip": "192.168.1.154",
            "client_key": "5d231b9dcc42018e0e8803bd678d834a",
            "tv_mac": "F8:B9:5A:A6:14:50",
            "theme": "Classic Black",
            "always_on_top": True,
            "auto_dismiss": False,
            "window_scale": 0.45,
        }
        self.config = self.load_config()

    def load_config(self) -> dict:
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    merged = self.defaults.copy()
                    merged.update(data)
                    return merged
            except Exception as e:
                print(f"Error reading config: {e}")
        return self.defaults.copy()

    def save_config(self):
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get(self, key: str, default=None):
        return self.config.get(key, default if default is not None else self.defaults.get(key))

    def set(self, key: str, value):
        self.config[key] = value
        self.save_config()
