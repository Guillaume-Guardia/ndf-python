# -*- coding: utf-8 -*-

import os
from pyndf.qtlib import QtCore
from pyndf.logbook import Logger


class AbstractReader(Logger, QtCore.QObject):
    """Abstract class for reading file."""

    type = None

    @classmethod
    def can_read(cls, filename):
        if cls.regex.match(filename):
            return cls.type
        return None

    def check_path(self, filename=None):
        if not os.path.exists(filename):
            self.log.warning(f"The file '{filename}' doesn't exists !")
            return False

        self.log.info(f"Extract Data from {self.type.upper()} file: {os.path.basename(filename)}")
        return True
