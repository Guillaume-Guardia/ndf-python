# -*- coding: utf-8 -*-


from pyndf.gui.tables.useclass.smart.abstract import AbstractSmartTable
from pyndf.constants import CONST
from pyndf.utils import Utils


class ExcelSmartTable(AbstractSmartTable):
    type = CONST.TYPE.EXC

    def set_type(self, value, header):
        if header != CONST.FILE.YAML[self.type]["matricule"]:
            value = Utils.type(value)
        return value
