# -*- coding: utf-8 -*-

import re
import googlemaps
from pyndf.logbook import Logger, log_time
from pyndf.constants import CONFIG
from pyndf.db.session import db
from pyndf.db.client import Client
from pyndf.db.employee import Employee
from pyndf.db.measure import Measure


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
    def run(self, client_address, employee_address):
        """Start the process google matrix api.

        Args:
            client_address (string): client_address to evaluate.
            employee_address (string): employee_address to evaluate.

        Returns:
            (tuple): Returned the result of API: distance between the client_address and employee_address with duration.
        """
        self.log.debug(f"Start calcul the distance between {client_address} and {employee_address}.")
        client_address = self.format_address(client_address)
        employee_address = self.format_address(employee_address)

        # Check cache
        if (client_address, employee_address) in self._cache:
            self.log.info(
                f"Status: {CONFIG['good_status'][1]} || Result: {self._cache[(client_address, employee_address)]}"
            )
            return CONFIG["good_status"][1], self._cache[(client_address, employee_address)]

        # Check DB
        with db.session_scope() as session:
            measure = (
                session.query(Measure)
                .filter(Measure.client_address == client_address)
                .filter(Measure.employee_address == employee_address)
                .first()
            )
            self.log.info(f"Result measure in DB: {measure}")

            if measure:
                # Add in cache
                self._cache[(client_address, employee_address)] = (measure.distance, measure.duration)

                self.log.info(f"Status: {CONFIG['good_status'][2]} || Result: {(measure.distance, measure.duration)}")
                return CONFIG["good_status"][2], (measure.distance, measure.duration)

        dict_params = dict(
            origins=client_address,
            destinations=employee_address,
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

        # Add in cache
        self._cache[(client_address, employee_address)] = distance, duration

        # Add in DB
        with db.session_scope() as session:
            # Check if client or employee exists
            new_client = Client(address=client_address)
            new_employee = Client(address=employee_address)
            add_measure = False

            if session.query(Client).filter(Client.address == client_address).first() is None:
                session.add(new_client)
                add_measure = True

            if session.query(Employee).filter(Employee.address == employee_address).first() is None:
                session.add(new_employee)
                add_measure = True

            session.flush()

            if add_measure:
                new_measure = Measure(
                    client_address=client_address,
                    employee_address=employee_address,
                    distance=distance,
                    duration=duration,
                )
                session.add(new_measure)

        self.log.info(f"Status: {element_status} || Result: {(distance, duration)}")
        return element_status, (distance, duration)