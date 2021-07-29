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

        last_matricule = None

        # Get the data on excel file in dataframe format.
        dataframe = pd.read_excel(filename, sheet_name=sheet_name, na_filter=False)

        if progress is not None:
            progress.set_maximum(len(dataframe.to_dict("records")))

        if manager is None:
            manager = RecordsManager(log_level=self.log_level)

        for record in dataframe.to_dict("records"):
            if type is not None:
                # For the global Excel -> alternate colored with the key matricule
                matricule = record.get(CONST.FILE.YAML[CONST.TYPE.PDF]["matricule"])
                if last_matricule is None:
                    # Initialisation
                    last_matricule = matricule
                    colored = True

                if matricule != last_matricule:
                    colored = not colored
                last_matricule = matricule
            else:
                colored = (
                    self.record_regex.match(str(record.get(CONST.FILE.YAML[CONST.TYPE.EXC]["libelle"]))) is not None
                )

            if analyse:
                analyse(
                    Items(
                        type or self.type,
                        *list([Utils.type(r) for r in record.values()]),
                        columns=dataframe.columns,
                        colored=colored,
                        filename=filename,
                    )
                )
                continue

            if progress is not None:
                progress.send(msg=self.tr("Load EXCEL file"))

            if colored is False or type is not None:
                continue

            manager.add_excel_record(record)

        return manager
