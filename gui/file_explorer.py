import os
import sys
import string
from functools import partial
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QFile, QIODevice, QModelIndex
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QSpacerItem, QComboBox, QSizePolicy, QWidget, QPushButton, QGridLayout, QStackedWidget, QFileDialog, QCheckBox, QLineEdit, QTreeView, QFileSystemModel, QHeaderView

class WhereToLookControlWidgetSignal(QObject):
    signal_where_to_look = pyqtSignal(str)
    signal_add_quick_access = pyqtSignal(str)
    signal_back = pyqtSignal(str)

class WhereToLookControlWidget(QWidget):
    def __init__(self, whereToLookControlWidget, font):
        super(WhereToLookControlWidget, self).__init__()
        # Policy
        self.sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.sizePolicy.setHorizontalStretch(0)
        self.sizePolicy.setVerticalStretch(0)
        self.sizePolicy.setHeightForWidth(whereToLookControlWidget.sizePolicy().hasHeightForWidth())
        # Layout, signal
        self.whereToLookControlWidget = whereToLookControlWidget
        self.whereToLookControlLayout = QHBoxLayout(self.whereToLookControlWidget)
        self.font = font
        self.signals = WhereToLookControlWidgetSignal()
        # 0        
        self.whereToLookComboBox = QComboBox(self.whereToLookControlWidget)
        self.whereToLookComboBox.setFont(self.font.fonts["12"])
        self.whereToLookComboBox.setStyleSheet("""QComboBox{ background-color: white; padding-left: 15px }
                                                QComboBox:QAbstractItemView{ background-color: white; color:orange; padding-left: 15px }""")
        self.whereToLookComboBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.whereToLookComboBox.activated[str].connect(self.onWhereToLook)
        self.reloadWhereToLookCombobox("")
        self.sizePolicy.setHeightForWidth(self.whereToLookComboBox.sizePolicy().hasHeightForWidth())
        self.whereToLookControlLayout.addWidget(self.whereToLookComboBox, 0)
        # # 1
        self.previousDirectoryButton = QPushButton(self.whereToLookControlWidget)
        self.previousDirectoryButton.setText("Back") # ("←")
        self.previousDirectoryButton.setFont(self.font.fonts["14"])
        self.previousDirectoryButton.setStyleSheet("""QPushButton{ background-color: #068170; color: #ffffff; border: transparent; padding: 5; border-radius: 5; }
                                                    QPushButton::pressed{ background-color: #088170; color: #ffffff; border: transparent; padding: 5; border-radius: 5; }
                                                    QPushButton::hover{ background-color: #229586; color: #ffffff; border: transparent; padding: 5; border-radius: 5; }""")
        self.previousDirectoryButton.clicked.connect(self.onBack)
        self.whereToLookControlLayout.addWidget(self.previousDirectoryButton, 1)
        # 2
        self.addQuickAccessButton = QPushButton(self.whereToLookControlWidget)
        self.addQuickAccessButton.setText("Add to QuickAccess")
        self.addQuickAccessButton.setFont(self.font.fonts["14"])
        self.addQuickAccessButton.setStyleSheet("""QPushButton{ background-color: #068170; color: #ffffff; border: transparent; padding: 5; border-radius: 5; }
                                                    QPushButton::pressed{ background-color: #088170; color: #ffffff; border: transparent; padding: 5; border-radius: 5; }
                                                    QPushButton::hover{ background-color: #229586; color: #ffffff; border: transparent; padding: 5; border-radius: 5; }""")
        self.addQuickAccessButton.clicked.connect(self.onAddQuickAccess)
        self.whereToLookControlLayout.addWidget(self.addQuickAccessButton, 1)
        # 3
        # self.whereToLookControlLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))
        # Stretch
        self.whereToLookControlLayout.setStretch(0, 1)
        self.whereToLookControlLayout.setStretch(1, 0)
        self.whereToLookControlLayout.setStretch(2, 0)
        # self.whereToLookControlLayout.setStretch(3, 20)
        self.whereToLookControlWidget.setLayout(self.whereToLookControlLayout)

    def reloadWhereToLookCombobox(self, path):
        self.whereToLookComboBox.clear()
        def listItemt(whereToLookComboBox, path):
            whereToLookComboBox.addItem(path)
            path_ = os.path.dirname(path)
            if path_ != path:
                listItemt(whereToLookComboBox, path_)

        listItemt(self.whereToLookComboBox, path)
        for letter in string.ascii_uppercase:
            if ((path == "") or (letter != path[0])) and (os.path.exists(f"{letter}:/")):
                self.whereToLookComboBox.addItem(f"{letter}:/")
        
    
    def onAddQuickAccess(self):
        self.signals.signal_add_quick_access.emit(self.whereToLookComboBox.currentText())

    def onWhereToLook(self, text):
        self.signals.signal_where_to_look.emit(text)
        
    def onBack(self):
        path = self.whereToLookComboBox.currentText()
        if os.path.isdir(path):
            _path = os.path.dirname(path)
        elif os.path.isfile(path):
            _path = os.path.dirname(os.path.dirname(path))
        else:
            _path = os.getcwd().replace("\\", "/")

        self.signals.signal_back.emit(os.getcwd().replace("\\", "/") if _path=="/" else _path)
        

class NameTypeFilterWidgetSignal(QObject):
    signal_type_filter = pyqtSignal(str)
    signal_set_name_line_edit = pyqtSignal(str)
    signal_update_type_filter = pyqtSignal(str)
    signal_close_application = pyqtSignal()
    signal_send_open_path = pyqtSignal(str)

class NameTypeFilterWidget(QWidget):
    def __init__(self, nameTypeFilterWidget, font):
        super(NameTypeFilterWidget, self).__init__()
        # Policy
        self.sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.sizePolicy.setHorizontalStretch(0)
        self.sizePolicy.setVerticalStretch(0)
        self.sizePolicy.setHeightForWidth(nameTypeFilterWidget.sizePolicy().hasHeightForWidth())
        # Layout, signal
        self.nameTypeFilterWidget = nameTypeFilterWidget
        self.nameTypeFilterLayout = QGridLayout(self.nameTypeFilterWidget)
        self.font = font
        self.signals = NameTypeFilterWidgetSignal()
        # 0, 0
        self.fileNameLabel = QLabel(self.nameTypeFilterWidget)
        self.fileNameLabel.setText("Name (N):")
        self.fileNameLabel.setFont(self.font.fonts["12"])
        self.fileNameLabel.setAlignment(Qt.AlignRight)
        self.fileNameLabel.setStyleSheet("background-color: transparent; color: #075e6f; border: transparent; padding: 10;")
        self.fileNameLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.nameTypeFilterLayout.addWidget(self.fileNameLabel, 0, 0, 1, 1)
        # 1, 0
        self.typeNameLabel = QLabel(self.nameTypeFilterWidget)
        self.typeNameLabel.setText("Type (T):")
        self.typeNameLabel.setFont(self.font.fonts["12"])
        self.typeNameLabel.setAlignment(Qt.AlignRight)
        self.typeNameLabel.setStyleSheet("background-color: transparent; color: #075e6f; border: transparent; padding: 10;")
        self.typeNameLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.nameTypeFilterLayout.addWidget(self.typeNameLabel, 1, 0, 1, 1)
        # 0, 1
        self.nameLineEdit = QLineEdit(self.nameTypeFilterWidget)
        self.nameLineEdit.setText("")
        self.nameLineEdit.setFont(self.font.fonts["12"])
        self.nameLineEdit.setAlignment(Qt.AlignLeft)
        self.nameLineEdit.setStyleSheet("background-color: white; color: #075e6f; border: transparent; padding: 10;")
        self.nameLineEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.nameTypeFilterLayout.addWidget(self.nameLineEdit, 0, 1, 1, 1)
        self.signals.signal_set_name_line_edit.connect(lambda val: self.nameLineEdit.setText(os.path.basename(val)))
        # 1, 1
        self.nameTypeFilterComboBox = QComboBox(self.nameTypeFilterWidget)
        self.nameTypeFilterComboBox.setFont(self.font.fonts["12"])
        self.nameTypeFilterComboBox.setStyleSheet("""QComboBox{ background-color: white; padding-left: 15px }
                                            QComboBox:QAbstractItemView{ background-color: white; color:orange; padding-left: 15px }""")
        self.nameTypeFilterComboBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.reloadCombobox(self.nameTypeFilterComboBox, ["Image (*.PNG, *.JPG)", "Drawing eXchange Format - CAD (*.DXF)"])
        self.sizePolicy.setHeightForWidth(self.nameTypeFilterComboBox.sizePolicy().hasHeightForWidth())
        self.nameTypeFilterLayout.addWidget(self.nameTypeFilterComboBox, 1, 1, 1, 1)
        self.nameTypeFilterComboBox.activated[str].connect(self.onnameTypeFilterActivated)
        # 0, 2
        self.nameTypeFilterLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))
        # 0, 3
        self.openButton = QPushButton(self.nameTypeFilterWidget)
        self.openButton.setText("Open")
        self.openButton.setFont(self.font.fonts["12"])
        self.openButton.setStyleSheet("""QPushButton{ background-color: #068170; color: #ffffff; border: transparent; padding: 5; border-radius: 10; }
                                    QPushButton::pressed{ background-color: #088170; color: #ffffff; border: transparent; padding: 5; border-radius: 10; }
                                    QPushButton::hover{ background-color: #229586; color: #ffffff; border: transparent; padding: 5; border-radius: 10; }""")
        self.openButton.clicked.connect(self.onOpenButton)
        self.nameTypeFilterLayout.addWidget(self.openButton, 0, 3, 1, 1)
        # 1, 3
        self.cancelButton = QPushButton(self.nameTypeFilterWidget)
        self.cancelButton.setText("Cancel")
        self.cancelButton.setFont(self.font.fonts["12"])
        self.cancelButton.setStyleSheet("""QPushButton{ background-color: #068170; color: #ffffff; border: transparent; padding: 5; border-radius: 10; }
                                    QPushButton::pressed{ background-color: #088170; color: #ffffff; border: transparent; padding: 5; border-radius: 10; }
                                    QPushButton::hover{ background-color: #229586; color: #ffffff; border: transparent; padding: 5; border-radius: 10; }""")
        self.cancelButton.clicked.connect(lambda: self.signals.signal_close_application.emit())
        self.nameTypeFilterLayout.addWidget(self.cancelButton, 1, 3, 1, 1)
        # Stretch
        self.nameTypeFilterLayout.setRowStretch(0, 1)
        self.nameTypeFilterLayout.setRowStretch(1, 1)
        self.nameTypeFilterLayout.setColumnStretch(0, 2)
        self.nameTypeFilterLayout.setColumnStretch(1, 7)
        self.nameTypeFilterLayout.setColumnStretch(2, 1)
        self.nameTypeFilterLayout.setColumnStretch(3, 2)
        self.nameTypeFilterWidget.setLayout(self.nameTypeFilterLayout)

    def reloadCombobox(self, comboBox, listValues):
        comboBox.clear()
        for item in listValues:
            comboBox.addItem(item)

    def onnameTypeFilterActivated(self, text):
        self.signals.signal_update_type_filter.emit(text)
        
    def onOpenButton(self):
        self.signals.signal_send_open_path.emit(self.nameLineEdit.text().replace("\\", "/"))

class TreeViewFileSystemWidgetSignal(QObject):
    signal_send_clicked_path = pyqtSignal(str)

class TreeViewFileSystemWidget(QWidget):
    def __init__(self, treeViewFileSystemWidget, font, desktop_w, desktop_h):
        super(TreeViewFileSystemWidget, self).__init__()
        self.desktop_w = desktop_w
        self.desktop_h = desktop_h
        # Policy
        self.sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.sizePolicy.setHorizontalStretch(0)
        self.sizePolicy.setVerticalStretch(0)
        self.sizePolicy.setHeightForWidth(treeViewFileSystemWidget.sizePolicy().hasHeightForWidth())
        # Layout, signal
        self.treeViewFileSystemWidget = treeViewFileSystemWidget
        self.treeViewFileSystemLayout = QGridLayout(self.treeViewFileSystemWidget)
        self.font = font
        self.signals = TreeViewFileSystemWidgetSignal()
        #
        self.treeView = QTreeView(self.treeViewFileSystemWidget)
        self.model = QFileSystemModel()
        self.treeView.setModel(self.model)
        header = self.treeView.header()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.treeView.clicked.connect(self.onTreeViewClicked)
        self.treeView.doubleClicked.connect(self.onTreeViewClicked)
        self.treeView.setExpandsOnDoubleClick(True) # Hide ">" button
        self.treeView.setRootIsDecorated(False)
        self.treeView.setIndentation(10)
        self.treeView.setAutoExpandDelay(-1)
        self.treeView.setAnimated(False)
        self.treeView.setUniformRowHeights(True)
        self.treeView.setSortingEnabled(True)
        self.setRootPath(os.getcwd().replace("\\", "/"))
        self.treeViewFileSystemLayout.addWidget(self.treeView, 0, 0, 1, 1)
        # Stretch
        self.treeViewFileSystemLayout.setRowStretch(0, 1)
        self.treeViewFileSystemLayout.setColumnStretch(0, 1)
        self.treeViewFileSystemWidget.setLayout(self.treeViewFileSystemLayout)

    def onTreeViewClicked(self, index: QModelIndex):
        path = self.model.filePath(index)
        # if os.path.isfile(path):
        if True:
            self.signals.signal_send_clicked_path.emit(path)

    def setRootPath(self, path):
        if os.path.isfile(path):
            path = os.path.dirname(path)

        self.model.setRootPath(path)
        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.model.index(path))
        # Collapse all expanded items
        self.treeView.collapseAll()

    def getCurrentIndex(self):
        current_index = self.treeView.currentIndex()
        current_path = self.model.filePath(current_index)
        return current_path
