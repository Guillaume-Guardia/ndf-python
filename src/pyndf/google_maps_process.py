# -*- coding: utf-8 -*-

import os
import re
import yaml
import googlemaps
from pyndf.logbook import Logger


class DistanceMatrixAPI(Logger):
    """Class which cover the API of google, adapted for ndf.

    Args:
        Logger (object): for logging in console.
    """

    _cache = {}

    def __init__(self, configuration=None):
        super().__init__()
        if configuration is None:
            # configuration file
            conf_file = os.path.join(os.path.dirname(__file__), "conf", "conf.yaml")

            with open(conf_file, "rt", encoding="utf-8") as opened_file:
                configuration = yaml.safe_load(opened_file)

        self.configuration = configuration
        self.key = "AIzaSyBxHUFfYitI-doxwvyAv04rJwop13ktzcM"
        self.language = "fr"
        self.mode = configuration["mode"]["DRIVING"]
        self.unit = configuration["units"]["METERS"]
        self.client = googlemaps.Client(self.key)

    def format_address(self, addr):
        """Formatter of addresses. Each address is returned like:
        - ROAD, ZIPCODE, CITY

        Args:
            addr (string): addresse to format

        Returns:
            string: formatted addresse or "" if no match with the regex.
        """
        reg = re.compile(r"(?P<road>^.*)(?P<zipcode> \d{5})(?P<city>.*$)")
        match = reg.match(addr)
        if match is not None:
            road = match.groupdict()["road"].strip()
            code = match.groupdict()["zipcode"].strip()
            city = match.groupdict()["city"].strip().upper()
            return ",".join([road, code, city])
        return ""

    def run(self, origin, destination):
        """Start the process google matrix api.

        Args:
            origin (string): origin to evaluate.
            destination (string): destination to evaluate.

        Returns:
            (tuple): Returned the result of API: distance between the origin and destination with duration.
        """
        origin = self.format_address(origin)
        destination = self.format_address(destination)

        if (origin, destination) in self._cache:
            self.log.info("Find in cache, not use the Google API!")
            return self._cache[(origin, destination)]

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

        self._cache[(origin, destination)] = distance, duration

        return distance, duration
