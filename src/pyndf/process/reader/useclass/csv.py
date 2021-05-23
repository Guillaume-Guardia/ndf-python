# -*- coding: utf-8 -*-

import re
import pandas as pd
from pyndf.logbook import log_time
from pyndf.constants import CONST
from pyndf.gui.items.factory import Items
from pyndf.process.reader.abstract import AbstractReader
from pyndf.utils import Utils


class CSVReader(AbstractReader):
    """Class for reading csv file."""

    type = CONST.TYPE.CSV
    regex = re.compile(".*[.][cC][sS][vV]")

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
                analyse_callback(Items(self.type, *list(record.values())))
                continue

            matricule = record[CONST.FILE.YAML[CONST.TYPE.CSV]["matricule"]]
            total = 0

            for i in range(1, 4):
                montant = Utils.type(record[CONST.FILE.YAML[CONST.TYPE.CSV][f"montant{i}"]], decimal=",")

                if isinstance(montant, (int, float)):
                    total += montant
            records[matricule] = round(total, 2)

            if progress_callback:
                progress_callback((0.1 + (index / n) * 0.9) * p, self.tr("Select info {} / {}".format(index, n)))

        return records
