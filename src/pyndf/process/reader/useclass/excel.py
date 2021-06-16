# -*- coding: utf-8 -*-

import re
import pandas as pd
from pyndf.gui.items.factory import Items
from pyndf.constants import CONST
from pyndf.process.reader.abstract import AbstractReader
from pyndf.utils import Utils


class ExcelReader(AbstractReader):
    """Class for reading excel file."""

    type = CONST.TYPE.EXC
    regex = re.compile(".*[.][xX][lL]*")
    record_regex = re.compile(".*DEPLACEMENT.*")

    def read(self, filename=None, sheet_name=0, progress=None, analyse=None, manager=None):
        if self.check_path(filename) is False:
            return

        # Get the data on excel file in dataframe format.
        dataframe = pd.read_excel(filename, sheet_name=sheet_name, na_filter=False)

        if progress is not None:
            progress.set_maximum(len(dataframe.to_dict("records")))

        for record in dataframe.to_dict("records"):
            keep_me = self.record_regex.match(str(record[CONST.FILE.YAML[CONST.TYPE.EXC]["libelle"]])) is not None

            if analyse:
                analyse(
                    Items(
                        self.type,
                        *list([Utils.type(r) for r in record.values()]),
                        columns=dataframe.columns,
                        colored=keep_me,
                    )
                )
                continue

            if keep_me is False:
                continue

            if manager is not None:
                manager.add_excel_record(record)

            if progress is not None:
                progress.send(msg=self.tr("Load EXCEL file"))

        return manager
