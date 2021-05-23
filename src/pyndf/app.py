# -*- coding: utf-8 -*-

import os
import tempfile
from glob import glob
from pyndf.qtlib import QtWidgets, QtCore
from pyndf.constants import CONST
from pyndf.gui.windows.main import MainWindow


class App(QtWidgets.QApplication):
    def __init__(self, language, *args):
        super().__init__(*args)

        self.temp_dir = tempfile.mkdtemp()

        self.__window = None
        self.__language = None

        self.language = language or self.get_language_mem()
        self.translator = None
        self.language_available = self.get_available_language()
        self.resolution = self.primaryScreen().availableSize()

    def get_available_language(self):
        language_available = []
        ts_files = glob(os.path.join(CONST.FILE.TRANSLATION_DIR, "*" + CONST.EXT.TS))
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
        if translator.load(self.language, "pyndf", "_", CONST.FILE.TRANSLATION_DIR, CONST.EXT.QM):
            # Install translator
            self.installTranslator(translator)
            self.translator = translator

    def load_window(self, *args, **kwargs):
        self.window = MainWindow(self, *args, **kwargs)

    def get_language_mem(self):
        settings = QtCore.QSettings(CONST.COMPANY, CONST.TITLE_APP)
        return settings.value(CONST.TYPE.LAN)

    def set_language_mem(self):
        settings = QtCore.QSettings(CONST.COMPANY, CONST.TITLE_APP)
        settings.setValue(CONST.TYPE.LAN, self.language.language())
