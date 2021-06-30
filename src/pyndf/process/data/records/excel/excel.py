# -*- coding: utf-8 -*-

from pyndf.constants import CONST
from pyndf.process.data.records.abstract import Record


class ExcelRecord(Record):
    def __init__(self, record, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log.debug("Create Excel record")
        # Personal info
        for key in CONST.READER.EXC.COL_PERSO:
            setattr(self, key, record.get(self.excel_mapper[key], CONST.WRITER.PDF.UNKNOWN))
            self.log.debug(f"{key:25} = {getattr(self, key)}")

    @property
    def nom_intervenant(self):
        name = self.nom.split()
        for index, s in enumerate(name):
            name[index] = s.capitalize()
        return " ".join(name)
