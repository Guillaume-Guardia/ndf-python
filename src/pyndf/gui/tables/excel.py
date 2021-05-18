# -*- coding: utf-8 -*-

from collections import defaultdict
from pyndf.gui.tables.abstract import AbstractTable
from pyndf.process.writer.excel import ExcelWriter
from pyndf.constants import CONFIG, COL


class ExcelTable(AbstractTable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.writer = ExcelWriter(temp_dir=self.tab.window.app.temp_dir)

        self.itemChanged.connect(self.on_item_changed)

    def init(self):
        self.blockSignals(True)
        return super().init()

    def on_item_changed(self, *args):
        # table to dataframe
        data = defaultdict(list)
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                header = self.custom_item.headers[col]
                value = self.item(row, col).text()

                if header != CONFIG[COL]["matricule"]:
                    try:
                        value = float(value)
                    except ValueError:
                        pass

                data[header].append(value)

        self.tab.window.set_excel_from_writer(self.writer.write(data, self.tab.window.excel))

    def finished(self):
        self.blockSignals(False)
        return super().finished()
