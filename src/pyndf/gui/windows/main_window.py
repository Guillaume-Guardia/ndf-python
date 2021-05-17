# -*- coding: utf-8 -*-

from pyndf.qtlib import QtWidgets, QtCore, QtGui
from pyndf.logbook import Logger
from pyndf.process.thread import Thread
from pyndf.constants import COMPANY, TITLE_APP, TAB_PRO, TAB_ANA
from pyndf.gui.tabs.analyse import AnalyseTab
from pyndf.gui.tabs.process import ProcessTab
from pyndf.gui.items.all_item import AllItem
from pyndf.gui.items.api_item import APIItem
from pyndf.gui.items.pdf_item import PDFItem


class MainWindow(Logger, QtWidgets.QMainWindow):
    """Main window of the app"""

    def __init__(self, excel="", csv="", output="", resolution=None):
        super().__init__()

        # Window parameters
        self.setWindowTitle(TITLE_APP)
        self.setWindowIcon(self.style().standardIcon(self.style().StandardPixmap.SP_TitleBarMenuButton))
        if resolution:
            self.setMinimumWidth(int(resolution.width() / 1.5))
            self.setMinimumHeight(int(resolution.height() / 3))

        self.read_settings()

        # Initialisation attributes
        self.threadpool = QtCore.QThreadPool()

        # Menu bar
        self._create_menu_bar()

        # Tabs
        self.tabs = {}
        self._create_tabs(excel, csv, output)

        # Progress Bar in status bar
        self.progress = QtWidgets.QProgressBar()
        self._create_status_bar()

        self.ctrl_enabled = False

    def _create_menu_bar(self):
        menu = self.menuBar()

        # file
        file = menu.addMenu(self.tr("File"))

        # Select language
        menu.addAction(self.tr("Select language"), self.change_language)

        file.addSeparator()
        exit_action = QtGui.QAction(self.tr("Exit"), menu)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file.addAction(exit_action)

        # views
        views = menu.addMenu(self.tr("Views"))

        # Help
        action = QtGui.QAction(
            self.style().standardIcon(self.style().StandardPixmap.SP_MessageBoxQuestion), "Help", menu
        )
        action.triggered.connect(self.open_help)

        self.setMenuWidget(menu)

    def change_language(self):
        self.log.info("language change")

    def _create_tabs(self, excel, csv, output):
        widget = QtWidgets.QTabWidget()
        self.setCentralWidget(widget)

        # Process tab
        self.tabs[TAB_PRO] = ProcessTab(self, excel=excel, csv=csv, output=output)
        widget.addTab(self.tabs[TAB_PRO], self.tr("Process"))

        # Analyse tabs
        self.tabs[TAB_ANA] = {}
        info_dict = {
            "global": {"title": self.tr("Global Analyse"), "item": AllItem},
            "api": {"title": self.tr("Distance Google API Analyse"), "item": APIItem},
            "pdf": {"title": self.tr("PDF Writer Analyse"), "item": PDFItem},
        }

        for key, value in info_dict.items():
            self.tabs[TAB_ANA][key] = AnalyseTab(self, value["item"])
            widget.addTab(self.tabs[TAB_ANA][key], value["title"])

    def _create_status_bar(self):
        self.progress.hide()
        status_bar = QtWidgets.QStatusBar()
        status_bar.addPermanentWidget(self.progress, 0)
        self.setStatusBar(status_bar)

    def open_help(self):
        self.log.info("Help open!")

    def generate(self):
        """Method triggered with the button to start the generation of pdf. In process tab"""
        if not all([t.text() for t in self.tabs[TAB_PRO].texts.values()]):
            return None  # If one field is empty, ignore.

        self.progress.show()
        self.tabs[TAB_PRO].buttons["generate"].setDisabled(True)
        for tab in self.tabs[TAB_ANA].values():
            tab.table.init()
        process = Thread(*[t.text() for t in self.tabs[TAB_PRO].texts.values()])
        process.signals.error.connect(self.error)
        process.signals.finished.connect(self.generated)
        process.signals.progressed.connect(self.progressed)
        process.signals.analysed.connect(self.analysed)
        self.threadpool.start(process)
        return True

    @QtCore.pyqtSlot(object)
    def analysed(self, obj):
        if isinstance(obj, AllItem):
            self.tabs[TAB_ANA]["global"].table.add(obj)
        elif isinstance(obj, APIItem):
            self.tabs[TAB_ANA]["api"].table.add(obj)
        elif isinstance(obj, PDFItem):
            self.tabs[TAB_ANA]["pdf"].table.add(obj)

    @QtCore.pyqtSlot(float, str)
    def progressed(self, value, text):
        if value <= 100:
            self.progress.setValue(int(value))
            self.statusBar().showMessage(text, 1000)

    # End methods
    def tear_down(self):
        self.progress.hide()
        self.progress.reset()
        for tab in self.tabs[TAB_ANA].values():
            tab.table.finished()
        self.tabs[TAB_PRO].buttons["generate"].setDisabled(False)

    @QtCore.pyqtSlot(object)
    def error(self, obj):
        self.tear_down()
        QtWidgets.QMessageBox.critical(self, self.tr("Error"), self.tr("Error: {}").format(obj))

    @QtCore.pyqtSlot(float)
    def generated(self, time):
        """Success methdod"""
        self.tear_down()
        QtWidgets.QMessageBox.information(self, self.tr("Finished"), self.tr("PDFs have been generated !"))

    def read_settings(self):
        settings = QtCore.QSettings(COMPANY, TITLE_APP)
        geo = settings.value("geometry")
        state = settings.value("windowState")
        if geo is not None:
            self.restoreGeometry(geo)
        if state is not None:
            self.restoreState(state)

    def closeEvent(self, event):
        settings = QtCore.QSettings(COMPANY, TITLE_APP)
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState())
        super().closeEvent(event)
