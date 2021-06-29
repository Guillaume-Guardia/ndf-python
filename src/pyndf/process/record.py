# -*- coding: utf-8 -*-
import re
from pyndf.constants import CONST
from pyndf.logbook import Logger
from pyndf.utils import Utils


class Indemnite(Logger, Utils):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.total = 0
        self.quantite_payee = 0

    @property
    def plafond(self):
        if self.quantite_payee > 0:
            return round(self.total / self.quantite_payee, 2)
        return 0


class Mission(Indemnite):
    def __init__(self, parent, record, **kwargs):
        # Pylint args init
        super().__init__(**kwargs)
        self.distance = 0
        self.duration = 0
        self.km = 0

        for key in CONST.READER.EXC.COL_MISSION:
            setattr(self, key, record.get(parent.excel_mapper[key], 0))
            self.log.debug(f"{parent.matricule} | {key:15} = {getattr(self, key)}")

    def set_api_result(self, result):
        if result is None:
            return

        self.distance, self.duration = result
        self.km = round(self.quantite_payee * 2 * self.distance, 2)


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


class CsvRecord(Record):
    def __init__(self, record, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log.debug("Create CSV record")
        # Matricule + Nom + agence
        for key in CONST.READER.CSV.COL_PERSO:
            setattr(self, key, record.get(self.csv_mapper[key], CONST.WRITER.PDF.UNKNOWN))
            self.log.debug(f"{key:25} = {getattr(self, key)}")

    @property
    def nom_intervenant(self):
        return f"{self.nom.capitalize()} {self.prenom.capitalize()}"


class ExcelRecord(Record):
    def __init__(self, record, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log.debug("Create Excel record")
        # Personal info
        for key in CONST.READER.EXC.COL_PERSO:
            setattr(self, key, record.get(self.excel_mapper[key], CONST.WRITER.PDF.UNKNOWN))
            self.log.debug(f"{key:25} = {getattr(self, key)}")

    @property
    def nom_intervenant(self):
        name = self.nom.split()
        for index, s in enumerate(name):
            name[index] = s.capitalize()
        return " ".join(name)


class RecordsManager(Logger):
    def __init__(self, *args, matricule=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._records = {}
        self.matricule = Utils.type(matricule)

    def add_excel_record(self, record):
        matricule = Utils.type(record[CONST.FILE.YAML[CONST.TYPE.EXC]["matricule"]])

        # Check if not exist already
        if matricule not in self._records:
            # Create Excel record
            self._records[matricule] = ExcelRecord(record, log_level=self.log_level)
        self._records[matricule].add_mission(record)

    def add_csv_record(self, record, columns):
        matricule = Utils.type(record[CONST.FILE.YAML[CONST.TYPE.CSV]["matricule"]])

        # Check if not exist already
        if matricule not in self._records:
            # Create CSV record
            self._records[matricule] = CsvRecord(record, log_level=self.log_level)
        return self._records[matricule].add_indemnites(record, columns)

    def __iter__(self):
        if self.matricule is not None:
            # Take only the specific matricule
            return (r for r in [self._records[self.matricule]])
        # Else take all the records defined in self._records
        return (r for r in self._records.values() if len(r) > 0)

    def __len__(self):
        return sum([int(len(record) > 0) for record in self._records.values()])
