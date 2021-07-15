# -*- coding: utf-8 -*-

from pyndf.logbook import Logger
from pyndf.utils import Utils


class Indemnite(Logger, Utils):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.total = 0
        self.taux = 0

    @property
    def plafond(self):
        if self.taux > 0:
            return round(self.total / self.taux, 2)
        return 0
