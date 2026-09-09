import os
import sys
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QSystemTrayIcon, QMenu,
    QLabel, QVBoxLayout, QToolTip
)
from PyQt6.QtGui import QIcon, QPixmap, QCursor, QMouseEvent, QPainter, QColor, QBrush, QPen
from PyQt6.QtCore import Qt, QPoint, QRect, QTimer

from src.button_mapping import find_button_at, BUTTONS
from src.settings_dialog import SettingsDialog

def get_resource_path(relative_path: str) -> str:
    """Get absolute path to resource, works for dev and for PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    base_dir = Path(__file__).parent.parent
    return str(base_dir / relative_path)

class RemoteWidget(QWidget):
    """Custom widget rendering MR20 remote control image with interactive button hotspots."""
    
    THEMES = {
        "Classic Black": "classic_black.png",
        "Silver Metallic": "silver_metallic.png",
        "USA Patriotic": "usa_patriotic.png",
        "Space Nebula": "space_nebula.png",
        "Mecha Robot": "mecha_robot.png",
        "Gold Carbon": "gold_carbon.png",
    }

    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.config_manager = parent_window.config_manager
        self.webos_client = parent_window.webos_client
        
        self.target_height = 640
        self.current_theme = self.config_manager.get("theme", "Classic Black")
        self.load_theme_pixmap(self.current_theme)
        self.setMouseTracking(True)
        
        self.current_hover_button = None
        self.pressed_button = None
        self.drag_start_pos = None

    def load_theme_pixmap(self, theme_name: str):
        self.current_theme = theme_name
        filename = self.THEMES.get(theme_name, "classic_black.png")
        path = get_resource_path(os.path.join("assets", "themes", filename))
        if not os.path.exists(path):
            path = get_resource_path(os.path.join("assets", "mr20_remote.png"))
            
        self.original_pixmap = QPixmap(path)
        self.target_width = int(self.original_pixmap.width() * (self.target_height / self.original_pixmap.height()))
        self.pixmap = self.original_pixmap.scaled(
            self.target_width, self.target_height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.setFixedSize(self.target_width, self.target_height)

    def mouseMoveEvent(self, event: QMouseEvent):
        rel_x = event.position().x() / self.width()
        rel_y = event.position().y() / self.height()

        btn = find_button_at(rel_x, rel_y)
        if btn != self.current_hover_button:
            self.current_hover_button = btn
            if btn:
                self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                QToolTip.showText(QCursor.pos(), btn.tooltip, self)
            else:
                self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
                QToolTip.hideText()
            self.update()

        if self.drag_start_pos and event.buttons() == Qt.MouseButton.LeftButton and not self.pressed_button:
            self.parent_window.move(event.globalPosition().toPoint() - self.drag_start_pos)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            rel_x = event.position().x() / self.width()
            rel_y = event.position().y() / self.height()
            
            btn = find_button_at(rel_x, rel_y)
            if btn:
                self.pressed_button = btn
                self.update()
                print(f"Button Clicked: {btn.name}")
                if btn.name == "APP_SETTINGS":
                    self.parent_window.open_settings()
                elif btn.name == "DISMISS":
                    self.parent_window.hide()
                else:
                    self.webos_client.send_button(btn.name)
            else:
                self.drag_start_pos = event.position().toPoint()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if self.pressed_button:
            self.pressed_button = None
            self.update()
        self.drag_start_pos = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw remote image
        painter.drawPixmap(0, 0, self.pixmap)
        
        # Draw sleek Dismiss / Minimize chin bar at the bottom
        dismiss_btns = [b for b in BUTTONS if b.name == "DISMISS"]
        if dismiss_btns:
            d_btn = dismiss_btns[0]
            dx = int(d_btn.x_min * self.width())
            dy = int(d_btn.y_min * self.height())
            dw = int((d_btn.x_max - d_btn.x_min) * self.width())
            dh = int((d_btn.y_max - d_btn.y_min) * self.height())

            is_hover = (self.current_hover_button and self.current_hover_button.name == "DISMISS")
            is_press = (self.pressed_button and self.pressed_button.name == "DISMISS")

            # Elegant frosted capsule styling
            bg = QColor(0, 160, 255, 140) if is_press else (QColor(35, 40, 50, 230) if is_hover else QColor(25, 25, 30, 200))
            border = QColor(0, 210, 255, 240) if (is_hover or is_press) else QColor(255, 255, 255, 60)

            painter.setBrush(QBrush(bg))
            painter.setPen(QPen(border, 1.5))
            painter.drawRoundedRect(QRect(dx, dy, dw, dh), dh // 2, dh // 2)

            txt_color = QColor(0, 225, 255) if is_hover else QColor(210, 215, 225)
            painter.setPen(QPen(txt_color, 1))
            f = painter.font()
            f.setPointSize(8)
            f.setBold(True)
            painter.setFont(f)
            painter.drawText(QRect(dx, dy, dw, dh), Qt.AlignmentFlag.AlignCenter, "⌄ Minimize")

        # Draw accurate perspective button highlight
        target_btn = self.pressed_button or self.current_hover_button
        if target_btn and target_btn.name != "DISMISS":
            bx = int(target_btn.x_min * self.width())
            by = int(target_btn.y_min * self.height())
            bw = int((target_btn.x_max - target_btn.x_min) * self.width())
            bh = int((target_btn.y_max - target_btn.y_min) * self.height())
            
            is_press = (target_btn == self.pressed_button)
            fill_color = QColor(255, 255, 255, 110) if is_press else QColor(0, 180, 255, 75)
            stroke_color = QColor(255, 255, 255, 220) if is_press else QColor(0, 200, 255, 200)
            
            painter.setBrush(QBrush(fill_color))
            painter.setPen(QPen(stroke_color, 2))
            
            if target_btn.shape == "circle":
                painter.drawEllipse(QRect(bx, by, bw, bh))
            else:
                painter.drawRoundedRect(QRect(bx, by, bw, bh), 6, 6)


class RemoteMainWindow(QMainWindow):
    """Main window hosting the floating LG MR20 remote widget."""
    
    def __init__(self, config_manager, webos_client):
        super().__init__()
        self.config_manager = config_manager
        self.webos_client = webos_client
        
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        
        self.remote_widget = RemoteWidget(self)
        self.setCentralWidget(self.remote_widget)
        self.setFixedSize(self.remote_widget.size())
        
        # System Tray Icon
        icon_path = get_resource_path(os.path.join("assets", "icon.ico"))
        
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(icon_path))
        self.tray_icon.setToolTip("LG WebOS Remote Control (Double-click to open)")
        
        # Tray Menu
        tray_menu = QMenu()
        show_action = tray_menu.addAction("Show/Hide Remote")
        show_action.triggered.connect(self.toggle_visibility)
        
        settings_action = tray_menu.addAction("Connection Settings...")
        settings_action.triggered.connect(self.open_settings)
        
        tray_menu.addSeparator()
        exit_action = tray_menu.addAction("Exit")
        exit_action.triggered.connect(QApplication.instance().quit)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_activated)
        self.tray_icon.show()
        
        self.position_bottom_right()

    def position_bottom_right(self):
        """Position remote window at lower-right corner of desktop screen."""
        screen = QApplication.primaryScreen()
        if screen:
            geom = screen.availableGeometry()
            x = geom.width() - self.width() - 20
            y = geom.height() - self.height() - 20
            self.move(max(0, x), max(0, y))

    def on_tray_activated(self, reason):
        if reason in (QSystemTrayIcon.ActivationReason.DoubleClick, QSystemTrayIcon.ActivationReason.Trigger):
            self.toggle_visibility()

    def toggle_visibility(self):
        if self.isVisible():
            self.hide()
        else:
            self.position_bottom_right()
            self.show()
            self.raise_()
            self.activateWindow()

    def open_settings(self):
        dialog = SettingsDialog(self.config_manager, self.webos_client, self)
        if dialog.exec():
            # Update window stays on top flag
            on_top = self.config_manager.get("always_on_top", True)
            flags = Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool
            if on_top:
                flags |= Qt.WindowType.WindowStaysOnTopHint
            self.setWindowFlags(flags)

            # Update theme
            new_theme = self.config_manager.get("theme", "Classic Black")
            self.remote_widget.load_theme_pixmap(new_theme)
            self.setFixedSize(self.remote_widget.size())
            self.position_bottom_right()
            self.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.hide()
        else:
            super().keyPressEvent(event)
