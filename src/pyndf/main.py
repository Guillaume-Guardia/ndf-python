# -*- coding: utf-8 -*-

import sys
import argparse
import logging
from pyndf.app import App
from pyndf.process.threads.ndf import NdfProcess


class Container:
    def __init__(self):
        # Distance parameters
        self.use_db = True
        self.use_cache = True
        self.use_api = True

        # Pdf parameters
        self.color = None
        self.overwrite = True
        self.use_multithreading = True
        self.processes = []


def start(*args, use_gui=True, excel=None, csv=None, output=None, **kwargs):
    app = App(*args, use_gui=use_gui)
    if use_gui:
        app.load_translator()
        app.load_window(excel, csv, output, **kwargs)
    else:
        container = Container()
        process = NdfProcess(container, excel, csv, output)
        process.start()

        # Connect signals to exit application
        process.signals.cancelled.connect(sys.exit)
        process.signals.error.connect(sys.exit)
        process.signals.finished.connect(sys.exit)

    return app.exec()


def cmdline():
    parser = argparse.ArgumentParser("NDF")
    parser.add_argument(
        "--log", help="level log", choices=["notset", "debug", "info", "warn", "error", "critical"], type=str
    )
    parser.add_argument("-e", "--excel", help="Excel file to parse", type=str)
    parser.add_argument("-c", "--csv", help="CSV file to parse", type=str)
    parser.add_argument("-o", "--output", help="Output directory", type=str)
    parser.add_argument("-l", "--language", help="Select language (en, fr)", type=str)

    args = parser.parse_args()

    level = logging.DEBUG
    if args.log:
        level = getattr(logging, args.log.upper())

    use_gui = not all([args.excel, args.csv, args.output])
    return start(args.language, use_gui=use_gui, excel=args.excel, csv=args.csv, output=args.output, log_level=level)


if __name__ == "__main__":
    print("coucou")
    # from PyQt6 import QtWidgets
    # print("ff")
    # app = QtWidgets.QApplication([])
    # window = QtWidgets.QMainWindow()
    # window.show()
    # sys.exit(app.exec())
    sys.exit(cmdline())
