# -*- coding: utf-8 -*-

from pyndf.gui.tables.useclass.analyse import AnalyseTable
from pyndf.gui.dialogs.preview import PreviewDialog


class PdfTable(AnalyseTable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.cellClicked.connect(self.on_filename_clicked)

    def on_filename_clicked(self, row, col):
        if self.custom_item.headers[col] == "filename":
            dialog = PreviewDialog(self, col, row)
            dialog.exec()
