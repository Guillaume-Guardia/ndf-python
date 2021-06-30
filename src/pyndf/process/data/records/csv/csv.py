# -*- coding: utf-8 -*-

from pyndf.constants import CONST
from pyndf.process.data.records.abstract import Record


class CsvRecord(Record):
    def __init__(self, record, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log.debug("Create CSV record")
        # Matricule + Nom + agence
        for key in CONST.READER.CSV.COL_PERSO:
            setattr(self, key, record.get(self.csv_mapper[key], CONST.WRITER.PDF.UNKNOWN))
            self.log.debug(f"{key:25} = {getattr(self, key)}")

    @property
    def nom_intervenant(self):
        return f"{self.nom.capitalize()} {self.prenom.capitalize()}"
