# -*- coding: utf-8 -*-

from collections import defaultdict
from pyndf.gui.tables.useclass.smart.abstract import AbstractSmartTable
from pyndf.constants import CONFIG, COL
from pyndf.process.utils import Utils


class ExcelSmartTable(AbstractSmartTable):
    type = "excel"

    def on_item_changed(self, *args):
        # table to dataframe
        data = defaultdict(list)
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                header = self.custom_item.headers[col]
                value = self.item(row, col).text()

                if header != CONFIG[COL]["matricule"]:
                    value = Utils.type(value)

                data[header].append(value)

        super().on_item_changed(data)
