# -*- coding: utf-8 -*-

from pyndf.qtlib import QtWidgets, QtCore, QtGui
from pyndf.logbook import Logger
from pyndf.process.thread import Thread
from pyndf.constants import COMPANY, TITLE_APP, TAB_PRO, TAB_ANA
from pyndf.gui.tabs.analyse import AnalyseTab
from pyndf.gui.tabs.process import ProcessTab
from pyndf.gui.items.analyse.all_item import AllItem
from pyndf.gui.items.analyse.api_item import APIItem
from pyndf.gui.items.analyse.pdf_item import PDFItem
from pyndf.gui.items.reader.excel_item import ExcelItem
from pyndf.gui.items.reader.csv_item import CSVItem


class MainWindow(Logger, QtWidgets.QMainWindow):
    """Main window of the app"""

    def __init__(self, app, excel=None, csv=None, output=None, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.excel = excel
        self.csv = csv
        self.output = output

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
        self._create_menu_bar()

        # Progress Bar in status bar
        self.progress = QtWidgets.QProgressBar()
        self._create_status_bar()

    def _create_menu_bar(self):
        menu = self.menuBar()

        # file
        file = menu.addMenu(self.tr("File"))

        # Select language
        language = menu.addMenu(self.tr("Select language"))

        for lang in self.app.language_available:
            language.addAction(lang, lambda l=lang: self.change_language(l))

        file.addSeparator()
        exit_action = QtGui.QAction(self.tr("Exit"), menu)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file.addAction(exit_action)

        # views
        views = menu.addMenu(self.tr("Views"))
        for tab in [self.tabs[TAB_PRO]] + list(self.tabs[TAB_ANA].values()):
            new_action = QtGui.QAction(tab.title, views)
            new_action.setCheckable(True)
            new_action.setChecked(True)
            new_action.toggled.connect(lambda boolean, tab_=tab: self.toggled_tab(tab_, boolean))
            views.addAction(new_action)

        # Help
        help = menu.addMenu(self.tr("Help"))
        action = QtGui.QAction(
            self.style().standardIcon(self.style().StandardPixmap.SP_MessageBoxQuestion), "Help", help
        )
        action.triggered.connect(self.open_help)

        self.setMenuWidget(menu)

    def toggled_tab(self, tab, boolean):
        widget = self.centralWidget()
        widget.setTabVisible(tab.index, boolean)

    def change_language(self, language):
        self.app.language = language
        self.app.load_translator()
        self.app.window = MainWindow(self.app, self.excel, self.csv, self.output, log_level=self.log_level)

        # self.blockSignals(True)
        self.deleteLater()

    def _create_tabs(self):
        widget = QtWidgets.QTabWidget()
        self.setCentralWidget(widget)

        # Process tab
        self.tabs[TAB_PRO] = ProcessTab(self, self.tr("Process"), excel=self.excel, csv=self.csv, output=self.output)
        self.tabs[TAB_PRO].index = widget.addTab(self.tabs[TAB_PRO], self.tabs[TAB_PRO].title)

        # Analyse tabs
        self.tabs[TAB_ANA] = {}
        info_dict = {
            "global": {"title": self.tr("Global Analyse"), "item": AllItem},
            "api": {"title": self.tr("Distance Google API Analyse"), "item": APIItem},
            "pdf": {"title": self.tr("PDF Writer Analyse"), "item": PDFItem},
            "excel": {"title": self.tr("Excel Reader"), "item": ExcelItem},
            "csv": {"title": self.tr("CSV Reader"), "item": CSVItem},
        }

        for key, value in info_dict.items():
            self.tabs[TAB_ANA][key] = AnalyseTab(self, value["title"], value["item"])
            self.tabs[TAB_ANA][key].index = widget.addTab(self.tabs[TAB_ANA][key], self.tabs[TAB_ANA][key].title)

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
        process = Thread(*[t.text() for t in self.tabs[TAB_PRO].texts.values()], log_level=self.log_level)
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
        elif isinstance(obj, ExcelItem):
            self.tabs[TAB_ANA]["excel"].table.add(obj)
        elif isinstance(obj, CSVItem):
            self.tabs[TAB_ANA]["csv"].table.add(obj)

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
        if geo is not None:
            self.restoreGeometry(geo)

        state = settings.value("windowState")
        if state is not None:
            self.restoreState(state)

        for name in ("excel", "csv", "output"):
            attr = settings.value(name)
            if attr is not None and getattr(self, name) is None:
                setattr(self, name, attr)

    def closeEvent(self, event):
        settings = QtCore.QSettings(COMPANY, TITLE_APP)
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState())

        # Memory
        for name in ("excel", "csv", "output"):
            settings.setValue(name, getattr(self, name))
        super().closeEvent(event)
