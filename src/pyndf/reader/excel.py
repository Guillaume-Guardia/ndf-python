# -*- coding: utf-8 -*-

import re
from collections import defaultdict
import pandas as pd
from pyndf.logbook import Logger, log_time
from pyndf.constants import CONFIG, COL, COL_PERSO, COL_MISSION


class ExcelReader(Logger):
    """Class for reading excel file."""

    def __init__(self, filename=None, sheet_name=0, regex_libelle="INDEMNITE.*"):
        """Initialisation

        Args:
            filename (string, optional): file to read. Defaults to None.
            sheet_name (int or string, optional): Sheet to read. Defaults to 0 -> First Sheet.
            regex_libelle (str, optional): Regex. Defaults to "INDEMNITE.*".
        """
        super().__init__()
        self.filename = filename
        self.sheet_name = sheet_name
        self.reg = re.compile(regex_libelle)

    @log_time
    def read(self, filename=None, sheet_name=0, progress_callback=None, p=100):
        path = filename or self.filename
        sheet = sheet_name or self.sheet_name
        self.log.info(f"Extract Data from sheet {sheet} and excel file {path}")
        # Initialisation variables
        records = defaultdict(dict)

        # Get the data on excel file in dataframe format.
        dataframe = pd.read_excel(path, sheet_name=sheet, na_filter=False, dtype={"matricule": str})

        if progress_callback:
            progress_callback(0.1 * p)

        n = len(dataframe.to_dict("records"))
        for index, record in enumerate(dataframe.to_dict("records")):
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

            if progress_callback:
                progress_callback((0.1 + (index / n) * 0.9) * p)

        return records
