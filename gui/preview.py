import os
import re
import sys
from functools import partial
from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QSpacerItem, QComboBox, QSizePolicy, QWidget, QPushButton, QGridLayout, QStackedWidget, QFileDialog, QCheckBox, QLineEdit
from PyQt5.QtGui import QPixmap
from datetime import datetime
from glob import glob

class FavouriteLinkWidgetSignal(QObject):
    signal_favorite_link = pyqtSignal(str)

class FavouriteLinkWidget(QWidget):
    def __init__(self, favouriteLinkWidget, font):
        super(FavouriteLinkWidget, self).__init__()
        # Policy
        self.sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.sizePolicy.setHorizontalStretch(0)
        self.sizePolicy.setVerticalStretch(0)
        self.sizePolicy.setHeightForWidth(favouriteLinkWidget.sizePolicy().hasHeightForWidth())
        # Layout, signal
        self.favouriteLinkWidget = favouriteLinkWidget
        self.favouriteLinkLayout = QHBoxLayout(self.favouriteLinkWidget)
        self.font = font
        self.signals = FavouriteLinkWidgetSignal()
        # 0
        self.favouriteLinkLabel = QLabel(self.favouriteLinkWidget)
        self.favouriteLinkLabel.setText("Favourite Link:")
        self.favouriteLinkLabel.setFont(self.font.fonts["14B"])
        self.favouriteLinkLabel.setAlignment(Qt.AlignCenter)
        self.favouriteLinkLabel.setStyleSheet("background-color: transparent; color: #075e6f; border: transparent; padding: 10;")
        self.favouriteLinkLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.favouriteLinkLayout.addWidget(self.favouriteLinkLabel, 0)
        # 1
        self.favouriteLinkComboBox = QComboBox(self.favouriteLinkWidget)
        self.favouriteLinkComboBox.setFont(self.font.fonts["12B"])
        self.favouriteLinkComboBox.setStyleSheet("""QComboBox{ background-color: white; padding-left: 15px }
                                            QComboBox:QAbstractItemView{ background-color: white; color:orange; padding-left: 15px }""")
        self.favouriteLinkComboBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.reloadFavouriteLinkComboBox(["all"])
        self.sizePolicy.setHeightForWidth(self.favouriteLinkComboBox.sizePolicy().hasHeightForWidth())
        self.favouriteLinkLayout.addWidget(self.favouriteLinkComboBox, 1)
        # 2
        self.button1 = QPushButton(self.favouriteLinkWidget)
        self.button1.setText("Button 1")
        self.button1.setFont(self.font.fonts["14"])
        self.button1.setStyleSheet("""QPushButton{ background-color: #068170; color: #ffffff; border: transparent; padding: 5; border-radius: 10; }
                                    QPushButton::pressed{ background-color: #088170; color: #ffffff; border: transparent; padding: 5; border-radius: 10; }
                                    QPushButton::hover{ background-color: #229586; color: #ffffff; border: transparent; padding: 5; border-radius: 10; }""")
        self.favouriteLinkLayout.addWidget(self.button1, 2)
        # 3
        self.button2 = QPushButton(self.favouriteLinkWidget)
        self.button2.setText("Button 2")
        self.button2.setFont(self.font.fonts["14"])
        self.button2.setStyleSheet("""QPushButton{ background-color: #068170; color: #ffffff; border: transparent; padding: 5; border-radius: 10; }
                                    QPushButton::pressed{ background-color: #088170; color: #ffffff; border: transparent; padding: 5; border-radius: 10; }
                                    QPushButton::hover{ background-color: #229586; color: #ffffff; border: transparent; padding: 5; border-radius: 10; }""")
        self.favouriteLinkLayout.addWidget(self.button2, 3)
        # Stretch
        self.favouriteLinkLayout.setStretch(0, 2)
        self.favouriteLinkLayout.setStretch(1, 5)
        self.favouriteLinkLayout.setStretch(2, 2)
        self.favouriteLinkLayout.setStretch(3, 2)
        self.favouriteLinkWidget.setLayout(self.favouriteLinkLayout)

    def reloadFavouriteLinkComboBox(self, listValues):
        self.favouriteLinkComboBox.clear()
        for itemContent in listValues:
            self.favouriteLinkComboBox.addItem(itemContent)

class VisualPreviewWidgetSignal(QObject):
    signal_visual_preview = pyqtSignal(str)
    signal_send_current_image = pyqtSignal(str)

class VisualPreviewWidget(QWidget):
    def __init__(self, visualPreviewWidget, font, destop_w, destop_h):
        super(VisualPreviewWidget, self).__init__()
        # Policy
        self.sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.sizePolicy.setHorizontalStretch(0)
        self.sizePolicy.setVerticalStretch(0)
        self.sizePolicy.setHeightForWidth(visualPreviewWidget.sizePolicy().hasHeightForWidth())
        # self.setStyleSheet("border: 1px solid transparent;")
        # Layout, signal
        self.visualPreviewWidget = visualPreviewWidget
        self.visualPreviewWLayout = QHBoxLayout(self.visualPreviewWidget)
        self.font = font
        self.signals = VisualPreviewWidgetSignal()
        # 0
        self.leftTriangleButton = QPushButton(self.visualPreviewWidget)
        self.leftTriangleButton.setText("◀")
        self.leftTriangleButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.leftTriangleButton.setFont(self.font.fonts["14"])
        self.leftTriangleButton.setStyleSheet("""QPushButton{ background-color: #068170; color: #ffffff; border: transparent; padding: 5; border-radius: 2; }
                                    QPushButton::pressed{ background-color: #088170; color: #ffffff; border: transparent; padding: 5; border-radius: 2; }
                                    QPushButton::hover{ background-color: #229586; color: #ffffff; border: transparent; padding: 5; border-radius: 2; }""")
        self.leftTriangleButton.clicked.connect(self.prev)
        self.visualPreviewWLayout.addWidget(self.leftTriangleButton, 2)
        # 1
        self.visualPreviewPixmap = QLabel(self.visualPreviewWidget)
        self.visualPreviewPixmap.setStyleSheet("background-color: black; color: #075e6f; border: transparent; padding: 10;")
        self.visualPreviewPixmap.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.visualPreviewPixmap.setScaledContents(True)
        self.visualPreviewPixmap.setAlignment(Qt.AlignCenter)
        self.visualPreviewPixmap.setFixedSize(int(destop_w / 3.975), int(destop_h / 2.175))
        self.visualPreviewWLayout.addWidget(self.visualPreviewPixmap, 2)
        # 2
        self.rightTriangleButton = QPushButton(self.visualPreviewWidget)
        self.rightTriangleButton.setText("▶")
        self.rightTriangleButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.rightTriangleButton.setFont(self.font.fonts["14"])
        self.rightTriangleButton.setStyleSheet("""QPushButton{ background-color: #068170; color: #ffffff; border: transparent; padding: 5; border-radius: 2; }
                                    QPushButton::pressed{ background-color: #088170; color: #ffffff; border: transparent; padding: 5; border-radius: 2; }
                                    QPushButton::hover{ background-color: #229586; color: #ffffff; border: transparent; padding: 5; border-radius: 2; }""")
        self.rightTriangleButton.clicked.connect(self.next)
        self.visualPreviewWLayout.addWidget(self.rightTriangleButton, 2)
        # 3
        self.openInNewWindowWidget = QWidget(self.visualPreviewWidget)
        self.initOpenInNewWindow()
        self.visualPreviewWLayout.addWidget(self.openInNewWindowWidget, 2)
        # Stretch
        self.visualPreviewWLayout.setStretch(0, 1)
        self.visualPreviewWLayout.setStretch(1, 20)
        self.visualPreviewWLayout.setStretch(2, 1)
        self.visualPreviewWLayout.setStretch(3, 5)
        self.visualPreviewWidget.setLayout(self.visualPreviewWLayout)
        # Params
        self.listFiles = []
        self.extensions = ["*.PNG", "*.JPG"]
        self.current = 0

    def initOpenInNewWindow(self):
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.openInNewWindowWidget.sizePolicy().hasHeightForWidth())
        self.openInNewWindowWidget.setSizePolicy(sizePolicy)
        self.openInNewWindowLayout = QVBoxLayout(self.openInNewWindowWidget)
        # 0
        self.unitLabel = QLabel(self.openInNewWindowWidget)
        self.unitLabel.setText("UNIT: MM/INCH")
        self.unitLabel.setFont(self.font.fonts["14"])
        self.unitLabel.setAlignment(Qt.AlignCenter)
        self.unitLabel.setStyleSheet("background-color: transparent; color: #075e6f; border: transparent; padding: 10;")
        self.unitLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.openInNewWindowLayout.addWidget(self.unitLabel, 0)
        # 1
        self.openInNewWindowCheckbox = QCheckBox(self.openInNewWindowWidget)
        self.openInNewWindowCheckbox.setText("Open in new window")
        self.openInNewWindowLayout.addWidget(self.openInNewWindowCheckbox, 1)
        # 2
        self.openInNewWindowLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))

        self.openInNewWindowLayout.setStretch(0, 1)
        self.openInNewWindowLayout.setStretch(1, 10)
        self.openInNewWindowLayout.setStretch(1, 5)
        self.openInNewWindowWidget.setLayout(self.openInNewWindowLayout)

    def resetPreview(self):
        self.visualPreviewPixmap.setPixmap(QPixmap())
    
    def resetAll(self):
        self.listFiles = []
        self.extensions = []
        self.current = 0
        self.resetPreview()

    def showPreview(self):
        if (self.current >= 0) and (self.current < len(self.listFiles)) and os.path.exists(self.listFiles[self.current]):
            pixmap = QPixmap(self.listFiles[self.current])
            pixmap = pixmap.scaled(self.visualPreviewPixmap.size(), Qt.KeepAspectRatio)
            self.visualPreviewPixmap.setPixmap(pixmap)
            # self.visualPreviewPixmap.show()
            self.signals.signal_send_current_image.emit(self.listFiles[self.current])
            return True
        else:
            self.visualPreviewPixmap.setPixmap(QPixmap())
            self.signals.signal_send_current_image.emit("")
            return False

    def updateListFiles(self, path, extensions=None):
        self.extensions = self.extensions if extensions is None else re.findall(r'(\*\.[\*\w]+)', extensions)
        if os.path.exists(path):
            self.listFiles = []
            for ext in self.extensions:
                self.listFiles.extend([fn.replace("\\", "/") for fn in glob(os.path.join(path if os.path.isdir(path) else os.path.dirname(path), ext))])

            self.listFiles.sort()
            try:
                self.current = self.listFiles.index(path.replace("\\", "/"))
            except ValueError:
                self.current = 0

            self.showPreview()

    def next(self):
        if (self.current + 1 < len(self.listFiles)):
            self.current += 1
            if self.showPreview():
                return
            else:
                self.next()
        else:
            self.current = 0
            if self.showPreview():
                return
            else:
                self.resetPreview()

    def prev(self):
        if (self.current - 1 >= 0):
            self.current -= 1
            if self.showPreview():
                return
            else:
                self.prev()
        else:
            self.current = len(self.listFiles) - 1 
            if self.showPreview():
                return
            else:
                self.resetPreview()

class ShowLenghtValuesWidgetSignal(QObject):
    signal_visual_preview = pyqtSignal(str)

class ShowLenghtValuesWidget(QWidget):
    def __init__(self, showLenghtValuesWidget, font):
        super(ShowLenghtValuesWidget, self).__init__()
        # Policy
        self.sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.sizePolicy.setHorizontalStretch(0)
        self.sizePolicy.setVerticalStretch(0)
        self.sizePolicy.setHeightForWidth(showLenghtValuesWidget.sizePolicy().hasHeightForWidth())
        # self.setStyleSheet("border: 1px solid transparent;")
        # Layout, signal
        self.showLenghtValuesWidget = showLenghtValuesWidget
        self.howLenghtValuesLayout = QGridLayout(self.showLenghtValuesWidget)
        self.font = font
        self.signals = ShowLenghtValuesWidgetSignal()
        # 0, 0
        self.lenghtLabel1 = QLabel(self.showLenghtValuesWidget)
        self.lenghtLabel1.setText("Length:")
        self.lenghtLabel1.setFont(self.font.fonts["12"])
        self.lenghtLabel1.setAlignment(Qt.AlignRight)
        self.lenghtLabel1.setStyleSheet("background-color: transparent; color: #075e6f; border: transparent; padding: 10;")
        self.lenghtLabel1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.howLenghtValuesLayout.addWidget(self.lenghtLabel1, 0, 0, 1, 1)
        # 1, 0
        self.lenghtLabel2 = QLabel(self.showLenghtValuesWidget)
        self.lenghtLabel2.setText("Length:")
        self.lenghtLabel2.setFont(self.font.fonts["12"])
        self.lenghtLabel2.setAlignment(Qt.AlignRight)
        self.lenghtLabel2.setStyleSheet("background-color: transparent; color: #075e6f; border: transparent; padding: 10;")
        self.lenghtLabel2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.howLenghtValuesLayout.addWidget(self.lenghtLabel2, 1, 0, 1, 1)
        # 2, 0
        self.lenghtLabel3 = QLabel(self.showLenghtValuesWidget)
        self.lenghtLabel3.setText("Length:")
        self.lenghtLabel3.setFont(self.font.fonts["12"])
        self.lenghtLabel3.setAlignment(Qt.AlignRight)
        self.lenghtLabel3.setStyleSheet("background-color: transparent; color: #075e6f; border: transparent; padding: 10;")
        self.lenghtLabel3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.howLenghtValuesLayout.addWidget(self.lenghtLabel3, 2, 0, 1, 1)
        # 3, 0
        self.lenghtLabel4 = QLabel(self.showLenghtValuesWidget)
        self.lenghtLabel4.setText("Length:")
        self.lenghtLabel4.setFont(self.font.fonts["12"])
        self.lenghtLabel4.setAlignment(Qt.AlignRight)
        self.lenghtLabel4.setStyleSheet("background-color: transparent; color: #075e6f; border: transparent; padding: 10;")
        self.lenghtLabel4.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.howLenghtValuesLayout.addWidget(self.lenghtLabel4, 3, 0, 1, 1)
        # 4, 0
        self.totalLengLabel = QLabel(self.showLenghtValuesWidget)
        self.totalLengLabel.setText("Total length:")
        self.totalLengLabel.setFont(self.font.fonts["12"])
        self.totalLengLabel.setAlignment(Qt.AlignRight)
        self.totalLengLabel.setStyleSheet("background-color: transparent; color: #075e6f; border: transparent; padding: 10;")
        self.totalLengLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.howLenghtValuesLayout.addWidget(self.totalLengLabel, 4, 0, 1, 1)
        # ----------------------
        # 0, 1
        self.lenght1ComboBox = QComboBox(self.showLenghtValuesWidget)
        self.lenght1ComboBox.setFont(self.font.fonts["12B"])
        self.lenght1ComboBox.setStyleSheet("""QComboBox{ background-color: white; padding-left: 15px }
                                            QComboBox:QAbstractItemView{ background-color: white; color:orange; padding-left: 15px }""")
        self.lenght1ComboBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.reloadCombobox(self.lenght1ComboBox, ["#"])
        self.sizePolicy.setHeightForWidth(self.lenght1ComboBox.sizePolicy().hasHeightForWidth())
        self.howLenghtValuesLayout.addWidget(self.lenght1ComboBox, 0, 1, 1, 1)
        # 1, 1
        self.lenght2ComboBox = QComboBox(self.showLenghtValuesWidget)
        self.lenght2ComboBox.setFont(self.font.fonts["12B"])
        self.lenght2ComboBox.setStyleSheet("""QComboBox{ background-color: white; padding-left: 15px }
                                            QComboBox:QAbstractItemView{ background-color: white; color:orange; padding-left: 15px }""")
        self.lenght2ComboBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.reloadCombobox(self.lenght2ComboBox, ["#"])
        self.sizePolicy.setHeightForWidth(self.lenght2ComboBox.sizePolicy().hasHeightForWidth())
        self.howLenghtValuesLayout.addWidget(self.lenght2ComboBox, 1, 1, 1, 1)
        # 2, 1
        self.lenght3ComboBox = QComboBox(self.showLenghtValuesWidget)
        self.lenght3ComboBox.setFont(self.font.fonts["12B"])
        self.lenght3ComboBox.setStyleSheet("""QComboBox{ background-color: white; padding-left: 15px }
                                            QComboBox:QAbstractItemView{ background-color: white; color:orange; padding-left: 15px }""")
        self.lenght3ComboBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.reloadCombobox(self.lenght3ComboBox, ["#"])
        self.sizePolicy.setHeightForWidth(self.lenght3ComboBox.sizePolicy().hasHeightForWidth())
        self.howLenghtValuesLayout.addWidget(self.lenght3ComboBox, 2, 1, 1, 1)
        # 3, 1
        self.lenght4ComboBox = QComboBox(self.showLenghtValuesWidget)
        self.lenght4ComboBox.setFont(self.font.fonts["12B"])
        self.lenght4ComboBox.setStyleSheet("""QComboBox{ background-color: white; padding-left: 15px }
                                            QComboBox:QAbstractItemView{ background-color: white; color:orange; padding-left: 15px }""")
        self.lenght4ComboBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.reloadCombobox(self.lenght4ComboBox, ["#"])
        self.sizePolicy.setHeightForWidth(self.lenght4ComboBox.sizePolicy().hasHeightForWidth())
        self.howLenghtValuesLayout.addWidget(self.lenght4ComboBox, 3, 1, 1, 1)
        # 4, 1
        self.totalLengthLineEdit = QLineEdit(self.showLenghtValuesWidget)
        self.totalLengthLineEdit.setText("0")
        self.totalLengthLineEdit.setFont(self.font.fonts["12"])
        self.totalLengthLineEdit.setAlignment(Qt.AlignLeft)
        self.totalLengthLineEdit.setStyleSheet("background-color: white; color: #075e6f; border: transparent; padding: 10;")
        self.totalLengthLineEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.howLenghtValuesLayout.addWidget(self.totalLengthLineEdit, 4, 1, 1, 1)
        # ----------------------
        # 0, 2
        self.length1LineEdit = QLineEdit(self.showLenghtValuesWidget)
        self.length1LineEdit.setText("")
        self.length1LineEdit.setPlaceholderText("0")
        self.length1LineEdit.setFont(self.font.fonts["12"])
        self.length1LineEdit.setAlignment(Qt.AlignLeft)
        self.length1LineEdit.setStyleSheet("background-color: white; color: #075e6f; border: transparent; padding: 10;")
        self.length1LineEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.length1LineEdit.editingFinished.connect(self.onEditingFinished)
        self.sizePolicy.setHeightForWidth(self.length1LineEdit.sizePolicy().hasHeightForWidth())
        self.howLenghtValuesLayout.addWidget(self.length1LineEdit, 0, 2, 1, 3)
        # 1, 2
        self.length2LineEdit = QLineEdit(self.showLenghtValuesWidget)
        self.length2LineEdit.setText("")
        self.length2LineEdit.setPlaceholderText("0")
        self.length2LineEdit.setFont(self.font.fonts["12"])
        self.length2LineEdit.setAlignment(Qt.AlignLeft)
        self.length2LineEdit.setStyleSheet("background-color: white; color: #075e6f; border: transparent; padding: 10;")
        self.length2LineEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.length2LineEdit.editingFinished.connect(self.onEditingFinished)
        self.sizePolicy.setHeightForWidth(self.length2LineEdit.sizePolicy().hasHeightForWidth())
        self.howLenghtValuesLayout.addWidget(self.length2LineEdit, 1, 2, 1, 3)
        # 2, 2
        self.length3LineEdit = QLineEdit(self.showLenghtValuesWidget)
        self.length3LineEdit.setText("")
        self.length3LineEdit.setPlaceholderText("0")
        self.length3LineEdit.setFont(self.font.fonts["12"])
        self.length3LineEdit.setAlignment(Qt.AlignLeft)
        self.length3LineEdit.setStyleSheet("background-color: white; color: #075e6f; border: transparent; padding: 10;")
        self.length3LineEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.length3LineEdit.editingFinished.connect(self.onEditingFinished)
        self.sizePolicy.setHeightForWidth(self.length3LineEdit.sizePolicy().hasHeightForWidth())
        self.howLenghtValuesLayout.addWidget(self.length3LineEdit, 2, 2, 1, 3)
        # 3, 2
        self.length4LineEdit = QLineEdit(self.showLenghtValuesWidget)
        self.length4LineEdit.setText("")
        self.length4LineEdit.setPlaceholderText("0")
        self.length4LineEdit.setFont(self.font.fonts["12"])
        self.length4LineEdit.setAlignment(Qt.AlignLeft)
        self.length4LineEdit.setStyleSheet("background-color: white; color: #075e6f; border: transparent; padding: 10;")
        self.length4LineEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.length4LineEdit.editingFinished.connect(self.onEditingFinished)
        self.sizePolicy.setHeightForWidth(self.length4LineEdit.sizePolicy().hasHeightForWidth())
        self.howLenghtValuesLayout.addWidget(self.length4LineEdit, 3, 2, 1, 3)
        # 4, 2
        self.totalMMLabel = QLabel(self.showLenghtValuesWidget)
        self.totalMMLabel.setText("mm")
        self.totalMMLabel.setFont(self.font.fonts["12"])
        self.totalMMLabel.setAlignment(Qt.AlignLeft)
        self.totalMMLabel.setStyleSheet("background-color: transparent; color: #075e6f; border: transparent; padding: 10;")
        self.totalMMLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.howLenghtValuesLayout.addWidget(self.totalMMLabel, 4, 2, 1, 1)
        # ----------------------
        # 4, 3
        self.designDateLabel = QLabel(self.showLenghtValuesWidget)
        self.designDateLabel.setText("Design date")
        self.designDateLabel.setFont(self.font.fonts["12"])
        self.designDateLabel.setAlignment(Qt.AlignRight)
        self.designDateLabel.setStyleSheet("background-color: transparent; color: #075e6f; border: transparent; padding: 10;")
        self.designDateLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.howLenghtValuesLayout.addWidget(self.designDateLabel, 4, 3, 1, 1)
        # ----------------------
        # 4, 4
        self.designDateComboBox = QComboBox(self.showLenghtValuesWidget)
        self.designDateComboBox.setFont(self.font.fonts["12"])
        self.designDateComboBox.setStyleSheet("""QComboBox{ background-color: white; padding-left: 15px }
                                            QComboBox:QAbstractItemView{ background-color: white; color:orange; padding-left: 15px }""")
        self.designDateComboBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.reloadCombobox(self.designDateComboBox, ["0"])
        self.sizePolicy.setHeightForWidth(self.designDateComboBox.sizePolicy().hasHeightForWidth())
        self.howLenghtValuesLayout.addWidget(self.designDateComboBox, 4, 4, 1, 1)
        # ----------------------
        # 0, 5
        self.mmLabel1 = QLabel(self.showLenghtValuesWidget)
        self.mmLabel1.setText("mm")
        self.mmLabel1.setFont(self.font.fonts["12"])
        self.mmLabel1.setAlignment(Qt.AlignLeft)
        self.mmLabel1.setStyleSheet("background-color: transparent; color: #075e6f; border: transparent; padding: 10;")
        self.mmLabel1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.howLenghtValuesLayout.addWidget(self.mmLabel1, 0, 5, 1, 1)
        # 1, 5
        self.mmLabel2 = QLabel(self.showLenghtValuesWidget)
        self.mmLabel2.setText("mm")
        self.mmLabel2.setFont(self.font.fonts["12"])
        self.mmLabel2.setAlignment(Qt.AlignLeft)
        self.mmLabel2.setStyleSheet("background-color: transparent; color: #075e6f; border: transparent; padding: 10;")
        self.mmLabel2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.howLenghtValuesLayout.addWidget(self.mmLabel2, 1, 5, 1, 1)
        # 2, 5
        self.mmLabel3 = QLabel(self.showLenghtValuesWidget)
        self.mmLabel3.setText("mm")
        self.mmLabel3.setFont(self.font.fonts["12"])
        self.mmLabel3.setAlignment(Qt.AlignLeft)
        self.mmLabel3.setStyleSheet("background-color: transparent; color: #075e6f; border: transparent; padding: 10;")
        self.mmLabel3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.howLenghtValuesLayout.addWidget(self.mmLabel3, 2, 5, 1, 1)
        # 3, 5
        self.mmLabel4 = QLabel(self.showLenghtValuesWidget)
        self.mmLabel4.setText("mm")
        self.mmLabel4.setFont(self.font.fonts["12"])
        self.mmLabel4.setAlignment(Qt.AlignLeft)
        self.mmLabel4.setStyleSheet("background-color: transparent; color: #075e6f; border: transparent; padding: 10;")
        self.mmLabel4.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.howLenghtValuesLayout.addWidget(self.mmLabel4, 3, 5, 1, 1)
        # ----------------------
        # 5, 6
        self.howLenghtValuesLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding), 5, 6, 1, 1)
        # Stretch
        self.howLenghtValuesLayout.setRowStretch(0, 1)
        self.howLenghtValuesLayout.setRowStretch(1, 1)
        self.howLenghtValuesLayout.setRowStretch(2, 1)
        self.howLenghtValuesLayout.setRowStretch(3, 1)
        self.howLenghtValuesLayout.setRowStretch(4, 1)
        self.howLenghtValuesLayout.setRowStretch(5, 3)
        self.howLenghtValuesLayout.setColumnStretch(0, 2)
        self.howLenghtValuesLayout.setColumnStretch(1, 6)
        self.howLenghtValuesLayout.setColumnStretch(2, 1)
        self.howLenghtValuesLayout.setColumnStretch(3, 1)
        self.howLenghtValuesLayout.setColumnStretch(4, 8)
        self.howLenghtValuesLayout.setColumnStretch(5, 1)
        self.howLenghtValuesLayout.setColumnStretch(6, 3)
        self.showLenghtValuesWidget.setLayout(self.howLenghtValuesLayout)

    def reloadCombobox(self, comboBox, listValues):
        comboBox.clear()
        for item in listValues:
            comboBox.addItem(item)

    def onEditingFinished(self):
        try:
            lenght1 = int("0" if self.length1LineEdit.text()=="" else self.length1LineEdit.text())
            lenght2 = int("0" if self.length2LineEdit.text()=="" else self.length2LineEdit.text())
            lenght3 = int("0" if self.length3LineEdit.text()=="" else self.length3LineEdit.text())
            lenght4 = int("0" if self.length4LineEdit.text()=="" else self.length4LineEdit.text())
            self.totalLengthLineEdit.setText(str(lenght1 + lenght2 + lenght3 + lenght4))
        except ValueError as e:
            self.totalLengthLineEdit.setText("0")
