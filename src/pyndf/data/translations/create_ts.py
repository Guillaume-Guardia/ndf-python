import os
from glob import glob
import argparse
from PyQt6.lupdate import lupdate


def write_ts_files(verbosity=False):
    file_dir = os.path.dirname(__file__)

    # get translation_files
    ts_files = glob(os.path.join(file_dir, "*.ts"))

    if len(ts_files) == 0:
        # Create it
        ts_files.append(os.path.join(file_dir, "pyndf_fr.ts"))
        ts_files.append(os.path.join(file_dir, "pyndf_en.ts"))

    # get py_files
    py_files = glob(os.path.join(file_dir, "..", "..", "**", "*.py"), recursive=True)

    if verbosity:
        print("TS", ts_files)
        print("PY", py_files)

    lupdate(py_files, ts_files)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbosity", help="increase output verbosity", action="store_true")

    args = parser.parse_args()

    write_ts_files(verbosity=args.verbosity)
