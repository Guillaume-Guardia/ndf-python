# -*- coding: utf-8 -*-

from pyndf.qtlib import QtWidgets
from pyndf.constants import CONST


class GenerateButton(QtWidgets.QPushButton):
    """ """

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Geometry
        self.setMinimumWidth(120)
        self.setMinimumHeight(40)

        # Front end
        self.setToolTip(self.tr("Click to generate the PDF files"))
        self.setText(self.tr("Generate PDF files"))
        self.setStyleSheet(CONST.UI.BUTTONSTYLE)

        # Signal
        self.pressed.connect(self.parent.window.generate)
