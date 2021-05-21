# -*- coding: utf-8 -*-

import pandas as pd
from pyndf.logbook import log_time
from pyndf.constants import CONFIG, COL_CSV
from pyndf.gui.items.useclass.reader.csv import CsvItem
from pyndf.process.reader.abstract import AbstractReader
from pyndf.process.utils import Utils


class CSVReader(AbstractReader):
    """Class for reading csv file."""

    type = "csv"

    @log_time
    def read(self, filename=None, progress_callback=None, p=100, analyse_callback=None):
        if self.check_path(filename) is False:
            return

        if progress_callback:
            progress_callback(0.1 * p, self.tr("Load CSV file with pandas..."))

        # Initialisation variables
        records = {}

        # Get the data on csv file in dataframe format.
        dataframe = pd.read_csv(filename, sep=";", decimal=",", na_filter=False, encoding="latin1")

        n = len(dataframe.to_dict("records"))
        for index, record in enumerate(dataframe.to_dict("records")):
            if analyse_callback:
                analyse_callback(CsvItem(*list(record.values())))
                continue

            matricule = record[CONFIG[COL_CSV]["matricule"]]
            total = 0

            for i in range(1, 4):
                montant = Utils.type(record[CONFIG[COL_CSV][f"montant{i}"]], decimal=",")

                if isinstance(montant, (int, float)):
                    total += montant
            records[matricule] = round(total, 2)

            if progress_callback:
                progress_callback((0.1 + (index / n) * 0.9) * p, self.tr("Select info {} / {}".format(index, n)))

        return records
