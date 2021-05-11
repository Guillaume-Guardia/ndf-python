# -*- coding: utf-8 -*-

import sys
import argparse
from PyQt6 import QtWidgets, QtCore
from pyndf.logbook import Logger
from pyndf.process.thread import Thread
from pyndf.constants import CONFIG, TRANSLATION_DIR
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
        self.setWindowTitle("PYNDF")
        self.setWindowIcon(self.style().standardIcon(self.style().StandardPixmap.SP_TitleBarMenuButton))
        if resolution:
            self.setMinimumWidth(int(resolution.width() / 1.5))
            self.setMinimumHeight(int(resolution.height() / 3))

        # Initialisation attributes
        self.threadpool = QtCore.QThreadPool()

        # Tabs
        self.tab_widget = QtWidgets.QTabWidget()
        self.setCentralWidget(self.tab_widget)
        self.tabs = {}

        # Process tab
        self.tabs["process"] = ProcessTab(self, excel=excel, csv=csv, output=output)
        self.tab_widget.addTab(self.tabs["process"], self.tabs["process"].title)

        # Analyse tabs
        self.tabs["analyse"] = {}
        titles = (self.tr("Analyse Global"), self.tr("Analyse Google API"), self.tr("Analyse PDF writer"))
        items = (AllItem, APIItem, PDFItem)
        for title, item in zip(titles, items):
            self.tabs["analyse"][title] = AnalyseTab(self, title, item)
            self.tab_widget.addTab(self.tabs["analyse"][title], title)

        # Progress Bar in status bar
        self.progress = QtWidgets.QProgressBar()
        self.set_progress_bar()

    def set_progress_bar(self):
        self.progress.hide()
        status_bar = QtWidgets.QStatusBar()
        status_bar.addPermanentWidget(self.progress, 0)
        self.setStatusBar(status_bar)

    def generate(self):
        """Method triggered with the button to start the generation of pdf."""
        if not all([t.text() for t in self.tabs["process"].texts.values()]):
            return None  # If one field is empty, ignore.

        self.progress.show()
        self.tabs["process"].buttons["generate"].setDisabled(True)
        for tab in self.tabs["analyse"].values():
            tab.init_table()
        process = Thread(*[t.text() for t in self.tabs["process"].texts.values()])
        process.signals.error.connect(self.error)
        process.signals.finished.connect(self.generated)
        process.signals.progressed.connect(self.progressed)
        process.signals.analysed_all.connect(self.tabs["analyse"][self.tr("Analyse Global")].analysed)
        process.signals.analysed_api.connect(self.tabs["analyse"][self.tr("Analyse Google API")].analysed)
        process.signals.analysed_pdf.connect(self.tabs["analyse"][self.tr("Analyse PDF writer")].analysed)
        self.threadpool.start(process)
        return True

    def error(self, obj):
        self.progress.hide()
        self.progress.reset()
        for tab in self.tabs["analyse"].values():
            tab.finished()
        self.tabs["process"].buttons["generate"].setDisabled(False)
        QtWidgets.QMessageBox.critical(self, self.tr("Error"), self.tr("Error: {}".format(obj)))

    def progressed(self, value, text):
        if value <= 100:
            self.progress.setValue(int(value))
            self.statusBar().showMessage(text, 1000)

    def generated(self, time):
        """Success methdod"""
        self.progress.hide()
        self.progress.reset()
        for tab in self.tabs["analyse"].values():
            tab.finished()
        self.tabs["process"].buttons["generate"].setDisabled(False)
        QtWidgets.QMessageBox.information(self, self.tr("Finished"), self.tr("PDFs have been generated !"))


def main(language="", **kwargs):
    app = QtWidgets.QApplication([])

    translator = QtCore.QTranslator()

    # Load translator
    locale = QtCore.QLocale()
    if language:
        locale = QtCore.QLocale(language)

    if translator.load(locale, "pyndf", "_", TRANSLATION_DIR, ".qm"):
        # Install translator
        app.installTranslator(translator)

    res = app.primaryScreen().availableSize()
    w = MainWindow(**kwargs, resolution=res)

    w.show()
    sys.exit(app.exec())


def cmdline():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbosity", help="increase output verbosity", action="store_true")
    parser.add_argument("-e", "--excel", help="Excel file to parse", type=str)
    parser.add_argument("-c", "--csv", help="CSV file to parse", type=str)
    parser.add_argument("-o", "--output", help="Output directory", type=str)
    parser.add_argument("-l", "--language", help="Select language (en, fr)", type=str)

    args = parser.parse_args()

    args.excel = r"C:\Users\guill\Documents\Projets\NDF_python\venv\src\ndf-python\data\FRAIS_202011.XLS"
    args.csv = r"C:\Users\guill\Documents\Projets\NDF_python\venv\src\ndf-python\data\RE NDF\GA327122020 test.CSV"
    args.output = "C:/Users/guill/Documents/Projets/NDF_python/venv/src/test2"

    main(excel=args.excel, csv=args.csv, output=args.output, language=args.language)


if __name__ == "__main__":
    cmdline()
