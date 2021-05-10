# -*- coding: utf-8 -*-

import os
import yaml

COL = "colonne"
COL_PERSO = "colonne_perso"
COL_MISSION = "colonne_mission"

LOGO = os.path.join(os.path.dirname(__file__), "data", "apside-logo.png")

# configuration file
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
  }

  QPushButton:hover {
      background-color: #378de5;
      border-width: 2px;
      border-radius: 10px;
      border-color: #378de5;
  }
  """

# DB file
DB_FILE = os.path.join(os.path.dirname(__file__), "db", "pydb.db")

# Translation directory
TRANSLATION_DIR = os.path.join(os.path.dirname(__file__), "data", "translations")
