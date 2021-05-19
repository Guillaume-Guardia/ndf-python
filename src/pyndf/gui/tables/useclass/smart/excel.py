# -*- coding: utf-8 -*-

from collections import defaultdict
from pyndf.gui.tables.useclass.smart.abstract import AbstractSmartTable
from pyndf.constants import CONFIG, COL


class ExcelSmartTable(AbstractSmartTable):
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
