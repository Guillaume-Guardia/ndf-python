# -*- coding: utf-8 -*-

import sys
import argparse
import logging
from pyndf.app import App


def main(language, **kwargs):
    app = App(language, [])
    app.load_translator()
    app.load_window(**kwargs)
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

    level = logging.NOTSET
    if args.log:
        level = getattr(logging, args.log.upper())

    return main(args.language, excel=args.excel, csv=args.csv, output=args.output, log_level=level)


if __name__ == "__main__":
    sys.exit(cmdline())
