class ButtonDefinition:
    def __init__(self, name: str, x_min: float, x_max: float, y_min: float, y_max: float, tooltip: str, shape: str = "rect"):
        self.name = name
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.tooltip = tooltip
        self.shape = shape  # "rect", "circle"

    def contains(self, rel_x: float, rel_y: float) -> bool:
        return self.x_min <= rel_x <= self.x_max and self.y_min <= rel_y <= self.y_max


BUTTONS = [
    # Top Tip COG Button
    ButtonDefinition("APP_SETTINGS", 0.38, 0.62, 0.015, 0.065, "⚙ App & TV Settings", shape="circle"),

    # Top Power & STB Power
    ButtonDefinition("POWER", 0.20, 0.42, 0.065, 0.118, "Power Off TV", shape="circle"),
    ButtonDefinition("STB_PWR", 0.58, 0.80, 0.065, 0.118, "Set-Top Box Power", shape="circle"),

    # Number Pad
    ButtonDefinition("1", 0.10, 0.34, 0.130, 0.170, "Number 1", shape="rect"),
    ButtonDefinition("2", 0.38, 0.62, 0.130, 0.170, "Number 2", shape="rect"),
    ButtonDefinition("3", 0.66, 0.90, 0.130, 0.170, "Number 3", shape="rect"),

    ButtonDefinition("4", 0.10, 0.34, 0.173, 0.213, "Number 4", shape="rect"),
    ButtonDefinition("5", 0.38, 0.62, 0.173, 0.213, "Number 5", shape="rect"),
    ButtonDefinition("6", 0.66, 0.90, 0.173, 0.213, "Number 6", shape="rect"),

    ButtonDefinition("7", 0.10, 0.34, 0.216, 0.256, "Number 7", shape="rect"),
    ButtonDefinition("8", 0.38, 0.62, 0.216, 0.256, "Number 8", shape="rect"),
    ButtonDefinition("9", 0.66, 0.90, 0.216, 0.256, "Number 9", shape="rect"),

    ButtonDefinition("LIST", 0.08, 0.34, 0.259, 0.299, "- / LIST: Saved Channel List", shape="rect"),
    ButtonDefinition("0", 0.38, 0.62, 0.259, 0.299, "Number 0", shape="rect"),
    ButtonDefinition("MORE_ACTIONS", 0.66, 0.92, 0.259, 0.299, "... Quick Access / SAP", shape="rect"),

    # Vol / Ch / Mute / Voice
    ButtonDefinition("VOL_UP", 0.09, 0.33, 0.305, 0.360, "Volume Up (+)", shape="rect"),
    ButtonDefinition("VOL_DOWN", 0.09, 0.33, 0.365, 0.425, "Volume Down (-)", shape="rect"),
    ButtonDefinition("MUTE", 0.38, 0.62, 0.305, 0.360, "Mute All Sound", shape="circle"),
    ButtonDefinition("VOICE", 0.38, 0.62, 0.385, 0.445, "Voice Search", shape="circle"),
    ButtonDefinition("CH_UP", 0.67, 0.91, 0.305, 0.360, "Channel Up", shape="rect"),
    ButtonDefinition("CH_DOWN", 0.67, 0.91, 0.365, 0.425, "Channel Down", shape="rect"),

    # Home & Settings
    ButtonDefinition("HOME", 0.08, 0.32, 0.435, 0.490, "Home Menu", shape="circle"),
    ButtonDefinition("SETTINGS", 0.68, 0.92, 0.435, 0.490, "Q. Settings", shape="circle"),

    # D-Pad
    ButtonDefinition("UP", 0.36, 0.64, 0.485, 0.535, "Up Arrow", shape="rect"),
    ButtonDefinition("DOWN", 0.36, 0.64, 0.590, 0.640, "Down Arrow", shape="rect"),
    ButtonDefinition("LEFT", 0.16, 0.36, 0.520, 0.605, "Left Arrow", shape="rect"),
    ButtonDefinition("RIGHT", 0.64, 0.84, 0.520, 0.605, "Right Arrow", shape="rect"),
    ButtonDefinition("OK", 0.38, 0.62, 0.525, 0.600, "Wheel Select / OK", shape="circle"),

    # Back & Guide
    ButtonDefinition("BACK", 0.08, 0.32, 0.635, 0.685, "Back / Exit", shape="circle"),
    ButtonDefinition("GUIDE", 0.68, 0.92, 0.635, 0.685, "TV Guide", shape="circle"),

    # Streaming Shortcuts & Input
    ButtonDefinition("NETFLIX", 0.06, 0.36, 0.690, 0.740, "Launch Netflix", shape="rect"),
    ButtonDefinition("INPUT", 0.38, 0.62, 0.685, 0.740, "Input Source", shape="circle"),
    ButtonDefinition("PRIME", 0.64, 0.94, 0.690, 0.740, "Launch Prime Video", shape="rect"),

    # Color Buttons
    ButtonDefinition("RED", 0.08, 0.28, 0.750, 0.785, "Red Feature Key", shape="circle"),
    ButtonDefinition("GREEN", 0.30, 0.48, 0.750, 0.785, "Green Feature Key", shape="circle"),
    ButtonDefinition("YELLOW", 0.52, 0.70, 0.750, 0.785, "Yellow Feature Key", shape="circle"),
    ButtonDefinition("BLUE", 0.72, 0.92, 0.750, 0.785, "Blue Feature Key", shape="circle"),

    # Media Controls
    ButtonDefinition("MOVIES", 0.08, 0.36, 0.790, 0.835, "LG Movies / Discovery", shape="rect"),
    ButtonDefinition("PLAY", 0.38, 0.60, 0.790, 0.835, "Play Media", shape="rect"),
    ButtonDefinition("PAUSE", 0.62, 0.88, 0.790, 0.835, "Pause Media", shape="rect"),

    # Bottom Chin Dismiss to Taskbar Button
    ButtonDefinition("DISMISS", 0.22, 0.78, 0.935, 0.985, "Dismiss Remote to Taskbar / System Tray", shape="pill"),
]

def find_button_at(rel_x: float, rel_y: float) -> ButtonDefinition:
    for btn in BUTTONS:
        if btn.contains(rel_x, rel_y):
            return btn
    return None
