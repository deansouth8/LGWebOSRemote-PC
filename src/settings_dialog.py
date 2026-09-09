from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QCheckBox, QComboBox, QGroupBox, QMessageBox
)
from PyQt6.QtCore import Qt

class SettingsDialog(QDialog):
    def __init__(self, config_manager, webos_client, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.webos_client = webos_client
        self.setWindowTitle("LG WebOS Remote Settings")
        self.setFixedSize(400, 320)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Connection Group
        conn_group = QGroupBox("LG WebOS TV Connection")
        conn_layout = QVBoxLayout()

        # IP Address
        ip_layout = QHBoxLayout()
        ip_layout.addWidget(QLabel("TV IP Address:"))
        self.ip_input = QLineEdit(self.config_manager.get("tv_ip", "192.168.1.100"))
        ip_layout.addWidget(self.ip_input)
        conn_layout.addLayout(ip_layout)

        # MAC Address (Optional for Wake On LAN)
        mac_layout = QHBoxLayout()
        mac_layout.addWidget(QLabel("TV MAC Address (Optional):"))
        self.mac_input = QLineEdit(self.config_manager.get("tv_mac", ""))
        self.mac_input.setPlaceholderText("AA:BB:CC:DD:EE:FF")
        mac_layout.addWidget(self.mac_input)
        conn_layout.addLayout(mac_layout)

        # Test Connection / Pair Button
        self.pair_btn = QPushButton("Connect / Pair TV")
        self.pair_btn.setStyleSheet("font-weight: bold; background-color: #0078d7; color: white; padding: 6px;")
        self.pair_btn.clicked.connect(self.on_pair_clicked)
        conn_layout.addWidget(self.pair_btn)

        self.status_label = QLabel("Status: Idle")
        self.status_label.setWordWrap(True)
        conn_layout.addWidget(self.status_label)

        conn_group.setLayout(conn_layout)
        layout.addWidget(conn_group)

        # Window & Visual Theme Group
        behavior_group = QGroupBox("Visual Theme & Window Preferences")
        behavior_layout = QVBoxLayout()
        
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel("Remote Theme:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems([
            "Classic Black",
            "Silver Metallic",
            "USA Patriotic",
            "Space Nebula",
            "Mecha Robot",
            "Gold Carbon"
        ])
        saved_theme = self.config_manager.get("theme", "Classic Black")
        idx = self.theme_combo.findText(saved_theme)
        if idx >= 0:
            self.theme_combo.setCurrentIndex(idx)
        theme_layout.addWidget(self.theme_combo)
        behavior_layout.addLayout(theme_layout)

        self.always_top_chk = QCheckBox("Keep remote window always on top")
        self.always_top_chk.setChecked(self.config_manager.get("always_on_top", True))
        behavior_layout.addWidget(self.always_top_chk)

        self.auto_dismiss_chk = QCheckBox("Auto-dismiss remote when clicking outside")
        self.auto_dismiss_chk.setChecked(self.config_manager.get("auto_dismiss", False))
        behavior_layout.addWidget(self.auto_dismiss_chk)

        behavior_group.setLayout(behavior_layout)
        layout.addWidget(behavior_group)

        # Config File Path Info
        config_group = QGroupBox("Configuration Storage")
        config_layout = QVBoxLayout()
        cfg_path_str = str(self.config_manager.config_path)
        config_label = QLabel(f"File Path:\n{cfg_path_str}")
        config_label.setStyleSheet("color: #555555; font-size: 11px;")
        config_label.setWordWrap(True)
        config_layout.addWidget(config_label)

        open_folder_btn = QPushButton("Open Config Folder in Explorer")
        open_folder_btn.clicked.connect(self.open_config_folder)
        config_layout.addWidget(open_folder_btn)

        config_group.setLayout(config_layout)
        layout.addWidget(config_group)

        # Buttons
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save & Close")
        save_btn.clicked.connect(self.on_save)
        btn_layout.addWidget(save_btn)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        layout.addLayout(btn_layout)

    def open_config_folder(self):
        import os
        folder = str(self.config_manager.app_dir)
        if os.path.exists(folder):
            os.startfile(folder)

    def on_pair_clicked(self):
        ip = self.ip_input.text().strip()
        if not ip:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid IP address.")
            return

        self.config_manager.set("tv_ip", ip)
        self.config_manager.set("tv_mac", self.mac_input.text().strip())
        self.pair_btn.setEnabled(False)
        self.status_label.setText("Connecting... Check TV screen if pairing prompt appears!")

        def _on_finish(success, message):
            self.pair_btn.setEnabled(True)
            if success:
                self.status_label.setText("Status: Successfully connected & paired!")
            else:
                self.status_label.setText(f"Status: Failed ({message})")

        self.webos_client.connect_async(on_finish=_on_finish)

    def on_save(self):
        self.config_manager.set("tv_ip", self.ip_input.text().strip())
        self.config_manager.set("tv_mac", self.mac_input.text().strip())
        self.config_manager.set("theme", self.theme_combo.currentText())
        self.config_manager.set("always_on_top", self.always_top_chk.isChecked())
        self.config_manager.set("auto_dismiss", self.auto_dismiss_chk.isChecked())
        self.accept()
