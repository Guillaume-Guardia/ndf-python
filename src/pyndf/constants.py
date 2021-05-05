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
