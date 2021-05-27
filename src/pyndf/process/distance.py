# -*- coding: utf-8 -*-

import re
import googlemaps
from pyndf.logbook import Logger, log_time
from pyndf.constants import CONST
from pyndf.db.session import db
from pyndf.db.client import Client
from pyndf.db.employee import Employee
from pyndf.db.measure import Measure
from pyndf.utils import Utils


class DistanceMatrixAPI(Logger):
    """Class which cover the API of google, adapted for ndf.

    Args:
        Logger (object): for logging in console.
    """

    _cache = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        for key, value in CONST.FILE.YAML[CONST.TYPE.API].items():
            setattr(self, key, value)
        self.client = googlemaps.Client(self.key)

        self.log.info("Get distance with API or DB or cache from Excel file")

    @staticmethod
    def format_address(addr: str) -> str:
        """Formatter of addresses. Each address is returned like:
        - ROAD,ZIPCODE,CITY if match
        else:
            return the raw address

        Args:
            addr (string): addresse to format

        Returns:
            string: formatted addresse or "" if no match with the regex.
        """
        addr = Utils.pretty_join(addr)
        reg = re.compile(r"(?P<road>^.*)(?P<zipcode> \d{5} )(?P<city>.*$)")
        match = reg.match(addr)
        if match is not None:
            road = match.groupdict()["road"]
            code = match.groupdict()["zipcode"].strip()
            city = match.groupdict()["city"].upper()
            return ",".join([road, code, city])
        return addr

    @log_time
    def run(self, client, employee, use_db=True, use_cache=True, use_api=True):
        """Start the process google matrix api.

        Args:
            client_address (string): client_address to evaluate.
            employee_address (string): employee_address to evaluate.

        Returns:
            (tuple): Returned the result of API: distance between the client_address and employee_address with duration.
        """
        client_name, client_address = client
        employee_matricule, employee_address = employee
        self.log.debug(f"Get the distance between {client_address} and {employee_address}.")
        client_address = DistanceMatrixAPI.format_address(client_address)
        employee_address = DistanceMatrixAPI.format_address(employee_address)

        # Check cache
        if use_cache and (client_address, employee_address) in self._cache:
            self.log.debug(f"Status: {CONST.STATUS.CACHE} || Result: {self._cache[(client_address, employee_address)]}")
            return self._cache[(client_address, employee_address)], CONST.STATUS.CACHE

        # Check DB
        if use_db:
            with db.session_scope() as session:
                measure = (
                    session.query(Measure)
                    .filter(Measure.client_address == client_address)
                    .filter(Measure.employee_address == employee_address)
                    .first()
                )

                if measure:
                    # Add in cache
                    self._cache[(client_address, employee_address)] = (measure.distance, measure.duration)

                    self.log.debug(f"Status: {CONST.STATUS.DB} || Result: {(measure.distance, measure.duration)}")
                    return (measure.distance, measure.duration), CONST.STATUS.DB

        if not use_api:
            return None, CONST.STATUS.NO_USE_API

        dict_params = dict(
            origins=client_address,
            destinations=employee_address,
            language=self.language,
            mode=self.mode,
            units=self.unit,
        )
        try:
            result = self.client.distance_matrix(**dict_params)
        except googlemaps.exceptions.ApiError as error:
            self.log.warning(f"Status: {error.status} || Result: None")
            return None, getattr(CONST.STATUS, error.status)

        # Check status
        top_status = result["status"]
        element = result["rows"][0]["elements"][0]
        element_status = element["status"]

        for status in (top_status, element_status):
            status = getattr(CONST.STATUS, status)
            if not status:
                self.log.warning(f"Status: {status} || Result: None")
                return None, status

        # conversion de m en km
        distance = element["distance"]["value"] / 1000
        duration = element["duration"]["value"]

        # Add in cache
        if use_cache:
            self._cache[(client_address, employee_address)] = distance, duration

        # Add in DB
        if use_db:
            DistanceMatrixAPI.add_result_in_db(
                client_name, client_address, employee_matricule, employee_address, distance, duration, log=self.log
            )

        self.log.debug(f"Status: {CONST.STATUS.API} || Result: {(distance, duration)}")
        return (distance, duration), CONST.STATUS.API

    @staticmethod
    def add_result_in_db(
        client_name, client_address, employee_matricule, employee_address, distance, duration, log=None
    ):
        with db.session_scope() as session:
            # Check if client or employee exists
            new_client = Client(name=client_name, address=client_address)
            if session.query(Client).filter(Client.address == client_address).first() is None:
                if log:
                    log.debug(f"Add new client {new_client}")
                session.add(new_client)

            new_employee = Employee(matricule=employee_matricule, address=employee_address)
            if session.query(Employee).filter(Employee.address == employee_address).first() is None:
                if log:
                    log.debug(f"Add new employee {new_employee}")
                session.add(new_employee)

            session.flush()

            # Add relation between client and employee
            employee = session.query(Employee).filter(Employee.address == employee_address).first()
            client = session.query(Client).filter(Client.address == client_address).first()

            if client not in employee.clients:
                employee.clients.append(client)

            new_measure = Measure(
                client=client,
                employee=employee,
                distance=distance,
                duration=duration,
            )
            if log:
                log.debug(f"Add new measure {new_measure}")
            session.add(new_measure)
