# -*- coding: utf-8 -*-

from pyndf.gui.tables.useclass.analyse import AnalyseTable
from pyndf.qtlib import QtCore
from pyndf.constants import CONST
from pyndf.gui.widgets.buttons.preview import PreviewButton
from pyndf.gui.widgets.buttons.retry import RetryButton


class PdfTable(AnalyseTable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add(self, obj):
        # Create push button for filename
        row, column = self.rowCount(), self.custom_item.headers.index("filename")
        obj.filename = PreviewButton(obj.filename, self, row, column)
        super().add(obj)

    def finished(self):
        column = self.columnCount() - 1

        # Add button to row with a red status
        must_hide_retry_col = True
        for row in range(self.rowCount()):
            if self.item(row, self.custom_item.headers.index("status")).status:
                continue

            matricule = self.item(row, self.custom_item.headers.index("matricule")).data(
                QtCore.Qt.ItemDataRole.EditRole
            )
            button = RetryButton(matricule, self)
            self.setCellWidget(row, column, button)
            must_hide_retry_col = False

        self.setColumnHidden(
            self.custom_item.headers.index("retry"),
            must_hide_retry_col,
        )

        # Add the total column and set visible the corresponding item in menu
        super().finished()
