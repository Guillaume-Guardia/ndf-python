# -*- coding: utf-8 -*-

import os
import tempfile
from glob import glob
from pyndf.qtlib import QtWidgets, QtCore
from pyndf.constants import CONST
from pyndf.gui.windows.main import MainWindow


class App(QtWidgets.QApplication):
    def __init__(self, language="fr", use_gui=True):
        super().__init__([])

        self.temp_dir = tempfile.mkdtemp()

        self.__window = None
        self.__language = None

        self.language = language or App.get_language_mem()
        self.translator = None

        if use_gui:
            self.language_available = App.get_available_language()
            self.resolution = self.primaryScreen().availableSize()

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
        """Load translator in Qt app. To load another translator, you have to remove the existent before."""
        if self.translator is not None:
            self.removeTranslator(self.translator)

        translator = QtCore.QTranslator()

        # Load translator
        if translator.load(self.language, "pyndf", "_", CONST.FILE.TRANSLATION_DIR, CONST.EXT.QM):
            # Install translator
            self.installTranslator(translator)
            self.translator = translator

    def load_window(self, *args, **kwargs):
        """Load window. shortcut to add app in argument of window."""
        self.window = MainWindow(self, *args, **kwargs)
        self.window.show()

    def set_language_mem(self):
        """Memorize the language in settings object to reuse in another session."""
        settings = QtCore.QSettings(CONST.COMPANY, CONST.TITLE_APP)
        settings.setValue(CONST.TYPE.LAN, self.language.language())

    @staticmethod
    def get_available_language():
        """Get languages from translation directory. Add a ts file in translation dir
        to use it in app.

        Returns:
            list: list of available language
        """
        language_available = []
        ts_files = glob(os.path.join(CONST.FILE.TRANSLATION_DIR, "*" + CONST.EXT.TS))
        for ts_file in ts_files:
            language_available.append(os.path.basename(ts_file).split(".")[0].split("_")[1])

        return language_available

    @staticmethod
    def get_language_mem():
        """Get the language from the settings object of Qt.

        Returns:
            string: fr or en
        """
        settings = QtCore.QSettings(CONST.COMPANY, CONST.TITLE_APP)
        return settings.value(CONST.TYPE.LAN)
