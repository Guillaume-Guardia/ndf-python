# -*- coding: utf-8 -*-

import re
from collections import defaultdict
import pandas as pd
from pyndf.logbook import Logger, log_time
from pyndf.constants import CONFIG, COL, COL_PERSO, COL_MISSION


class ExcelReader(Logger):
    """Class for reading excel file."""

    def __init__(self, filename=None, sheet_name=None, regex_libelle="INDEMNITE.*"):
        super().__init__()
        self.filename = filename
        self.sheet_name = sheet_name
        self.reg = re.compile(regex_libelle)

    @log_time
    def read(self, filename=None, sheet_name=None):
        path = filename or self.filename
        sheet = sheet_name or self.sheet_name
        self.log.info(f"Extract Data from sheet {sheet} and excel file {path}")
        # Initialisation variables
        records = defaultdict(dict)

        # Get the data on excel file in dataframe format.
        dataframe = pd.read_excel(path, sheet_name=sheet)

        for record in dataframe.to_dict("records"):
            matricule = record[CONFIG[COL]["matricule"]]

            if self.reg.match(str(record[CONFIG[COL]["libelle"]])) is None:
                continue

            if matricule not in records:
                # Personal info
                for key in CONFIG[COL_PERSO]:
                    records[matricule][key] = record[CONFIG[COL][key]]
                    self.log.debug(f"{matricule} | {key} = {records[matricule][key]}")
                records[matricule]["missions"] = []

            # Mission Info
            mission_record = {}
            for key in CONFIG[COL_MISSION]:
                mission_record[key] = record[CONFIG[COL][key]]
                self.log.debug(f"{matricule} | missions | {key} = {mission_record[key]}")
            records[matricule]["missions"].append(mission_record)

        return records
