# -*- coding: utf-8 -*-

from pyndf.qtlib import QtWidgets, QtGui
from pyndf.constants import CONST


class ExplorerButton(QtWidgets.QPushButton):
    """ """

    icon = CONST.UI.ICONS.PLUS

    def __init__(self, parent, *args):
        super().__init__(parent)
        self.parent = parent
        
        # Geometry
        self.setFixedHeight(30)
        self.setFixedWidth(45)

        # Front end
        self.setToolTip(self.tr("Click to select files"))
        self.setIcon(QtGui.QIcon(self.icon))

        # Signal
        self.pressed.connect(lambda: self.choose(*args))

    def choose(self, name_env, name, _format):
        """Method which call the native file dialog to choose file."""
        if _format is None:
            path = QtWidgets.QFileDialog.getExistingDirectory(self, self.tr("Open"))
            if not path:
                return
            paths = [path]
        else:
            paths, _ = QtWidgets.QFileDialog.getOpenFileNames(
                self,
                self.tr("Open"),
                filter=f"{name} {_format}" + f";;{self.tr('All files')} *" * CONST.READER.CAN_ADD_ALL_FILES,
            )

        self.parent.combos[name_env].add_items(paths)
