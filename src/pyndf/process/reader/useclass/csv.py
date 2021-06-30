# -*- coding: utf-8 -*-

import re
import pandas as pd
from pyndf.constants import CONST
from pyndf.gui.items.factory import Items
from pyndf.process.reader.abstract import AbstractReader
from pyndf.process.data.records_manager import RecordsManager
from pyndf.utils import Utils


class CsvReader(AbstractReader):
    """Class for reading csv file."""

    type = CONST.TYPE.CSV
    regex = re.compile(".*[.][cC][sS][vV]")

    def read(self, filename=None, progress=None, analyse=None, manager=None):
        if self.check_path(filename) is False:
            return

        # Get the data on csv file in dataframe format.
        dataframe = pd.read_csv(filename, sep=";", decimal=",", na_filter=False, encoding="latin1")

        # Progress Bar
        if progress:
            progress.set_maximum(len(dataframe.to_dict("records")))

        if manager is None:
            manager = RecordsManager(log_level=self.log_level)

        for record in dataframe.to_dict("records"):
            status = manager.add_csv_record(record, list(dataframe.columns))

            if analyse:
                analyse(
                    Items(
                        self.type,
                        *list([Utils.type(r) for r in record.values()]),
                        columns=dataframe.columns,
                        colored=status,
                    )
                )
                continue

            if progress is not None:
                progress.send(msg=self.tr("Load CSV file"))

        return manager
