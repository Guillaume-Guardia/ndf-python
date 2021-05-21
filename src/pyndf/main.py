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
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--log", help="level log", choices=["NOTSET", "DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"], type=str
    )
    parser.add_argument("-e", "--excel", help="Excel file to parse", type=str)
    parser.add_argument("-c", "--csv", help="CSV file to parse", type=str)
    parser.add_argument("-o", "--output", help="Output directory", type=str)
    parser.add_argument("-l", "--language", help="Select language (en, fr)", type=str)

    args = parser.parse_args()

    if args.log:
        level = getattr(logging, args.log)
    else:
        level = logging.INFO

    return main(args.language, excel=args.excel, csv=args.csv, output=args.output, log_level=level)


if __name__ == "__main__":
    sys.exit(cmdline())
