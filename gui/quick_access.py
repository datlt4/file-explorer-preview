import os
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QSize
from PyQt5.QtWidgets import QLabel, QSizePolicy, QWidget, QVBoxLayout, QListWidgetItem, QListWidget, QPushButton, QAction, QMenu
from PyQt5.QtGui import QIcon

class QuickAccessItemSignals(QObject):
    signal_send_quickaccess_address = pyqtSignal(str)
    signal_remove_quickaccess = pyqtSignal(list)

class QuickAccessItem(QListWidgetItem):
    def __init__(self, listWidget, font, address, desktop_w, desktop_h, idx):
        super(QuickAccessItem, self).__init__()
        self.idx = idx
        self.address = address
        self.font = font
        self.desktop_w = desktop_w
        self.desktop_h = desktop_h
        self.listWidget = listWidget
        self.signals = QuickAccessItemSignals()
        self.item = QListWidgetItem()
        self.widget = QWidget()
        self.widgetLayout = QVBoxLayout(self.widget)
        self.widget.setStyleSheet("background-color: transparent; border: red; border-radius: 3;")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        # 0
        self.button = QPushButton(self.widget)
        self.icon = QIcon("./image/green-folder.png")
        self.button.setIcon(self.icon)
        self.button.setIconSize(QSize(int(min(self.desktop_w, self.desktop_w) / 22), int(min(self.desktop_w, self.desktop_w) / 20)))
        # self.button.setText(os.path.basename(self.address))
        self.button.clicked.connect(lambda: self.signals.signal_send_quickaccess_address.emit(self.address))
        self.widgetLayout.addWidget(self.button)
        # 0
        self.label = QLabel(self.widget)
        self.label.setText(os.path.basename(self.address))
        self.label.setFont(self.font.fonts["10"])
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("background-color: transparent; color: #075e6f; border: transparent; padding: 10;")
        self.widgetLayout.addWidget(self.label)
        # Stretch
        self.widgetLayout.setStretch(0, 3)
        self.widgetLayout.setStretch(0, 1)
        self.widget.setLayout(self.widgetLayout)
        self.item.setSizeHint(self.widget.sizeHint())
        # Create a right-click menu with a remove action
        self.menu = QMenu(self.widget)
        self.menu.setStyleSheet("""
                                QMenu::item:unselected { background-color: white; color: #404040; }
                                QMenu::item:selected { background-color: #99FDC3; color: #075e6f; }
                                QMenu::item:selected:!active { background-color: #99FDC3; color: #075e6f; }
                                """)
        self.menu.setFont(self.font.fonts["10"])
        self.removeAction = QAction("Remove", self.widget)
        self.removeAction.triggered.connect(self.onRemoveAction)
        # self.menu.addAction(self.removeAction)
        # Connect the context menu event handler function to the customContextMenuRequested signal
        self.widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.widget.customContextMenuRequested.connect(self.showContextMenu)

    def get_address(self):
        return self.address

    def insert(self, top=True):
        if top:
            self.listWidget.insertItem(0, self.item)
            self.widgetItem = self.listWidget.item(0)
        else:
            self.listWidget.addItem(self.item)
            self.widgetItem = self.listWidget.item(self.listWidget.count() - 1)
        self.listWidget.setItemWidget(self.item, self.widget)

    def onRemoveAction(self):
        # row = self.listWidget.row(self.widgetItem)
        # self.listWidget.takeItem(row)
        self.signals.signal_remove_quickaccess.emit([self.idx, self.address])
        # self.menu.close()

    def showContextMenu(self, pos):
        self.menu.exec_(self.widget.mapToGlobal(pos))

class QuickAccessWidgetSignals(QObject):
    signal_send_quickaccess_address = pyqtSignal(str)
    signal_remove_quickaccess = pyqtSignal(list)

class QuickAccessWidget(QWidget):
    def __init__(self, quickAccessWidget, font, quickAccessAddresses, desktop_w, desktop_h):
        super(QuickAccessWidget, self).__init__()
        # Policy
        self.sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.sizePolicy.setHorizontalStretch(0)
        self.sizePolicy.setVerticalStretch(0)
        self.sizePolicy.setHeightForWidth(quickAccessWidget.sizePolicy().hasHeightForWidth())
        self.desktop_w = desktop_w
        self.desktop_h = desktop_h
        # Layout, signal
        self.quickAccessWidget = quickAccessWidget
        self.quickAccessLayout = QVBoxLayout(self.quickAccessWidget)
        self.font = font
        self.signals = QuickAccessWidgetSignals()
        # 0
        self.quickAccessListWidget = QListWidget(self.quickAccessWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.quickAccessListWidget.sizePolicy().hasHeightForWidth())
        self.quickAccessListWidget.setSizePolicy(sizePolicy)
        self.quickAccessListWidget.setStyleSheet("background-color: transparent; color: transparent; border: transparent; border-radius: 0px;")
        self.quickAccessLayout.addWidget(self.quickAccessListWidget)
        # set layout
        self.quickAccessWidget.setLayout(self.quickAccessLayout)
        # Other
        self.quickAccessListItems = []
        self.reload(quickAccessAddresses)

    def addNew(self, address, idx):
        item = QuickAccessItem(self.quickAccessListWidget, self.font, address, self.desktop_w, self.desktop_h, idx)
        item.signals.signal_send_quickaccess_address.connect(lambda path: self.signals.signal_send_quickaccess_address.emit(path))
        item.signals.signal_remove_quickaccess.connect(lambda item: self.signals.signal_remove_quickaccess.emit(item))
        item.insert(top=False)
        self.quickAccessListItems.append(item)

    def reload(self, quickAccess):
        for i in range(len(self.quickAccessListItems) - 1, -1 , -1):
            del(self.quickAccessListItems[i])
        self.quickAccessListWidget.clear()
        self.quickAccessListItems.clear()
        for idx, address in enumerate(quickAccess):
            self.addNew(address, idx)

