# -*- coding: utf-8 -*-

import re
import pandas as pd
from pyndf.gui.items.factory import Items
from pyndf.constants import CONST
from pyndf.process.reader.abstract import AbstractReader
from pyndf.process.data.records_manager import RecordsManager
from pyndf.utils import Utils


class ExcelReader(AbstractReader):
    """Class for reading excel file."""

    type = CONST.TYPE.EXC
    regex = re.compile(".*[.][xX][lL]*")
    record_regex = re.compile(".*DEPLACEMENT.*")

    def read(self, filename=None, sheet_name=0, progress=None, analyse=None, manager=None, type=None):
        if self.check_path(filename) is False:
            return

        # Get the data on excel file in dataframe format.
        dataframe = pd.read_excel(filename, sheet_name=sheet_name, na_filter=False)

        if progress is not None:
            progress.set_maximum(len(dataframe.to_dict("records")))

        if manager is None:
            manager = RecordsManager(log_level=self.log_level)

        for record in dataframe.to_dict("records"):
            keep_me = (
                self.record_regex.match(str(record.get(CONST.FILE.YAML[CONST.TYPE.EXC]["libelle"]))) is not None
                # For the global Excel -> colored the info from the csv.
                or record.get(CONST.FILE.YAML[CONST.TYPE.PDF]["nbr_km_mois"]) == "Inconnu"
            )

            if analyse:
                analyse(
                    Items(
                        type or self.type,
                        *list([Utils.type(r) for r in record.values()]),
                        columns=dataframe.columns,
                        colored=keep_me,
                        filename=filename,
                    )
                )
                continue

            if progress is not None:
                progress.send(msg=self.tr("Load EXCEL file"))

            if keep_me is False:
                continue

            manager.add_excel_record(record)

        return manager
