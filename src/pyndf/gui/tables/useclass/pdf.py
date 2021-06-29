# -*- coding: utf-8 -*-

from pyndf.gui.tables.useclass.analyse import AnalyseTable
from pyndf.qtlib import QtWidgets, QtCore
from pyndf.constants import CONST
from pyndf.gui.dialogs.preview import PreviewDialog


class PdfTable(AnalyseTable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add(self, obj):
        # Create push button for filename
        obj.filename = QtWidgets.QPushButton(obj.filename, self)
        obj.filename.setToolTip(self.tr("Click to view the pdf"))
        row, column = self.rowCount(), self.custom_item.headers.index("filename")
        obj.filename.pressed.connect(lambda r=row, c=column: self.on_filename_press(r, c))
        super().add(obj)

    def on_filename_press(self, *args):
        dialog = PreviewDialog(self, *args)
        dialog.exec()

    def finished(self):
        column = self.columnCount() - 1

        # Add button to row with a red status
        for row in range(self.rowCount()):
            status = self.item(row, self.custom_item.headers.index("status")).text()
            if not getattr(CONST.STATUS, status):
                matricule = self.item(row, self.custom_item.headers.index("matricule")).data(
                    QtCore.Qt.ItemDataRole.EditRole
                )
                button = QtWidgets.QPushButton(self.tr("Retry {}").format(matricule), self)
                button.pressed.connect(lambda mat=matricule: self.retry_process(mat))
                self.setCellWidget(row, column, button)

        # Add the total column and set visible the corresponding item in menu
        super().finished()

    def retry_process(self, matricule):
        self.tab.window.generate(matricule)
