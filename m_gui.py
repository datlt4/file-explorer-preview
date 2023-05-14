import os
import sys
from functools import partial
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QSpacerItem, QApplication, QSizePolicy, QWidget, QPushButton, QGridLayout, QStackedWidget, QListWidget
from PyQt5.QtGui import QPixmap
from gui import *
import m_db

# """ ========= AppWindow ========= """
class AppWindowSignals(QObject):
    signal = pyqtSignal()

class AppWindow(QMainWindow):
    def __init__(self, app):
        super(AppWindow, self).__init__()
        screen = app.primaryScreen()
        self.font = MFont()
        rect = screen.availableGeometry()
        self.title = "Open File **"
        self.l = 0
        if OS.startswith("win"):
            self.t = 30
        elif OS.startswith("linux"):
            self.t = 0
        elif OS.startswith("darwin"):
            self.t = 0
        else:
            sys.exit(1)
        self.w = rect.width()
        self.h = rect.height() - self.t
        # self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint);
        self.setWindowFlags(Qt.Window)
        # Init
        self.selectedFile = "/"

        self.quickAccessAddresses = m_db.read_db()
        self.initUI()
        self.initSignalConnection()
        self.closeEvent = self._closeEvent
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.l, self.t, self.w, self.h)
        self.homeWindowWidget = QWidget()
        self.homeWindowLayout = QHBoxLayout(self.homeWindowWidget)
        self.homeWindowWidget.setStyleSheet("border: 1px solid transparent;")
        # 0
        self.fileExplorerWidget = QWidget(self.homeWindowWidget)
        self.initFileExplorer()
        self.homeWindowLayout.addWidget(self.fileExplorerWidget, 0)
        # 1
        self.previewInfoWidget = QWidget(self.homeWindowWidget)
        self.initPreviewInfo()
        self.homeWindowLayout.addWidget(self.previewInfoWidget, 1)
        # Stretch
        self.homeWindowLayout.setStretch(0, 7)
        self.homeWindowLayout.setStretch(1, 4)
        self.homeWindowWidget.setLayout(self.homeWindowLayout)
        self.setCentralWidget(self.homeWindowWidget)

    def initFileExplorer(self):
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fileExplorerWidget.sizePolicy().hasHeightForWidth())
        self.fileExplorerWidget.setSizePolicy(sizePolicy)
        self.fileExplorerLayout = QGridLayout(self.fileExplorerWidget)
        # 0, 0
        self.whereToLookLabel = QLabel(self.fileExplorerWidget)
        self.whereToLookLabel.setText("Where to look")
        self.whereToLookLabel.setFont(self.font.fonts["14B"])
        self.whereToLookLabel.setAlignment(Qt.AlignRight)
        self.whereToLookLabel.setStyleSheet("background-color: transparent; color: #075e6f; border: transparent; padding: 10;")
        self.whereToLookLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.fileExplorerLayout.addWidget(self.whereToLookLabel, 0, 0, 1, 1)
        # 0, 1
        self.whereToLookControlWidget = WhereToLookControlWidget(QWidget(self.fileExplorerWidget), self.font)
        self.fileExplorerLayout.addWidget(self.whereToLookControlWidget.whereToLookControlWidget, 0, 1, 1, 1)
        # 1, 0
        self.quickAccessWidget = QuickAccessWidget(QWidget(self.fileExplorerWidget), self.font, self.quickAccessAddresses, self.w, self.h)
        self.fileExplorerLayout.addWidget(self.quickAccessWidget.quickAccessWidget, 1, 0, 1, 1)
        # 1, 1
        self.listAllFileDirWidget = TreeViewFileSystemWidget(QWidget(self.fileExplorerWidget), self.font, self.w, self.h)
        self.fileExplorerLayout.addWidget(self.listAllFileDirWidget.treeViewFileSystemWidget, 1, 1, 1, 1)
        # 2, 0
        self.fileExplorerLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding), 2, 0, 1, 1)
        # 2, 1
        self.nameTypeFilterWidget = NameTypeFilterWidget(QWidget(self.fileExplorerWidget), self.font)
        self.fileExplorerLayout.addWidget(self.nameTypeFilterWidget.nameTypeFilterWidget, 2, 1, 1, 1)
        # Stretch
        self.fileExplorerLayout.setRowStretch(0, 1)
        self.fileExplorerLayout.setRowStretch(1, 20)
        self.fileExplorerLayout.setRowStretch(2, 3)
        self.fileExplorerLayout.setColumnStretch(0, 1)
        self.fileExplorerLayout.setColumnStretch(1, 7)
        self.fileExplorerWidget.setLayout(self.fileExplorerLayout)

    def initPreviewInfo(self):
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.previewInfoWidget.sizePolicy().hasHeightForWidth())
        self.previewInfoWidget.setSizePolicy(sizePolicy)
        self.previewInfoLayout = QVBoxLayout(self.previewInfoWidget)
        # 0
        self.favouriteLinkWidget = FavouriteLinkWidget(QWidget(self.previewInfoWidget), self.font)
        self.previewInfoLayout.addWidget(self.favouriteLinkWidget.favouriteLinkWidget, 0)
        # 1
        self.visualPreviewWidget = VisualPreviewWidget(QWidget(self.previewInfoWidget), self.font, self.w, self.h)
        self.previewInfoLayout.addWidget(self.visualPreviewWidget.visualPreviewWidget, 1)
        # 2
        self.lenghtInfoWidget = ShowLenghtValuesWidget(QWidget(self.previewInfoWidget), self.font)
        self.previewInfoLayout.addWidget(self.lenghtInfoWidget.showLenghtValuesWidget, 2)
        # 3
        self.previewInfoLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))
        # Stretch
        self.previewInfoLayout.setStretch(0, 1)
        self.previewInfoLayout.setStretch(1, 12)
        self.previewInfoLayout.setStretch(2, 7)
        self.previewInfoLayout.setStretch(3, 4)
        self.previewInfoWidget.setLayout(self.previewInfoLayout)

    def initSignalConnection(self):
        # Signals connections
        self.listAllFileDirWidget.signals.signal_send_clicked_path.connect(self.onClickedFile)
        self.nameTypeFilterWidget.signals.signal_close_application.connect(lambda: QCoreApplication.exit(0))
        self.nameTypeFilterWidget.signals.signal_update_type_filter.connect(self.onUpdateExtensionFilter)
        self.visualPreviewWidget.signals.signal_send_current_image.connect(self.onSendCurrentImage)
        self.whereToLookControlWidget.signals.signal_where_to_look.connect(lambda path: self.onSendCurrentImage(path))
        self.nameTypeFilterWidget.signals.signal_send_open_path.connect(lambda path: self.onSendCurrentImage(path))
        self.quickAccessWidget.signals.signal_send_quickaccess_address.connect(lambda path: self.onSendCurrentImage(path))
        self.whereToLookControlWidget.signals.signal_add_quick_access.connect(self.onAddNewQuickAccess)

    def onClickedFile(self, path):
        if os.path.exists(path):
            self.selectedFile = path
            self.nameTypeFilterWidget.signals.signal_set_name_line_edit.emit(self.selectedFile)
            self.whereToLookControlWidget.reloadWhereToLookCombobox(self.selectedFile)
            self.visualPreviewWidget.updateListFiles(self.selectedFile)

    def onUpdateExtensionFilter(self, filter):
        self.visualPreviewWidget.updateListFiles(self.selectedFile, filter)

    def onSendCurrentImage(self, path):
        if path != "":
            file_index = self.listAllFileDirWidget.model.index(path)
            self.listAllFileDirWidget.treeView.setCurrentIndex(file_index)
            self.selectedFile = path
            self.nameTypeFilterWidget.signals.signal_set_name_line_edit.emit(self.selectedFile)
            self.whereToLookControlWidget.reloadWhereToLookCombobox(self.selectedFile)
            if os.path.isdir(self.selectedFile):
                self.visualPreviewWidget.updateListFiles(self.selectedFile)

    def onAddNewQuickAccess(self, text):
        path = text if (os.path.isdir(text)) else os.path.dirname(text)
        self.quickAccessAddresses.append(path)
        m_db.write_db(self.quickAccessAddresses)
        self.quickAccessWidget.reload(self.quickAccessAddresses)

    def _closeEvent(self, event):
        pass

if __name__ == "__main__":
    stylesheet = """
        AppWindow {
            background-image: url(image/contour-dark-blue-lines-white.jpg);
            background-repeat: no-repeat;
            background-position: center;
        }
    """

    app = QApplication(sys.argv)
    app.aboutToQuit.connect(lambda: print("__Application exited__"))
    app.setStyleSheet(stylesheet)
    window = AppWindow(app)
    # window.showFullScreen()
    window.showMaximized()
    sys.exit(app.exec_())
