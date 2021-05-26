# -*- coding: utf-8 -*-

import re
from collections import defaultdict
import pandas as pd
from pyndf.gui.items.factory import Items
from pyndf.constants import CONST
from pyndf.process.reader.abstract import AbstractReader


class ExcelReader(AbstractReader):
    """Class for reading excel file."""

    type = CONST.TYPE.EXC
    regex = re.compile(".*[.][xX][lL]*")

    def read(self, filename=None, sheet_name=0, progress=None, analyse_callback=None):
        if self.check_path(filename) is False:
            return

        # Initialisation variables
        records = defaultdict(dict)

        # Get the data on excel file in dataframe format.
        dataframe = pd.read_excel(filename, sheet_name=sheet_name, na_filter=False, dtype={"matricule": str})

        if progress:
            progress.set_maximum(len(dataframe.to_dict("records")))

        reg = re.compile("INDEMNITE.*")

        for record in dataframe.to_dict("records"):
            if analyse_callback:
                analyse_callback(Items(self.type, *list(record.values()), columns=dataframe.columns))
                continue

            if reg.match(str(record[CONST.FILE.YAML[CONST.TYPE.EXC]["libelle"]])) is None:
                continue

            matricule = record[CONST.FILE.YAML[CONST.TYPE.EXC]["matricule"]]

            if matricule not in records:
                # Personal info
                for key in CONST.READER.EXC.COL_PERSO:
                    records[matricule][key] = record[CONST.FILE.YAML[CONST.TYPE.EXC][key]]
                    self.log.debug(f"{matricule} | {key} = {records[matricule][key]}")
                records[matricule]["missions"] = []

            # Mission Info
            mission_record = {}
            for key in CONST.READER.EXC.COL_MISSION:
                mission_record[key] = record[CONST.FILE.YAML[CONST.TYPE.EXC][key]]
                self.log.debug(f"{matricule} | missions | {key} = {mission_record[key]}")
            records[matricule]["missions"].append(mission_record)

            if progress:
                progress.send(msg=self.tr("Load EXCEL file"))
        return records
