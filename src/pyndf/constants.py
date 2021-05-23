# -*- coding: utf-8 -*-

import os
import yaml
from dataclasses import dataclass


class CONST:
    TITLE_APP = "PYNDF"
    COMPANY = "APSIDE"
    VERSION = "1.0"

    class FILE:
        DIR = os.path.dirname(__file__)
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

    class UI:
        class ICONS:
            excel = "src\pyndf\data\icons\excel.png"
            csv = "src\pyndf\data\icons\csv.png"
            CLO = "src\pyndf\data\icons\close.png"
            fr = r"src\pyndf\data\icons\fr.png"
            HEL = "src\pyndf\data\icons\help.png"
            LAN = "src\pyndf\data\icons\language.png"
            output = "src\pyndf\data\icons\output.png"
            PDF = "src\pyndf\data\icons\pdf.png"
            en = "src\pyndf\data\icons\en.png"
            COL = "src\pyndf\data\icons\color.png"
            MAN = "src\pyndf\data\icons\manual.png"

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
            attr = CONST.STATUS.Status(key)
            setattr(cls, key, attr)
            return attr

    class STATUS(metaclass=MetaClass):
        @dataclass
        class Status:
            NAME: str
            COLOR: str = "#FFFF00"
            STATE: bool = False

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


if __name__ == "__main__":
    print(vars(CONST.STATUS))
    print(CONST.STATUS.N)
    print(vars(CONST.STATUS))
