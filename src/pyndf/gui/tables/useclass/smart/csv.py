# -*- coding: utf-8 -*-

from collections import defaultdict
from pyndf.gui.tables.useclass.smart.abstract import AbstractSmartTable


class CsvSmartTable(AbstractSmartTable):
    type = "csv"

    def on_item_changed(self, *args):
        # table to dataframe
        data = defaultdict(list)
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                header = self.custom_item.headers[col]
                value = self.item(row, col).text()

                if value.isdigit():
                    if float(value) == int(value):
                        value = int(value)
                    else:
                        value = float(value)

                data[header].append(value)

        super().on_item_changed(data)
