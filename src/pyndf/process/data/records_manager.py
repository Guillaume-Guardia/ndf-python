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
            self._records[matricule] = ExcelRecord(record, self, log_level=self.log_level)
        self._records[matricule].add_mission(record)

    def add_csv_record(self, record, columns):
        matricule = Utils.type(record[CONST.FILE.YAML[CONST.TYPE.CSV]["matricule"]])

        # Check if not exist already
        if matricule not in self._records:
            # Create CSV record
            self._records[matricule] = CsvRecord(record, self, log_level=self.log_level)
        return self._records[matricule].add_indemnites(record, columns)

    def __iter__(self):
        if self.matricule is not None:
            # Take only the specific matricule
            return (r for r in [self._records[self.matricule]])
        # Else take all the records defined in self._records
        return (r for r in self._records.values() if len(r) > 0)

    def __len__(self):
        if self.matricule is not None:
            # Take only the specific matricule
            return 1
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

        for record in self:
            # Check if number of missions is egual to number of indemnites.
            while len(record.missions) < len(record.indemnites):
                # Add default mission or add default indemnite
                record.missions.append(record.default_mission)

            while len(record.missions) > len(record.indemnites):
                # Add default mission or add default indemnite
                record.indemnites[f"default_{len(record.indemnites)}"] = record.default_indemnite

            # Missions
            for mission, indemnite in zip(record.missions, record.indemnites.values()):
                add_personal_info()
                # List of dictionnary
                for name in CONST.WRITER.PDF.COL_MISSION_EXCEL:
                    attr = getattr(mission, name)

                    if name == "periode_production":
                        attr = getattr(self, name)
                    elif name == "nbr_km_mois" and attr == 0:
                        attr = ""

                    data[CONST.FILE.YAML[CONST.TYPE.PDF][name]].append(attr)

                # Dictionnary of dictionnary
                for name in CONST.WRITER.PDF.COL_MISSION_CSV:
                    attr = getattr(indemnite, name)
                    if attr == 0:
                        attr = ""
                    data[CONST.FILE.YAML[CONST.TYPE.PDF][name]].append(attr)

        return data
