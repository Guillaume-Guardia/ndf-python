# -*- coding: utf-8 -*-

import os
import yaml
from dataclasses import dataclass

DIR = os.path.dirname(__file__)


class CONST:
    TITLE_APP = "PYNDF"
    COMPANY = "APSIDE"
    VERSION = "1.0"

    class FILE:
        DB = os.path.join(DIR, "db", "pydb.db")
        TRANSLATION_DIR = os.path.join(DIR, "data", "translations")
        README = os.path.join(DIR, "..", "..", "README.md")
        LOGO = os.path.join(DIR, "data", "apside-logo.png")
        CONF = os.path.join(DIR, "conf", "conf.yaml")
        with open(CONF, "rt", encoding="utf-8") as opened_file:
            YAML = yaml.safe_load(opened_file)

    class EXT:
        CSV = ".csv"
        EXC = ".xlsx"
        PDF = ".pdf"
        QM = ".qm"
        TS = ".ts"

    class TYPE:
        # Analyse
        ALL = "all"
        API = "api"
        PDF = "pdf"
        TOT = "total"

        # RW
        CSV = "csv"
        EXC = "excel"

        # Process
        PRO = "process"

        # Others
        OUT = "output"
        COL = "color"
        LAN = "language"

    MEMORY = TYPE.EXC, TYPE.CSV, TYPE.OUT, TYPE.COL

    class UI:
        class ICONS:
            excel = os.path.join(DIR, "data\icons\excel.png")
            csv = os.path.join(DIR, "data\icons\csv.png")
            CLO = os.path.join(DIR, "data\icons\close.png")
            fr = os.path.join(DIR, "data\icons\fr.png")
            HEL = os.path.join(DIR, "data\icons\help.png")
            LAN = os.path.join(DIR, "data\icons\language.png")
            output = os.path.join(DIR, "data\icons\output.png")
            PDF = os.path.join(DIR, "data\icons\pdf.png")
            en = os.path.join(DIR, "data\icons\en.png")
            COL = os.path.join(DIR, "data\icons\color.png")
            MAN = os.path.join(DIR, "data\icons\manual.png")

        BUTTONSTYLE = """  QPushButton {
                background-color: #79bbff;
                border-radius: 10px;
                border-style: solid;
                border-width: 2px;
                font-size: 12px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #378de5;
                border-width: 2px;
                border-radius: 10px;
                border-color: #378de5;
            }
            """

    class TAB:
        READER = ["csv", "excel"]
        ANALYSE = ["all", "api", "pdf"]

    class READER:
        class EXC:
            COL_PERSO = ["nom", "matricule", "societe", "agence", "agence_o", "adresse_intervenant"]
            COL_MISSION = [
                "periode_production",
                "client",
                "adresse_client",
                "quantite_payee",
                "prix_unitaire",
                "total",
            ]

    class MetaClass(type):
        def __getattr__(cls, key):
            # check key
            total_status = []
            kwargs = {}
            splits = key.split("/")
            if len(splits) > 1:
                for s in splits:
                    status = getattr(CONST.STATUS, s)
                    total_status.append(bool(status))

                if all(total_status):
                    kwargs["COLOR"] = CONST.STATUS.OK.COLOR
                    kwargs["STATE"] = True

            attr = CONST.STATUS.Status(key, **kwargs)
            if len(splits) == 1:
                setattr(cls, key, attr)
            return attr

    class STATUS(metaclass=MetaClass):
        @dataclass
        class Status:
            NAME: str
            COLOR: str = "#A12312"
            STATE: bool = False

            def __bool__(self):
                return self.STATE

        OK = Status("OK", "#008000", True)
        CACHE = Status("CACHE", "#32CD32", True)
        DB = Status("DB", "#ADFF2F", True)

        # NOK class
        BAD = [
            # BAD TOP
            "INVALID_REQUEST",  # indicates that the provided request was invalid.
            "MAX_ELEMENTS_EXCEEDED",  # > 100 elements by request
            "MAX_DIMENSIONS_EXCEEDED",  # rqt > 25 origins or 25 detinations
            "OVER_QUERY_LIMIT",  # > 1000 elements / second
            "REQUEST_DENIED",
            "UNKNOWN_ERROR",  # Server Error -> Try again.
            # indicates any of the following:
            # The API key is missing or invalid.
            # Billing has not been enabled on your account.
            # A self-imposed usage cap has been exceeded.
            # The provided method of payment is no longer valid (for example, a credit card has expired).
            "OVER_DAILY_LIMIT",
            # BAD ELEMENT
            "NOT_FOUND",  # indicates that the origin and/or destination of this pairing could not be geocoded.
            "ZERO_RESULTS",  # indicates no route could be found between the origin and destination.
            "MAX_ROUTE_LENGTH_EXCEEDED",  # indicates the requested route is too long and cannot be processed.
        ]

    class WRITER:
        class PDF:
            FONT = ["Helvetica", 10]
            COLOR = "#99ccff"  # Blue

            COL_PERSO = ["nom", "matricule", "adresse_intervenant"]
            COL_MISSION = ["client", "periode", "addresse_client", "nbrkm_mois", "taux", "plafond", "total"]

            UNKNOWN = "Inconnu"
