# -*- coding: utf-8 -*-

import unittest
from pyndf.constants import CONST
from pyndf.db.client import Client
from pyndf.db.employee import Employee
from pyndf.db.measure import Measure
from pyndf.process.distance import DistanceMatrixAPI
from pyndf.db.session import db


class TestDistanceMatrixAPI(unittest.TestCase):
    """Test Class"""

    @classmethod
    def setUpClass(cls):
        cls.api = DistanceMatrixAPI()

    def setUp(self):
        pass

    def test_format_address(self):
        """test function"""

        dico = [
            ("90 rue Ernest Hemingway 29200  BREST", "90 rue Ernest Hemingway,29200,BREST"),
            ("90 rue Ernest Hemingway CS85416  29200  BREST", "90 rue Ernest Hemingway CS85416,29200,BREST"),
            ("", ""),
            ("hcbuyczeyzye", "hcbuyczeyzye"),
            ("8 rue 15555           Brest", "8 rue,15555,BREST"),
            ("rue JD                  455555 45555 NS", "rue JD 455555,45555,NS"),
        ]

        for raw, result in dico:
            self.assertEqual(DistanceMatrixAPI.format_address(raw), result)

    def test_run(self):
        origin = "15000", "7 Rue George Sand, 29200 Brest"
        destination = "Apside", "90 Rue Ernest Hemingway, 29200 Brest"

        # Check API
        ((distance, duration), status), time_spend = self.api.run(origin, destination, use_db=False)

        # Check status
        self.assertEqual(status, CONST.STATUS.API)
        self.assertEqual(round(distance, 1), 2.1)
        self.assertEqual(round(duration / 60), 4)

        # Check Cache
        ((distance, duration), status), time_spend = self.api.run(origin, destination, use_db=False)

        # Check status
        self.assertEqual(status, CONST.STATUS.CACHE)
        self.assertEqual(round(distance, 1), 2.1)
        self.assertEqual(round(duration / 60), 4)

    def test_run_no_address(self):
        origin = "15000", ""  # No address
        destination = "Apside", "90 Rue Ernest Hemingway, 29200 Brest"
        # Check API
        (result, status), time_spend = self.api.run(origin, destination, use_db=False)

        # Check status
        self.assertEqual(status, CONST.STATUS.INVALID_REQUEST)
        self.assertEqual(result, None)

        # Check API
        (result, status), time_spend = self.api.run(destination, origin, use_db=False)

        # Check status
        self.assertEqual(status, CONST.STATUS.INVALID_REQUEST)
        self.assertEqual(result, None)

    def test_run_not_found(self):
        # indicates that the origin and/or destination of this pairing could not be geocoded.
        origin = "15000", "cgduyuyzyz uichsduicshd 78500 sdciucshui"
        destination = "Apside", "90 Rue Ernest Hemingway, 29200 Brest"
        # Check API
        (result, status), time_spend = self.api.run(origin, destination, use_db=False)

        # Check status
        self.assertEqual(status, CONST.STATUS.NOT_FOUND)
        self.assertEqual(result, None)

    def test_run_zero_results(self):
        # indicates no route could be found between the origin and destination.
        origin = "15000", "Statue de la Liberté, New York, NY 10004, États-Unis"
        destination = "Apside", "90 Rue Ernest Hemingway, 29200 Brest"
        # Check API
        (result, status), time_spend = self.api.run(origin, destination, use_db=False)

        # Check status
        self.assertEqual(status, CONST.STATUS.ZERO_RESULTS)
        self.assertEqual(result, None)

    def test_add_result_in_db(self):
        # indicates the requested route is too long and cannot be processed.
        client = Client(name="Atchoum", address="atchoum address")
        employee = Employee(matricule="150000", address="150000 address")
        distance = 15
        duration = 10.5

        DistanceMatrixAPI.add_result_in_db(
            client.name, client.address, employee.matricule, employee.address, distance, duration
        )

        # Check in db
        with db.session_scope() as session:
            db_client = session.query(Client).filter(Client.name == client.name).one()
            self.assertEqual(db_client.address, client.address)

            db_employee = session.query(Employee).filter(Employee.matricule == employee.matricule).one()
            self.assertEqual(db_employee.address, employee.address)

            # Check relation between employee and client
            self.assertListEqual(db_employee.clients, [db_client])
            self.assertListEqual(db_client.employees, [db_employee])

            db_measure = (
                session.query(Measure).filter(Measure.client == db_client).filter(Measure.employee == db_employee).one()
            )

            self.assertEqual(db_measure.distance, 15)
            self.assertEqual(db_measure.duration, 10.5)

        # Remove in db
        with db.session_scope() as session:
            db_client = session.query(Client).filter(Client.name == client.name).one()
            db_employee = session.query(Employee).filter(Employee.matricule == employee.matricule).one()
            db_measure = (
                session.query(Measure).filter(Measure.client == db_client).filter(Measure.employee == db_employee).one()
            )

            session.delete(db_client)
            session.delete(db_employee)
            session.delete(db_measure)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()
