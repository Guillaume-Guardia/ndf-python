# -*- coding: utf-8 -*-

from pyndf.gui.tables.abstract import AbstractTable
from pyndf.process.writer.factory import Writer


class AbstractSmartTable(AbstractTable):
    type = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.writer = Writer(self.type, dir=self.tab.window.app.temp_dir)

        self.itemChanged.connect(self.on_item_changed)

    def on_item_changed(self, data):
        self.tab.window.set_path(self.type, self.writer.write(data, getattr(self.tab.window, self.type)))

    def init(self, clear=False):
        self.blockSignals(True)
        if clear:
            super().init()

    def finished(self):
        self.blockSignals(False)
        super().finished()
