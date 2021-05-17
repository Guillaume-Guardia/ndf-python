# -*- coding: utf-8 -*-

import sys
import argparse
from pyndf.qtlib import QtWidgets, QtCore
from pyndf.constants import TRANSLATION_DIR
from pyndf.gui.windows.main_window import MainWindow


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
