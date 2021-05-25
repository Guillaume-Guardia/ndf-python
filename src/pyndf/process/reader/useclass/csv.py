# -*- coding: utf-8 -*-

import re
import pandas as pd
from pyndf.constants import CONST
from pyndf.gui.items.factory import Items
from pyndf.process.reader.abstract import AbstractReader
from pyndf.utils import Utils


class CSVReader(AbstractReader):
    """Class for reading csv file."""

    type = CONST.TYPE.CSV
    regex = re.compile(".*[.][cC][sS][vV]")

    def read(self, filename=None, progress=None, analyse_callback=None):
        if self.check_path(filename) is False:
            return

        # Initialisation variables
        records = {}

        # Get the data on csv file in dataframe format.
        dataframe = pd.read_csv(filename, sep=";", decimal=",", na_filter=False, encoding="latin1")

        if progress:
            progress.set_maximum(len(dataframe.to_dict("records")))

        for record in dataframe.to_dict("records"):
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

            if progress:
                progress.send(msg=self.tr("Load CSV file"))

        return records
