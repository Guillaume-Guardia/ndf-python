# -*- coding: utf-8 -*-

import shutil
import json
from pyndf.gui.widgets.control import ControlButtons
from pyndf.qtlib import QtWidgets, QtCore
from pyndf.logbook import Logger
from pyndf.process.thread import NdfProcess
from pyndf.constants import CONST
from pyndf.gui.tabs.useclass.analyse import AnalyseTab
from pyndf.gui.tabs.useclass.process import ProcessTab
from pyndf.gui.items.factory import Items
from pyndf.gui.menus.menu import MainMenu
from pyndf.utils import Utils


class MainWindow(Logger, QtWidgets.QMainWindow):
    """Main window of the app"""

    def __init__(self, app, excel=None, csv=None, output=None, color=None, use_db=None, use_cache=None, **kwargs):
        super().__init__(**kwargs)
        self.app = app

        # Selection files + directory
        self.excel = []
        if excel:
            self.excel.append(excel)

        self.csv = []
        if csv:
            self.csv.append(csv)

        self.output = []
        if output:
            self.output.append(output)

        # Api parameters
        self.use_db = use_db
        self.use_cache = use_cache
        self.use_api = True

        # Pdf parameters
        self.color = color or CONST.WRITER.PDF.COLOR

        # Window parameters
        self.setWindowTitle(CONST.TITLE_APP)
        self.setWindowIcon(self.style().standardIcon(self.style().StandardPixmap.SP_TitleBarMenuButton))
        if app.resolution:
            self.setMinimumWidth(int(app.resolution.width() / 1.5))
            self.setMinimumHeight(int(app.resolution.height() / 3))

        self.read_settings()

        # Process parameters
        self.moving_tab = False
        self.process = None

        # Tabs
        self.controller_tab = QtWidgets.QTabWidget()
        self.setCentralWidget(self.controller_tab)
        self.tabs = {}
        self._create_tabs()

        # Menu bar
        self.setMenuWidget(MainMenu(self))

        # Progress Bar in status bar
        self.control_buttons = ControlButtons(self)
        self.progress = QtWidgets.QProgressBar()
        self._create_status_bar()

    def set_path(self, name, path):
        """Set new path from the temp directory -> modification ask.

        Args:
            name (str): type of file
            path (str): path of temp file
        """
        self.tabs[CONST.TYPE.PRO].texts[name].setCurrentText(path)

    def toggled_tab(self, tab, boolean):
        index = self.controller_tab.indexOf(tab)
        self.controller_tab.setTabVisible(index, boolean)

    def change_language(self, language):
        self.app.language = language
        self.app.load_translator()
        self.app.load_window(self.excel, self.csv, self.output, self.color, log_level=self.log_level)

        self.deleteLater()

    def _create_tabs(self):
        # Analyse tabs
        info_dict = {
            CONST.TYPE.EXC: self.tr("EXCEL"),
            CONST.TYPE.CSV: self.tr("CSV"),
            CONST.TYPE.ALL: self.tr("Global Analyse"),
            CONST.TYPE.API: self.tr("Google API Analyse"),
            CONST.TYPE.PDF: self.tr("PDF files Analyse"),
            CONST.TYPE.DB_CLIENT: self.tr("Database Client"),
            CONST.TYPE.DB_EMPLOYEE: self.tr("Database Employee"),
            CONST.TYPE.DB_MEASURE: self.tr("Database Measure"),
        }

        for index, (key, title) in enumerate(info_dict.items()):
            self.tabs[key] = AnalyseTab(self, title, Items(key))
            index = self.controller_tab.insertTab(index + 1, self.tabs[key], title)
            self.controller_tab.setTabVisible(index, False)

        # Process tab
        title = self.tr("Process")
        self.tabs[CONST.TYPE.PRO] = ProcessTab(self, title, excel=self.excel, csv=self.csv, output=self.output)
        self.controller_tab.insertTab(0, self.tabs[CONST.TYPE.PRO], title)
        self.controller_tab.setCurrentIndex(0)

    def _create_status_bar(self):
        status_bar = QtWidgets.QStatusBar()
        status_bar.addPermanentWidget(self.control_buttons)
        status_bar.addPermanentWidget(self.progress)
        status_bar.hide()
        self.setStatusBar(status_bar)

    def generate(self):
        """Method triggered with the button to start the generation of pdf. In process tab"""
        parameters = [t.currentText() for t in self.tabs[CONST.TYPE.PRO].texts.values()]
        if not all(parameters):
            return None  # If one field is empty, ignore.

        self.statusBar().show()

        self.tabs[CONST.TYPE.PRO].buttons[CONST.TYPE.PDF].setDisabled(True)
        for name in CONST.TAB.ANALYSE + CONST.TAB.READER:
            self.tabs[name].table.init()

        self.process = NdfProcess(
            *parameters,
            color=self.color,
            log_level=self.log_level,
            use_db=self.use_db,
            use_cache=self.use_cache,
            use_api=self.use_api,
        )
        self.process.signals.error.connect(self.error)
        self.process.signals.finished.connect(self.generated)
        self.process.signals.progressed.connect(self.progressed)
        self.process.signals.analysed.connect(self.analysed)
        self.process.signals.cancelled.connect(self.cancelled)
        self.process.start()

        return True

    # End methods
    def tear_down(self):
        """Hide the status bar, reset the progress bar, show the table tabs, add the total in each table. Reactivation of the start button."""
        self.statusBar().hide()
        self.progress.reset()
        for name in CONST.TAB.ANALYSE + CONST.TAB.READER:
            self.tabs[name].table.finished()
        self.tabs[CONST.TYPE.PRO].buttons[CONST.TYPE.PDF].setDisabled(False)
        self.process = None

    @QtCore.pyqtSlot()
    def cancelled(self):
        """Slot method which is connected to tear_down method."""
        self.tear_down()

    @QtCore.pyqtSlot(object)
    def analysed(self, obj):
        """Slot method which send the obj row to the good table.

        Args:
            obj (row): row to print in table.
        """
        self.toggled_tab(self.tabs[obj.type], True)
        if self.moving_tab and self.controller_tab.currentWidget != self.tabs[obj.type]:
            self.controller_tab.setCurrentWidget(self.tabs[obj.type])
        self.tabs[obj.type].table.add(obj)

    @QtCore.pyqtSlot(float, str)
    def progressed(self, value, text):
        """Slot method which show the evolution of thread via progress bar and message.

        Args:
            value (int): 0 -> 100
            text (str): message printed
        """
        if value <= 100:
            self.progress.setValue(int(value))
            self.statusBar().showMessage(text, 3000)

    @QtCore.pyqtSlot(object)
    def error(self, obj):
        """Slot method which pop up a message of error

        Args:
            obj (Exception): Exception to print
        """
        self.tear_down()
        QtWidgets.QMessageBox.critical(self, self.tr("Error"), self.tr("Error: {}").format(obj))

    @QtCore.pyqtSlot()
    def generated(self):
        """Success methdod"""
        self.tear_down()
        QtWidgets.QMessageBox.information(self, self.tr("Finished"), self.tr("The PDF files have been generated!"))

    def read_settings(self):
        """Read the settings store in PC"""
        settings = QtCore.QSettings(CONST.COMPANY, CONST.TITLE_APP)
        geo = settings.value("geometry")
        if geo is not None:
            self.restoreGeometry(geo)

        state = settings.value("windowState")
        if state is not None:
            self.restoreState(state)

        for name in CONST.MEMORY:
            attr = json.loads(settings.value(name))
            if attr is None:
                continue

            if getattr(self, name) is None:
                setattr(self, name, attr)

            elif isinstance(getattr(self, name), list):
                getattr(self, name).extend(attr)

    def closeEvent(self, event):
        """Qt method

        Args:
            event (Qt.event):
        """
        # Cancel processing
        self.control_buttons.cancel()

        # Save geometry of window
        settings = QtCore.QSettings(CONST.COMPANY, CONST.TITLE_APP)
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState())

        # Remove temp directory
        shutil.rmtree(self.app.temp_dir, ignore_errors=True)

        # Memory
        for name in CONST.MEMORY:
            settings.setValue(name, json.dumps(getattr(self, name)))

        self.app.set_language_mem()
        super().closeEvent(event)
