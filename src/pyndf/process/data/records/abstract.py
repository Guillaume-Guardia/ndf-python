# -*- coding: utf-8 -*-
import re
from pyndf.constants import CONST
from pyndf.logbook import Logger
from pyndf.utils import Utils
from pyndf.process.data.records.excel.mission import Indemnite, Mission


class Record(Logger, Utils):
    regexes = {
        "total": re.compile(r".*(?P<montant>Montant.*)(?P<indice>\d{5})"),
        "quantite_payee": re.compile(r".*(?P<quantite>Nombre.*)(?P<indice>\d{5})"),
    }
    csv_mapper = CONST.FILE.YAML[CONST.TYPE.CSV]
    excel_mapper = CONST.FILE.YAML[CONST.TYPE.EXC]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.indemnites = {}

        # Initialize missions
        self.missions = []

    def add_indemnites(self, record, columns):
        status = CONST.STATUS.NOT_OK
        for column in columns:
            # Montant + Quantite
            for key, regex in self.regexes.items():
                match = regex.match(column)
                if match is None:
                    continue

                indice = match.groupdict()["indice"].strip()
                if indice not in self.indemnites:
                    self.indemnites[indice] = Indemnite(log_level=self.log_level)

                setattr(self.indemnites[indice], key, Utils.type(record[column], decimal=",", default=0))
                if getattr(self.indemnites[indice], key) > 0:
                    status = CONST.STATUS.OK
        if not status:
            self.indemnites.clear()
        return status

    def prepare_for_pdf(self):
        self.remove_null_indemnite()
        self.check_if_agence_o_exist()

    def remove_null_indemnite(self):
        for key, indemnite in list(self.indemnites.items()):
            if indemnite.total == 0:
                self.indemnites.pop(key)

    def add_mission(self, record, status=None):
        mission = Mission(self, record, log_level=self.log_level)
        if status is not None:
            mission.status = status
        self.missions.append(mission)

    @property
    def pdf_missions(self):
        memory = []

        for mission in self.missions:
            if (mission.client, mission.adresse_client) not in memory:
                yield mission
                memory.append((mission.client, mission.adresse_client))

    def check_if_agence_o_exist(self):
        # Check agence d'origine/address are in missions:
        name, address = Utils.pretty_split(
            CONST.FILE.YAML[CONST.TYPE.AGENCE].get(self.agence_o, "|".join(2 * [CONST.WRITER.PDF.UNKNOWN]))
        )
        if name not in [mission.client for mission in self.missions]:
            mission = {
                self.excel_mapper["client"]: name,
                self.excel_mapper["adresse_client"]: address,
            }
            self.log.debug(f"Add Mission Agence o{mission}")
            self.add_mission(mission, CONST.STATUS.OK)

    @property
    def nbr_km_mois(self):
        nbr_km_mois = sum([mission.km for mission in self.missions])
        quantite = self.quantite_payee_mois(somme=True)
        if quantite > 0 and nbr_km_mois / quantite > 100:
            return f"> {100 * quantite}"
        return round(nbr_km_mois, 2)

    def quantite_payee_mois(self, somme=False):
        if somme:
            return round(sum([data.quantite_payee for data in self.indemnites.values()]), 2)
        return "\n".join([str(indem.quantite_payee) for indem in self.indemnites.values()])

    @property
    def total_mois(self):
        # return round(sum([data.total for data in self.indemnites.values()]), 2)
        return "\n".join([str(indem.total) for indem in self.indemnites.values()])

    @property
    def plafond_mois(self):
        # return round(self.total_mois / self.quantite_payee_mois, 2)
        return "\n".join([str(indem.plafond) for indem in self.indemnites.values()])

    def __len__(self):
        return len(self.missions) + len(self.indemnites)
