# -*- coding: utf-8 -*-

import math
import pandas as pd
from pyndf.qtlib import QtCore
from pyndf.logbook import Logger, log_time
from pyndf.constants import CONFIG


class CSVReader(Logger, QtCore.QObject):
    """Class for reading csv file."""

    def __init__(self, filename=None):
        """Initialisation"""
        super().__init__()
        self.filename = filename

    @log_time
    def read(self, filename=None):
        # Initialisation variables
        records = {}

        path = filename or self.filename
        self.log.info(f"Extract Data in csv file: {path}")
        # Get the data on csv file in dataframe format.
        dataframe = pd.read_csv(path, sep=";", decimal=",")

        n = len(dataframe.to_dict("records"))
        for index, record in enumerate(dataframe.to_dict("records")):
            montant_total = 0
            for i in range(1, 4):
                montant = record[CONFIG["colonne_csv"][f"montant{i}"]]
                if not math.isnan(montant):
                    montant_total += montant
            records[record[CONFIG["colonne_csv"]["matricule"]]] = round(montant_total, 2)

        return records
