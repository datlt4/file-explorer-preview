from itertools import product
from PyQt5.QtGui import QFont
import sys

OS = sys.platform
if OS.startswith("win32"):
    # FONT = FONT
    FONT = "Noah"
elif OS.startswith("linux"):
    FONT = "Serif"
elif OS.startswith("darwin"):
    FONT = "Serif"
else:
    sys.exit(1)

class MFont():
    def __init__(self):
        self.fonts = {}
        self.define()

    def define(self):
        for size, t in product(range(8, 73), ["normal", "bold", "italic", "underline", "bold underline", "bold italic", "italic underline", "bold italic underline"]):
            font = QFont()
            font.setFamily(FONT)
            font.setPointSize(size)

            # Apply requested font type(s)
            if "bold" in t:
                font.setBold(True)
            if "italic" in t:
                font.setItalic(True)
            if "underline" in t:
                font.setUnderline(True)

            # Store font with a name based on size and type
            name = f"{size}{t.replace(' ', '').replace('bold', 'B').replace('italic', 'I').replace('underline', 'U').replace('normal', '')}"
            self.fonts[name] = font

if __name__ == "__main__":
    font = MFont()
    font.fonts["12B"]
