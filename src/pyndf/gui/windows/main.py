# -*- coding: utf-8 -*-

import traceback
import shutil
import yaml
from pyndf.qtlib import QtWidgets, QtCore
from pyndf.logbook import Logger
from pyndf.constants import CONST
from pyndf.process.threads.ndf import NdfProcess
from pyndf.gui.widgets.control import ControlButtons
from pyndf.gui.tabs.useclass.analyse import AnalyseTab
from pyndf.gui.tabs.useclass.process import ProcessTab
from pyndf.gui.items.factory import Items
from pyndf.gui.menus.menu import MainMenu


class MainWindow(Logger, QtWidgets.QMainWindow):
    """Main window of the app"""

    def __init__(self, app, excel=None, csv=None, output=None, color=None, use_db=None, use_cache=None, **kwargs):
        super().__init__(**kwargs)
        self.app = app

        # Selection files + directory
        for name, value in (("excel", excel), ("csv", csv), ("output", output)):
            setattr(self, name, set())
            if value:
                try:
                    getattr(self, name).add(value)
                except TypeError:
                    getattr(self, name).update(value)

        # Reader parameters
        self.save_tmp_file = True

        # Api parameters
        self.use_db = use_db
        self.use_cache = use_cache
        self.use_api = True

        # Pdf parameters
        self.overwrite = True
        self.use_multithreading = True
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
        self.processes = []

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
        if self.save_tmp_file:
            getattr(self, name).add(path)

        self.tabs[CONST.TYPE.PRO].combos[name].add_item(path)

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
        self.tabs[CONST.TYPE.PRO] = ProcessTab(self, title)
        self.controller_tab.insertTab(0, self.tabs[CONST.TYPE.PRO], title)
        self.controller_tab.setCurrentIndex(0)

        # Analyse Global excel
        title = self.tr("Global analyse EXCEL file")
        self.tabs[CONST.TYPE.GLO_EXC] = AnalyseTab(self, title, Items(CONST.TYPE.EXC), read_only=True)
        index = self.controller_tab.addTab(self.tabs[CONST.TYPE.GLO_EXC], title)
        self.controller_tab.setTabVisible(index, False)

    def _create_status_bar(self):
        status_bar = QtWidgets.QStatusBar()
        status_bar.addPermanentWidget(self.control_buttons)
        status_bar.addPermanentWidget(self.progress)
        status_bar.hide()
        self.setStatusBar(status_bar)

    def generate(self, **kwargs):
        """Method triggered with the button to start the generation of pdf. In process tab"""
        parameters = [t.currentText() for t in self.tabs[CONST.TYPE.PRO].combos.values()]
        exists = [t.check_path() for t in self.tabs[CONST.TYPE.PRO].combos.values()]
        if not all(parameters) or not all(exists):
            return None  # If one field is empty, ignore or if one path doesn't exists.

        self.statusBar().show()

        self.tabs[CONST.TYPE.PRO].buttons[CONST.TYPE.PDF].setDisabled(True)
        for name in CONST.TAB.ANALYSE + CONST.TAB.READER:
            self.tabs[name].table.init(**kwargs)

        self.process = NdfProcess(self, *parameters, **kwargs)
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
        self.menuWidget()._actions[obj.type].setChecked(True)
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
        QtWidgets.QMessageBox.critical(
            self, self.tr("Error"), f"{obj.__class__.__name__}:\n{''.join(traceback.format_tb(obj.__traceback__))}"
        )

    @QtCore.pyqtSlot(object)
    def generated(self, matricule):
        """Success methdod"""
        self.tear_down()
        if matricule is not None:
            msg = self.tr("The PDF file with the matricule {} have been generated!").format(matricule)
        else:
            msg = self.tr("The PDF files have been generated!")
        QtWidgets.QMessageBox.information(self, self.tr("Finished"), msg)

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
            setting = settings.value(name)
            if setting is None:
                continue
            attr = yaml.load(setting, Loader=yaml.FullLoader)
            if attr is None:
                continue

            if getattr(self, name) is None:
                setattr(self, name, attr)

            elif isinstance(getattr(self, name), set):
                getattr(self, name).update(attr)

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
            settings.setValue(name, yaml.dump(getattr(self, name)))

        self.app.set_language_mem()
        super().closeEvent(event)
