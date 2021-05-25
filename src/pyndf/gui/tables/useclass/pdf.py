# -*- coding: utf-8 -*-

from pyndf.gui.tables.useclass.analyse import AnalyseTable
from pyndf.gui.dialogs.preview import PreviewDialog


class PdfTable(AnalyseTable):
    def finished(self):
        self.cellClicked.connect(self.on_filename_clicked)
        super().finished()

    def on_filename_clicked(self, row, col):
        if col != 0:
            return

        dialog = PreviewDialog(self, row)
        dialog.exec()
