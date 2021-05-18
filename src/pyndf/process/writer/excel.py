# -*- coding: utf-8 -*-

import os
import pandas as pd
from pyndf.qtlib import QtCore
from pyndf.logbook import Logger


class ExcelWriter(Logger, QtCore.QObject):
    """Class for reading excel file."""

    def __init__(self, filename=None, temp_dir=None, **kwargs):
        """Initialisation

        Args:
            filename (string, optional): file to read. Defaults to None.
            sheet_name (int or string, optional): Sheet to read. Defaults to 0 -> First Sheet.
            regex_libelle (str, optional): Regex. Defaults to "INDEMNITE.*".
        """
        super().__init__(**kwargs)
        self.filename = filename
        self.temp_dir = temp_dir

    def write(self, data, filename=None):
        path = filename or self.filename
        basename = os.path.basename(path)
        basename = basename.split(".")[0] + ".xlsx"
        self.log.info(f"Write data on temp excel file {os.path.basename(basename)}")

        path = os.path.join(self.temp_dir, basename)

        df = pd.DataFrame(data)

        with pd.ExcelWriter(path, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False)

        return path
