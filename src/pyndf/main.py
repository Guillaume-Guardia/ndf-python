# -*- coding: utf-8 -*-

import os
import sys
import argparse
from glob import glob
import logging
from pyndf.qtlib import QtWidgets, QtCore
from pyndf.constants import TRANSLATION_DIR
from pyndf.gui.windows.main_window import MainWindow


class App(QtWidgets.QApplication):
    def __init__(self, language, *args):
        super().__init__(*args)

        self.__window = None
        self.__language = None

        self.language = language
        self.translator = None
        self.language_available = self.get_available_language()
        self.resolution = self.primaryScreen().availableSize()

    def get_available_language(self):
        language_available = []
        ts_files = glob(os.path.join(TRANSLATION_DIR, "*.ts"))
        for ts_file in ts_files:
            language_available.append(os.path.basename(ts_file).split(".")[0].split("_")[1])

        return language_available

    @property
    def window(self):
        return self.__window

    @window.setter
    def window(self, value):
        self.__window = value
        self.__window.show()

    @property
    def language(self):
        return self.__language

    @language.setter
    def language(self, value):
        if value:
            self.__language = QtCore.QLocale(value)
        else:
            self.__language = QtCore.QLocale()

    def load_translator(self):
        if self.translator is not None:
            self.removeTranslator(self.translator)

        translator = QtCore.QTranslator()

        # Load translator
        if translator.load(self.language, "pyndf", "_", TRANSLATION_DIR, ".qm"):
            # Install translator
            self.installTranslator(translator)
            self.translator = translator


def main(language, **kwargs):
    app = App(language, [])
    app.load_translator()
    app.window = MainWindow(app, **kwargs)
    sys.exit(app.exec())


def cmdline():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbosity", help="increase output verbosity", action="store_true")
    parser.add_argument("-e", "--excel", help="Excel file to parse", type=str)
    parser.add_argument("-c", "--csv", help="CSV file to parse", type=str)
    parser.add_argument("-o", "--output", help="Output directory", type=str)
    parser.add_argument("-l", "--language", help="Select language (en, fr)", type=str)

    args = parser.parse_args()

    if args.verbosity:
        level = logging.DEBUG
    else:
        level = logging.INFO

    main(args.language, excel=args.excel, csv=args.csv, output=args.output, log_level=level)


if __name__ == "__main__":
    cmdline()
