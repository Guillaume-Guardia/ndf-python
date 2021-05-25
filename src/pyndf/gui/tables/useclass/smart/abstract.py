# -*- coding: utf-8 -*-

from collections import defaultdict
from pyndf.gui.tables.abstract import AbstractTable
from pyndf.process.writer.factory import Writer
from pyndf.utils import Utils


class AbstractSmartTable(AbstractTable):
    type = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.writer = Writer(self.type, directory=self.tab.window.app.temp_dir)

        self.itemChanged.connect(self.on_item_changed)

    def on_item_changed(self, *args):
        # table to dataframe
        data = defaultdict(list)
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                header = self.custom_item.headers[col]
                value = self.item(row, col).text()
                value = self.set_type(value, header)
                data[header].append(value)

        (filename, status), time_spend = self.writer.write(data, getattr(self.tab.window, self.type))
        self.tab.window.set_path(self.type, filename)

    def set_type(self, value, *args):
        return Utils.type(value)

    def init(self, clear=False):
        self.blockSignals(True)
        if clear:
            super().init()

    def finished(self):
        self.blockSignals(False)
        super().finished()
