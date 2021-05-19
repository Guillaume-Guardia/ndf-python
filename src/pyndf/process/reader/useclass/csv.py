# -*- coding: utf-8 -*-

import math
import pandas as pd
from pyndf.logbook import log_time
from pyndf.constants import CONFIG
from pyndf.gui.items.useclass.reader.csv import CsvItem
from pyndf.process.reader.abstract import AbstractReader


class CSVReader(AbstractReader):
    """Class for reading csv file."""

    type = "CSV"

    @log_time
    def read(self, filename=None, analysed=None, just_read=False):
        if self.check_path(filename) is False:
            return

        # Initialisation variables
        records = {}

        # Get the data on csv file in dataframe format.
        dataframe = pd.read_csv(filename, sep=";", decimal=",")

        n = len(dataframe.to_dict("records"))
        for index, record in enumerate(dataframe.to_dict("records")):
            montant_total = 0
            analysed(CsvItem(*list(record.values())))

            if just_read:
                continue

            for i in range(1, 4):
                montant = record[CONFIG["colonne_csv"][f"montant{i}"]]
                if not math.isnan(montant):
                    montant_total += montant
            records[record[CONFIG["colonne_csv"]["matricule"]]] = round(montant_total, 2)

        return records
