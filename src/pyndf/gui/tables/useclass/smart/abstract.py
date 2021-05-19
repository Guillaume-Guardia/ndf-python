# -*- coding: utf-8 -*-

from pyndf.gui.tables.abstract import AbstractTable
from pyndf.process.writer.factory import writer_factory


class AbstractSmartTable(AbstractTable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.writer = writer_factory(self.custom_item, dir=self.tab.window.app.temp_dir)

        self.itemChanged.connect(self.on_item_changed)

    def on_item_changed(self, *args):
        pass

    def init(self):
        self.blockSignals(True)
        return super().init()

    def finished(self):
        result = super().finished()
        self.blockSignals(False)
        return result
