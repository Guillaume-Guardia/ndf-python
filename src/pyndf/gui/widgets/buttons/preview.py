# -*- coding: utf-8 -*-

import os
import re
from pyndf.qtlib import QtWidgets
from pyndf.gui.dialogs.preview import PreviewDialog
from pyndf.constants import CONST


class PreviewButton(QtWidgets.QPushButton):
    """ """

    def __init__(self, path, parent, column):
        basename = os.path.basename(path)
        super().__init__(basename, parent)
        self.parent = parent
        self.path = path

        # Front end
        self.setToolTip(self.tr("Click to view the PDF file {}").format(path))
        self.setStyleSheet(CONST.UI.BUTTONSTYLE)

        # Signal
        self.pressed.connect(lambda: self.on_filename_press(column))

    def on_filename_press(self, *args):
        dialog = PreviewDialog(self, *args)
        dialog.show()

    def update_mode(self, dev_mode):
        pass
