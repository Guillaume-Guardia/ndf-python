# -*- coding: utf-8 -*-

from pyndf.qtlib import QtWidgets
from pyndf.constants import CONST


class RetryButton(QtWidgets.QPushButton):
    """ """

    def __init__(self, matricule, parent):
        super().__init__(parent)
        self.parent = parent

        # FrontEnd
        self.setText(self.tr("Retry {}").format(matricule))
        self.setToolTip(self.tr("Click to regenerate the pdf"))
        self.setStyleSheet(CONST.UI.BUTTONSTYLE)

        # Signal
        self.pressed.connect(lambda: self.retry_process(matricule))

    def retry_process(self, matricule):
        self.parent.tab.window.generate(matricule)

    def update_mode(self, dev_mode):
        pass
