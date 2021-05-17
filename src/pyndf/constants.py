# -*- coding: utf-8 -*-

import os
import yaml

# configuration file
COL = "colonne_excel"
COL_PERSO = "colonne_perso"
COL_MISSION = "colonne_mission"
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

# Colors analyse table
COLORS = {"others": "#FFA500"}

for i, color in enumerate(["#008000", "#32CD32", "#ADFF2F"]):
    COLORS[CONFIG["good_status"][i]] = color

for bad_status in CONFIG["bad_status"]:
    for substatus in bad_status:
        COLORS[substatus] = "#FFFF00"

# Title app
TITLE_APP = "PYNDF"

# Title tabs
TAB_PRO = "process"
TAB_ANA = "analyse"
