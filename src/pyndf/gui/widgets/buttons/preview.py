# -*- coding: utf-8 -*-

import os
from pyndf.qtlib import QtWidgets
from pyndf.gui.dialogs.preview import PreviewDialog
from pyndf.constants import CONST


class PreviewButton(QtWidgets.QPushButton):
    """ """

    def __init__(self, path, parent, row, column):
        basename = os.path.basename(path)
        super().__init__(basename, parent)
        self.parent = parent
        self.path = path

        # Front end
        self.setToolTip(self.tr("Click to view the PDF file {}").format(path))
        self.setStyleSheet(CONST.UI.BUTTONSTYLE)

        # Signal
        self.pressed.connect(lambda: self.on_filename_press(row, column))

    def on_filename_press(self, *args):
        dialog = PreviewDialog(self.parent, *args)
        dialog.exec()

    def update_mode(self, dev_mode):
        pass
