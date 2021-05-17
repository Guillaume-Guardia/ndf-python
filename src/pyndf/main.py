# -*- coding: utf-8 -*-

import os
import sys
import argparse
from glob import glob
from pyndf.qtlib import QtWidgets, QtCore
from pyndf.constants import TRANSLATION_DIR
from pyndf.gui.windows.main_window import MainWindow


class App(QtWidgets.QApplication):
    def __init__(self, *args, language="", **kwargs):
        super().__init__(*args)

        self.locale = QtCore.QLocale()
        self.set_locale(language)

        self.language_available = []

        ts_files = glob(os.path.join(TRANSLATION_DIR, "*.ts"))
        for ts_file in ts_files:
            self.language_available.append(os.path.basename(ts_file).split(".")[0].split("_")[1])

        self.resolution = self.primaryScreen().availableSize()

        self.translator = None

    def set_locale(self, language):
        if language:
            self.locale = QtCore.QLocale(language)

    def set_translator(self):

        if self.translator is not None:
            self.removeTranslator(self.translator)

        translator = QtCore.QTranslator()

        # Load translator
        if translator.load(self.locale, "pyndf", "_", TRANSLATION_DIR, ".qm"):
            # Install translator
            self.installTranslator(translator)
            self.translator = translator


def main(language="", **kwargs):
    app = App([], language=language)

    window = MainWindow(app, **kwargs)
    window.show()
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
