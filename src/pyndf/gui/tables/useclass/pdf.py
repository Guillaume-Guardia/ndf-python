# -*- coding: utf-8 -*-

from pyndf.gui.tables.useclass.analyse import AnalyseTable
from pyndf.gui.dialogs.preview import PreviewDialog


class PdfTable(AnalyseTable):
    def finished(self):
        self.cellClicked.connect(self.on_filename_clicked)
        self.tab.window.toggled_tab(self.tab, True)
        super().finished()

    def on_filename_clicked(self, row, col):
        if col != 0:
            return

        filename = self.item(row, col).text()

        dialog = PreviewDialog(self.tab.window, filename)
        dialog.exec()
