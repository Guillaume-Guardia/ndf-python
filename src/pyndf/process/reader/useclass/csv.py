# -*- coding: utf-8 -*-

import re
import pandas as pd
from pyndf.constants import CONST
from pyndf.gui.items.factory import Items
from pyndf.process.reader.abstract import AbstractReader
from pyndf.utils import Utils


class CsvReader(AbstractReader):
    """Class for reading csv file."""

    type = CONST.TYPE.CSV
    regex = re.compile(".*[.][cC][sS][vV]")
    record_regex = re.compile("Montant salarial.*")

    def read(self, filename=None, progress=None, analyse=None):
        if self.check_path(filename) is False:
            return

        # Initialisation variables
        records = {}

        # Get the data on csv file in dataframe format.
        dataframe = pd.read_csv(filename, sep=";", decimal=",", na_filter=False, encoding="latin1")

        if progress:
            progress.set_maximum(len(dataframe.to_dict("records")))

        for record in dataframe.to_dict("records"):
            matricule = record[CONST.FILE.YAML[CONST.TYPE.CSV]["matricule"]]
            total = 0

            for column in list(dataframe.columns):
                if self.record_regex.match(column):
                    montant = Utils.type(record[column], decimal=",")

                    if isinstance(montant, (int, float)):
                        total += montant
            records[matricule] = round(total, 2)

            if analyse:
                analyse(
                    Items(
                        self.type,
                        *list([Utils.type(r) for r in record.values()]),
                        columns=dataframe.columns,
                        colored=records[matricule] > 0,
                    )
                )
                continue

            if progress:
                progress.send(msg=self.tr("Load CSV file"))

        return records
