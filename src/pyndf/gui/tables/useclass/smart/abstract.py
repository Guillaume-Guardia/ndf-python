# -*- coding: utf-8 -*-

from collections import defaultdict
from pyndf.gui.tables.abstract import AbstractTable
from pyndf.process.writer.factory import Writer
from pyndf.utils import Utils


class AbstractSmartTable(AbstractTable):
    type = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filename = None

        self.itemChanged.connect(self.on_item_changed)

    def on_item_changed(self, *args):
        if self.tab.window.save_tmp_file:
            directory = None
        else:
            directory = self.tab.window.app.temp_dir

        writer = Writer(self.type, directory=directory, log_level=self.tab.window.log_level)

        # table to dataframe
        data = defaultdict(list)
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                header = self.custom_item.headers[col]
                value = self.item(row, col).text()
                value = self.set_type(value, header)
                data[header].append(value)

        (filename, status), time_spend = writer.write(data, self.filename)
        self.tab.window.set_path(self.type, filename)

    def set_type(self, value, *args):
        return Utils.type(value)

    def init(self, filename=None, clear=False, **kwargs):
        if filename is not None:
            self.filename = filename
        self.blockSignals(True)
        super().init(clear=clear)

    def finished(self, *args):
        self.blockSignals(False)
        super().finished(*args)

    def add(self, obj):
        if self.columnCount() != obj.counter:
            self.set_horizontal_headers(obj.headers)
            self.custom_item.headers = obj.headers

        return super().add(obj)
