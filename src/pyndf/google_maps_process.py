#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import googlemaps
import pandas as pd
from pyndf.logbook import Logger


class DistanceMatrixAPI(Logger):
    def __init__(self, configuration):
        super().__init__()
        self.configuration = configuration
        self.key = "AIzaSyBxHUFfYitI-doxwvyAv04rJwop13ktzcM"
        self.language = "fr"
        self.mode = configuration["mode"]["DRIVING"]
        self.unit = configuration["units"]["METERS"]
        self.client = googlemaps.Client(self.key)

    def format_address(self, addr):
        reg = re.compile(r"(?P<road>^.*)(?P<zipcode> \d{5})(?P<city>.*$)")
        match = reg.match(addr)
        if match is not None:
            road = match.groupdict()["road"].strip()
            code = match.groupdict()["zipcode"].strip()
            city = match.groupdict()["city"].strip().upper()
            return ",".join([road, code, city])
        return ""

    def run(self, origin, destination):
        origin = self.format_address(origin)
        destination = self.format_address(destination)

        dict_params = dict(
            origins=origin,
            destinations=destination,
            language=self.language,
            mode=self.mode,
            units=self.unit,
        )

        result = self.client.distance_matrix(**dict_params)
        self.log.info(result)

        # Check status result
        top_status = result["status"]

        if top_status != self.configuration["status"]["OK"]:
            self.log.warning(f"Resultat pas ok: {top_status}")

        # Informations sur le trajet : duree et distance "elements"
        # Check status element
        element = result["rows"][0]["elements"][0]
        element_status = element["status"]

        if element_status != self.configuration["status"]["OK"]:
            self.log.warning(f"Element not OK: {element_status}")
            self.log.warning("Lieu(x) introuvable(s)")

        # conversion de m en km
        distance = element["distance"]["value"] / 1000
        duration = element["duration"]["value"]

        return distance, duration
