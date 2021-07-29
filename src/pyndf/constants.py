# -*- coding: utf-8 -*-

import os
from dataclasses import dataclass
import yaml

DIR = os.path.dirname(__file__)


class CONST:
    """Constantes ojbect. Shorcut to add constante in other file."""

    TITLE_APP = "PYNDF"
    COMPANY = "APSIDE"
    VERSION = "1.2"
    OPTI = True

    class FILE:
        """All important file"""

        DB = os.path.join(DIR, "db", "pydb.db")
        TRANSLATION_DIR = os.path.join(DIR, "data", "translations")
        README = os.path.join(DIR, "..", "..", "README.md")
        LOGO = os.path.join(DIR, "data", "apside-logo.png")
        CONF = os.path.join(DIR, "conf", "conf.yaml")
        with open(CONF, "rt", encoding="utf-8") as opened_file:
            YAML = yaml.safe_load(opened_file)

    class EXT:
        """All extension in app."""

        CSV = ".csv"
        EXC = ".xlsx"
        PDF = ".pdf"
        QM = ".qm"
        TS = ".ts"
        PNG = ".png"

    class TYPE:
        """String use in app to represent one type."""

        # Analyse
        ALL = "all"
        API = "api"
        PDF = "pdf"
        TOT = "total"

        # RW
        CSV = "csv"
        EXC = "excel"
        GLO_EXC = "global_excel"
        PNG = "png"

        # Process
        PRO = "process"

        # Others
        OUT = "output"
        COL = "color"
        LAN = "language"
        DB = "use_db"
        CACHE = "use_cache"
        USE_API = "use_api"
        USE_MULTITHREAGING = "use_multithreading"
        SAVE_TMP_FILE = "save_tmp_file"
        OVERWRITE = "overwrite"
        AGENCE = "agence"
        DEV_MODE = "dev_mode"

        # DB
        DB_CLIENT = "client"
        DB_EMPLOYEE = "employee"
        DB_MEASURE = "measure"

    MEMORY = TYPE.EXC, TYPE.CSV, TYPE.OUT, TYPE.COL, TYPE.DB, TYPE.CACHE

    class UI:
        """All visual parameters"""

        class ICONS:
            excel = os.path.join(DIR, r"data\icons\excel.png")
            csv = os.path.join(DIR, r"data\icons\csv.png")
            CLO = os.path.join(DIR, r"data\icons\close.png")
            fr = os.path.join(DIR, r"data\icons\fr.png")
            HEL = os.path.join(DIR, r"data\icons\help.png")
            LAN = os.path.join(DIR, r"data\icons\language.png")
            output = os.path.join(DIR, r"data\icons\output.png")
            PDF = os.path.join(DIR, r"data\icons\pdf.png")
            en = os.path.join(DIR, r"data\icons\en.png")
            COL = os.path.join(DIR, r"data\icons\color.png")
            MAN = os.path.join(DIR, r"data\icons\manual.png")
            RIGHT = os.path.join(DIR, r"data\icons\right.png")
            LEFT = os.path.join(DIR, r"data\icons\left.png")
            PLUS = os.path.join(DIR, r"data\icons\plus.png")
            RED = os.path.join(DIR, r"data\icons\button-red.png")
            GREEN = os.path.join(DIR, r"data\icons\button-green.png")

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
        """All tabs name"""

        READER = ["csv", "excel"]
        ANALYSE = ["all", "api", "pdf", "global_excel"]
        DB = ["client", "employee", "measure"]

    class MENU:
        API_ACTIONS = ["use_cache", "use_api", "use_multithreading", "overwrite", "save_tmp_file"]

    class READER:
        """All constants links to reader."""

        CAN_ADD_ALL_FILES = True

        class EXC:
            COL_PERSO = ["nom", "matricule", "societe", "agence", "agence_o", "adresse_intervenant"]
            COL_MISSION = [
                "periode_production",
                "client",
                "adresse_client",
                "taux",
                "prix_unitaire",
                "total",
            ]

        class CSV:
            COL_PERSO = ["nom", "prenom", "matricule", "agence"]
            COL_MISSION = [
                "periode_production",
                "taux",
                "prix_unitaire",
                "total",
            ]

    class MetaClass(type):
        """metaclass for status class"""

        def __getattr__(cls, key):
            """Get status from STATUS class. If don't exists, create a new one with a red color.

            Args:
                key (string): name of the status

            Returns:
                Status: New or Old status
            """
            # check key
            total_status = []
            state = False

            splits = list(set(key.split("/")))

            if len(splits) > 1:
                for s in splits:
                    status = getattr(CONST.STATUS, s)
                    total_status.append(bool(status))
                state = all(total_status)
                key = "/".join(splits)

            attr = CONST.STATUS.Status(key, state)
            if len(splits) == 1:
                setattr(cls, key, attr)
            return attr

    class STATUS(metaclass=MetaClass):
        """Status function in app."""

        @dataclass
        class Status:
            name: str
            state: bool = False

            def __bool__(self):
                return self.state

            def __str__(self):
                return self.name

            @property
            def color(self):
                if self:
                    return "#008000"
                return "#A12312"

            @property
            def icon(self):
                if self:
                    return CONST.UI.ICONS.GREEN
                return CONST.UI.ICONS.RED

        OK = Status("OK", True)
        API = Status("API", True)
        CACHE = Status("CACHE", True)
        DB = Status("DB", True)

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
        """All constants related to writer."""

        class PDF:
            FONT = ["Helvetica", 10]
            COLOR = "#99ccff"  # Blue

            COL_PERSO = ["nom_intervenant", "matricule", "adresse_intervenant"]
            COL_MISSION = ["client", "periode_production", "adresse_client", "nbr_km_mois", "taux", "plafond", "total"]
            COL_MISSION_EXCEL = COL_MISSION[:4]
            COL_MISSION_CSV = COL_MISSION[4:]
            UNKNOWN = "Inconnu"
