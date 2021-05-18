# -*- coding: utf-8 -*-

from collections import defaultdict
from pyndf.gui.tables.abstract import AbstractTable
from pyndf.process.writer.excel import ExcelWriter


class ExcelTable(AbstractTable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.itemChanged.connect(self.on_item_changed)

    def init(self):
        self.blockSignals(True)
        return super().init()

    def on_item_changed(self, *args):
        # table to dataframe
        data = defaultdict(list)
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                data[self.custom_item.headers[col]].append(self.item(row, col).text())

        writer = ExcelWriter(self.tab.window.excel, self.tab.window.app.temp_dir)

        self.tab.window.set_excel_from_writer(writer.write(data))

    def finished(self):
        self.blockSignals(False)
        return super().finished()
