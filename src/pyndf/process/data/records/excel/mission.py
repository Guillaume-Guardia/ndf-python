# -*- coding: utf-8 -*-

from pyndf.constants import CONST
from pyndf.process.data.records.csv.indemnite import Indemnite


class Mission(Indemnite):
    def __init__(self, parent, record, **kwargs):
        # Pylint args init
        super().__init__(**kwargs)
        self.distance = 0
        self.duration = 0
        self.nbr_km_mois = 0

        for key in CONST.READER.EXC.COL_MISSION:
            setattr(self, key, record.get(parent.excel_mapper[key], 0))
            self.log.debug(f"{parent.matricule} | {key:15} = {getattr(self, key)}")

        if self.periode_production != 0:
            # Set it in record manager
            parent.parent.periode_production = self.periode_production

    def set_api_result(self, result):
        if result is None:
            return

        self.distance, self.duration = result
        self.nbr_km_mois = round(self.taux * 2 * self.distance, 2)
