# -*- coding: utf-8 -*-

import shutil
from pyndf.qtlib import QtWidgets, QtCore
from pyndf.logbook import Logger
from pyndf.process.thread import Thread
from pyndf.constants import COMPANY, TITLE_APP, TAB_PRO, TAB_ANA, TAB_RW
from pyndf.gui.tabs.analyse import AnalyseTab
from pyndf.gui.tabs.process import ProcessTab
from pyndf.gui.items.useclass.analyse.all import AllItem
from pyndf.gui.items.useclass.analyse.api import ApiItem
from pyndf.gui.items.useclass.analyse.pdf import PdfItem
from pyndf.gui.items.useclass.reader.excel import ExcelItem
from pyndf.gui.items.useclass.reader.csv import CsvItem
from pyndf.gui.menus.menu import MainMenu


class MainWindow(Logger, QtWidgets.QMainWindow):
    """Main window of the app"""

    def __init__(self, app, excel=None, csv=None, output=None, color=None, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.excel = excel
        self.csv = csv
        self.output = output
        self.color = color

        # Window parameters
        self.setWindowTitle(TITLE_APP)
        self.setWindowIcon(self.style().standardIcon(self.style().StandardPixmap.SP_TitleBarMenuButton))
        if app.resolution:
            self.setMinimumWidth(int(app.resolution.width() / 1.5))
            self.setMinimumHeight(int(app.resolution.height() / 3))

        self.read_settings()

        # Initialisation attributes
        self.threadpool = QtCore.QThreadPool()

        # Tabs
        self.tabs = {}
        self._create_tabs()

        # Menu bar
        self.setMenuWidget(MainMenu(self))

        # Progress Bar in status bar
        self.progress = QtWidgets.QProgressBar()
        self._create_status_bar()

    def set_path(self, name, path):
        self.tabs[TAB_PRO].texts[name].setText(path)

    def toggled_tab(self, tab, boolean):
        widget = self.centralWidget()
        widget.setTabVisible(widget.indexOf(tab), boolean)

    def change_language(self, language):
        self.app.language = language
        self.app.load_translator()
        self.app.load_window(self.excel, self.csv, self.output, self.color, log_level=self.log_level)

        self.deleteLater()

    def _create_tabs(self):
        widget = QtWidgets.QTabWidget()
        self.setCentralWidget(widget)

        # Analyse tabs
        self.tabs[TAB_ANA] = {}
        self.tabs[TAB_RW] = {}
        info_dict = {
            "excel": {"title": self.tr("Excel Reader"), "item": ExcelItem, "tab": TAB_RW},
            "csv": {"title": self.tr("CSV Reader"), "item": CsvItem, "tab": TAB_RW},
            "global": {"title": self.tr("Global Analyse"), "item": AllItem, "tab": TAB_ANA},
            "api": {"title": self.tr("Distance Google API Analyse"), "item": ApiItem, "tab": TAB_ANA},
            "pdf": {"title": self.tr("PDF Writer Analyse"), "item": PdfItem, "tab": TAB_ANA},
        }

        for index, (key, value) in enumerate(info_dict.items()):
            self.tabs[value["tab"]][key] = AnalyseTab(self, value["title"], value["item"])
            widget.insertTab(index + 1, self.tabs[value["tab"]][key], self.tabs[value["tab"]][key].title)

        # Process tab
        self.tabs[TAB_PRO] = ProcessTab(self, self.tr("Process"), excel=self.excel, csv=self.csv, output=self.output)
        widget.insertTab(0, self.tabs[TAB_PRO], self.tabs[TAB_PRO].title)

        widget.setCurrentIndex(0)

    def _create_status_bar(self):
        self.progress.hide()
        status_bar = QtWidgets.QStatusBar()
        status_bar.addPermanentWidget(self.progress, 0)
        self.setStatusBar(status_bar)

    def generate(self):
        """Method triggered with the button to start the generation of pdf. In process tab"""
        if not all([t.text() for t in self.tabs[TAB_PRO].texts.values()]):
            return None  # If one field is empty, ignore.

        self.progress.show()
        self.tabs[TAB_PRO].buttons["pdf"].setDisabled(True)
        for tab in list(self.tabs[TAB_ANA].values()) + list(self.tabs[TAB_RW].values()):
            tab.table.init()
        process = Thread(
            *[t.text() for t in self.tabs[TAB_PRO].texts.values()], color=self.color, log_level=self.log_level
        )
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
        elif isinstance(obj, ApiItem):
            self.tabs[TAB_ANA]["api"].table.add(obj)
        elif isinstance(obj, PdfItem):
            self.tabs[TAB_ANA]["pdf"].table.add(obj)
        elif isinstance(obj, ExcelItem):
            self.tabs[TAB_RW]["excel"].table.add(obj)
        elif isinstance(obj, CsvItem):
            self.tabs[TAB_RW]["csv"].table.add(obj)

    @QtCore.pyqtSlot(float, str)
    def progressed(self, value, text):
        if value <= 100:
            self.progress.setValue(int(value))
            self.statusBar().showMessage(text, 1000)

    # End methods
    def tear_down(self):
        self.progress.hide()
        self.progress.reset()
        for tab in list(self.tabs[TAB_ANA].values()) + list(self.tabs[TAB_RW].values()):
            tab.table.finished()
        self.tabs[TAB_PRO].buttons["pdf"].setDisabled(False)

    @QtCore.pyqtSlot(object)
    def error(self, obj):
        self.tear_down()
        QtWidgets.QMessageBox.critical(self, self.tr("Error"), self.tr("Error: {}").format(obj))

    @QtCore.pyqtSlot()
    def generated(self):
        """Success methdod"""
        self.tear_down()
        QtWidgets.QMessageBox.information(self, self.tr("Finished"), self.tr("PDFs have been generated !"))

    def read_settings(self):
        settings = QtCore.QSettings(COMPANY, TITLE_APP)
        geo = settings.value("geometry")
        if geo is not None:
            self.restoreGeometry(geo)

        state = settings.value("windowState")
        if state is not None:
            self.restoreState(state)

        for name in ("excel", "csv", "output", "color"):
            attr = settings.value(name)
            if attr is not None and getattr(self, name) is None:
                setattr(self, name, attr)

    def closeEvent(self, event):
        settings = QtCore.QSettings(COMPANY, TITLE_APP)
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState())

        # Remove temp directory
        shutil.rmtree(self.app.temp_dir, ignore_errors=True)

        # Memory
        for name in ("excel", "csv", "output", "color"):
            settings.setValue(name, getattr(self, name))
        super().closeEvent(event)
