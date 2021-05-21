# -*- coding: utf-8 -*-

import re
from collections import defaultdict
import pandas as pd
from pyndf.logbook import log_time
from pyndf.constants import CONFIG, COL, COL_PERSO, COL_MISSION
from pyndf.gui.items.useclass.reader.excel import ExcelItem
from pyndf.process.reader.abstract import AbstractReader


class ExcelReader(AbstractReader):
    """Class for reading excel file."""

    type = "excel"

    @log_time
    def read(self, filename=None, sheet_name=0, progress_callback=None, p=100, analyse_callback=None):
        if self.check_path(filename) is False:
            return

        if progress_callback:
            progress_callback(0.1 * p, self.tr("Load Excel file with pandas..."))

        # Initialisation variables
        records = defaultdict(dict)

        # Get the data on excel file in dataframe format.
        dataframe = pd.read_excel(filename, sheet_name=sheet_name, na_filter=False, dtype={"matricule": str})

        n = len(dataframe.to_dict("records"))
        reg = re.compile("INDEMNITE.*")

        for index, record in enumerate(dataframe.to_dict("records")):
            if analyse_callback:
                analyse_callback(ExcelItem(*list(record.values())))
                continue

            if reg.match(str(record[CONFIG[COL]["libelle"]])) is None:
                continue

            matricule = record[CONFIG[COL]["matricule"]]

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
                progress_callback((0.1 + (index / n) * 0.9) * p, self.tr("Select info {} / {}".format(index, n)))
        return records
