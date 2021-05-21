# -*- coding: utf-8 -*-

import os
import yaml

VERSION = "1.0"

# configuration file
COL = "colonne_excel"
COL_PERSO = "colonne_perso"
COL_MISSION = "colonne_mission"
COL_CSV = "colonne_csv"
CONF_FILE = os.path.join(os.path.dirname(__file__), "conf", "conf.yaml")
with open(CONF_FILE, "rt", encoding="utf-8") as opened_file:
    CONFIG = yaml.safe_load(opened_file)

CONFIG[
    "buttonstyle"
] = """  QPushButton {
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

# Logo Apside
LOGO = os.path.join(os.path.dirname(__file__), "data", "apside-logo.png")

# DB file
DB_FILE = os.path.join(os.path.dirname(__file__), "db", "pydb.db")

# Translation directory
TRANSLATION_DIR = os.path.join(os.path.dirname(__file__), "data", "translations")

# README path
README_FILE = os.path.join(__file__, "..", "..", "..", "README.md")

# default parameters PDF
DEFAULT_FONT = ["Helvetica", 10]
PDF_COLOR = "#99ccff"  # Blue

# Colors analyse table
COLORS = {"others": "#FFA500"}

for i, color in enumerate(["#008000", "#32CD32", "#ADFF2F"]):
    COLORS[CONFIG["good_status"][i]] = color

for bad_status in CONFIG["bad_status"]:
    for substatus in bad_status:
        COLORS[substatus] = "#FFFF00"

TITLE_APP = "PYNDF"
COMPANY = "APSIDE"

# Title tabs
TAB_PRO = "process"
TAB_ANA = "analyse"
TAB_RW = "reader/writer"

# Icons
class ICONS:
    excel = "src\pyndf\data\icons\excel.png"
    csv = "src\pyndf\data\icons\csv.png"
    close = "src\pyndf\data\icons\close.png"
    fr = r"src\pyndf\data\icons\fr.png"
    help = "src\pyndf\data\icons\help.png"
    language = "src\pyndf\data\icons\language.png"
    output = "src\pyndf\data\icons\output.png"
    pdf = "src\pyndf\data\icons\pdf.png"
    en = "src\pyndf\data\icons\en.png"
    color = "src\pyndf\data\icons\color.png"
    manual = "src\pyndf\data\icons\manual.png"
