# -*- coding: utf-8 -*-

import os
from pyndf.qtlib import QtCore
from pyndf.logbook import Logger
from pyndf.constants import CONFIG
from pyndf.gui.items.useclass.reader.csv import CsvItem


class AbstractReader(Logger, QtCore.QObject):
    """Abstract class for reading file."""

    type = None

    def check_path(self, filename=None):
        if not os.path.exists(filename):
            self.log.warning(f"The file ' {filename} ' doesn't exists !")
            return False

        self.log.info(f"Extract Data from {self.type} file: {os.path.basename(filename)}")
        return True
