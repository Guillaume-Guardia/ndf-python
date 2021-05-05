# -*- coding: utf-8 -*-

import re
import googlemaps
from pyndf.logbook import Logger, log_time
from pyndf.constants import CONFIG


class DistanceMatrixAPI(Logger):
    """Class which cover the API of google, adapted for ndf.

    Args:
        Logger (object): for logging in console.
    """

    _cache = {}

    def __init__(self):
        super().__init__()

        self.key = CONFIG["distance_params"]["key"]
        self.language = CONFIG["distance_params"]["language"]
        self.mode = CONFIG["distance_params"]["mode"]
        self.unit = CONFIG["distance_params"]["unit"]
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

    @log_time
    def run(self, origin, destination):
        """Start the process google matrix api.

        Args:
            origin (string): origin to evaluate.
            destination (string): destination to evaluate.

        Returns:
            (tuple): Returned the result of API: distance between the origin and destination with duration.
        """
        self.log.debug(f"Start calcul the distance between {origin} and {destination}.")
        origin = self.format_address(origin)
        destination = self.format_address(destination)

        if (origin, destination) in self._cache:
            self.log.info(f"Status: {CONFIG['good_status'][1]} || Result: {self._cache[(origin, destination)]}")
            return CONFIG["good_status"][1], self._cache[(origin, destination)]

        dict_params = dict(
            origins=origin,
            destinations=destination,
            language=self.language,
            mode=self.mode,
            units=self.unit,
        )
        result = self.client.distance_matrix(**dict_params)

        # Check status result
        top_status = result["status"]

        if top_status in CONFIG["bad_status"]["Top"]:
            self.log.warning(f"Status: {top_status} || Result: None")
            return top_status, None

        # Informations sur le trajet : duree et distance "elements"
        # Check status element
        element = result["rows"][0]["elements"][0]
        element_status = element["status"]

        if element_status in CONFIG["bad_status"]["Element"]:
            self.log.warning(f"Status: {element_status} || Result: None")
            return element_status, None

        # conversion de m en km
        distance = element["distance"]["value"] / 1000
        duration = element["duration"]["value"]

        self._cache[(origin, destination)] = distance, duration

        self.log.info(f"Status: {element_status} || Result: {(distance, duration)}")
        return element_status, (distance, duration)
