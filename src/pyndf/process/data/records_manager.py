# -*- coding: utf-8 -*-

from collections import defaultdict
from pyndf.constants import CONST
from pyndf.logbook import Logger
from pyndf.utils import Utils
from pyndf.process.data.records.excel.excel import ExcelRecord
from pyndf.process.data.records.csv.csv import CsvRecord


class RecordsManager(Logger):
    def __init__(self, *args, matricule=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._records = {}
        self.matricule = Utils.type(matricule)

    def add_excel_record(self, record):
        matricule = Utils.type(record[CONST.FILE.YAML[CONST.TYPE.EXC]["matricule"]])

        # Check if not exist already
        if matricule not in self._records:
            # Create Excel record
            self._records[matricule] = ExcelRecord(record, log_level=self.log_level)
        self._records[matricule].add_mission(record)

    def add_csv_record(self, record, columns):
        matricule = Utils.type(record[CONST.FILE.YAML[CONST.TYPE.CSV]["matricule"]])

        # Check if not exist already
        if matricule not in self._records:
            # Create CSV record
            self._records[matricule] = CsvRecord(record, log_level=self.log_level)
        return self._records[matricule].add_indemnites(record, columns)

    def __iter__(self):
        if self.matricule is not None:
            # Take only the specific matricule
            return (r for r in [self._records[self.matricule]])
        # Else take all the records defined in self._records
        return (r for r in self._records.values() if len(r) > 0)

    def __len__(self):
        return sum([int(len(record) > 0) for record in self._records.values()])

    def export(self):
        data = defaultdict(list)

        def add_personal_info():
            # Agence
            data["Agence"].append(record.agence)
            data["Agence d'origine"].append(record.agence_o)

            # Personnal data in record
            for col in CONST.WRITER.PDF.COL_PERSO:
                data[CONST.FILE.YAML[CONST.TYPE.PDF][col]].append(getattr(record, col))

        for record in self._records.values():
            # Missions
            for mission in record.missions:
                add_personal_info()
                # List of dictionnary
                for name in CONST.WRITER.PDF.COL_MISSION:
                    data[CONST.FILE.YAML[CONST.TYPE.PDF][name]].append(getattr(mission, name))

            for indemnite in record.indemnites.values():
                add_personal_info()
                # Dictionnary of dictionnary
                for name in CONST.WRITER.PDF.COL_MISSION:
                    data[CONST.FILE.YAML[CONST.TYPE.PDF][name]].append(getattr(indemnite, name))

        return data
