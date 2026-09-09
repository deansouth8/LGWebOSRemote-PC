import os
from PIL import Image, ImageDraw

img_path = "assets/themes/classic_black.png"
img = Image.open(img_path).convert("RGBA")
w, h = img.size

overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)

# High precision fine-tuned calibrated buttons
CALIBRATED_BUTTONS = [
    # Top Tip COG
    ("COG", 0.38, 0.62, 0.015, 0.065, "circle"),

    # Power Row
    ("POWER", 0.20, 0.42, 0.065, 0.118, "circle"),
    ("STB_PWR", 0.58, 0.80, 0.065, 0.118, "circle"),

    # Number Pad (Fine-tuned column centering)
    ("1", 0.10, 0.34, 0.130, 0.170, "rect"),
    ("2", 0.38, 0.62, 0.130, 0.170, "rect"),
    ("3", 0.66, 0.90, 0.130, 0.170, "rect"),

    ("4", 0.10, 0.34, 0.173, 0.213, "rect"),
    ("5", 0.38, 0.62, 0.173, 0.213, "rect"),
    ("6", 0.66, 0.90, 0.173, 0.213, "rect"),

    ("7", 0.10, 0.34, 0.216, 0.256, "rect"),
    ("8", 0.38, 0.62, 0.216, 0.256, "rect"),
    ("9", 0.66, 0.90, 0.216, 0.256, "rect"),

    ("LIST", 0.08, 0.34, 0.259, 0.299, "rect"),
    ("0", 0.38, 0.62, 0.259, 0.299, "rect"),
    ("MORE", 0.66, 0.92, 0.259, 0.299, "rect"),

    # Vol / Ch / Mute / Voice
    ("VOL_UP", 0.09, 0.33, 0.305, 0.360, "rect"),
    ("VOL_DN", 0.09, 0.33, 0.365, 0.425, "rect"),
    ("MUTE", 0.38, 0.62, 0.305, 0.360, "circle"),
    ("VOICE", 0.38, 0.62, 0.385, 0.445, "circle"),
    ("CH_UP", 0.67, 0.91, 0.305, 0.360, "rect"),
    ("CH_DN", 0.67, 0.91, 0.365, 0.425, "rect"),

    # Home & Settings
    ("HOME", 0.08, 0.32, 0.435, 0.490, "circle"),
    ("SETTINGS", 0.68, 0.92, 0.435, 0.490, "circle"),

    # D-Pad
    ("UP", 0.36, 0.64, 0.485, 0.535, "rect"),
    ("DOWN", 0.36, 0.64, 0.590, 0.640, "rect"),
    ("LEFT", 0.16, 0.36, 0.520, 0.605, "rect"),
    ("RIGHT", 0.64, 0.84, 0.520, 0.605, "rect"),
    ("OK", 0.38, 0.62, 0.525, 0.600, "circle"),

    # Back & Guide
    ("BACK", 0.08, 0.32, 0.635, 0.685, "circle"),
    ("GUIDE", 0.68, 0.92, 0.635, 0.685, "circle"),

    # Netflix / Input / Prime
    ("NETFLIX", 0.06, 0.36, 0.690, 0.740, "rect"),
    ("INPUT", 0.38, 0.62, 0.685, 0.740, "circle"),
    ("PRIME", 0.64, 0.94, 0.690, 0.740, "rect"),

    # Colors
    ("RED", 0.08, 0.28, 0.750, 0.785, "circle"),
    ("GREEN", 0.30, 0.48, 0.750, 0.785, "circle"),
    ("YELLOW", 0.52, 0.70, 0.750, 0.785, "circle"),
    ("BLUE", 0.72, 0.92, 0.750, 0.785, "circle"),

    # Movies / Play / Pause
    ("MOVIES", 0.08, 0.36, 0.790, 0.835, "rect"),
    ("PLAY", 0.38, 0.60, 0.790, 0.835, "rect"),
    ("PAUSE", 0.62, 0.88, 0.790, 0.835, "rect"),
]

for name, x1_r, x2_r, y1_r, y2_r, shape in CALIBRATED_BUTTONS:
    bx1 = int(x1_r * w)
    bx2 = int(x2_r * w)
    by1 = int(y1_r * h)
    by2 = int(y2_r * h)

    fill_c = (0, 255, 200, 70)
    outline_c = (0, 255, 200, 230)

    if shape == "circle":
        draw.ellipse([bx1, by1, bx2, by2], fill=fill_c, outline=outline_c, width=2)
    else:
        draw.rounded_rectangle([bx1, by1, bx2, by2], radius=4, fill=fill_c, outline=outline_c, width=2)

    draw.text((bx1 + 3, by1 + 2), name, fill=(255, 255, 255, 230))

result = Image.alpha_composite(img, overlay)

brain_dir = r"C:\Users\dean\.gemini\antigravity\brain\5d1f1359-4830-49df-a5f5-36a13042774c"
review_path_brain = os.path.join(brain_dir, "button_calibration_review.png")
result.save(review_path_brain)
result.save("assets/button_calibration_review.png")
print("Updated review image generated successfully!")
