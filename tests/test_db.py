# -*- coding: utf-8 -*-

import re
import unittest
from pyndf.db.client import Client
from pyndf.db.session import db
from pyndf.utils import Utils


class TestDB(unittest.TestCase):
    """Test Class"""

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def test_get_clients(self):
        with db.session_scope() as session:
            clients = session.query(Client).all()
            self.assertGreater(len(clients), 0)

    def test_insert(self):
        agence_o = "BRES1"
        result = Utils.insert(agence_o, -1, "%")
        self.assertEqual("BRES%1", result)

    def test_get_client_agence_origin(self):
        agence_o = "BRES1"
        with db.session_scope() as session:
            client = session.query(Client).filter(Client.name.like(Utils.insert(agence_o, -1, "%"))).first()

            if client:
                self.assertEqual(client.name, "BREST 1")

    def test_get_client_agence_origin(self):
        agence_o = "HTITO"

        filter = Utils.insert(agence_o, -1, "%") + "%"

        with db.session_scope() as session:
            client = session.query(Client).filter(Client.name.like(filter)).first()

            if client:
                self.assertEqual(client.name, "HTI AUTO 3")

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()
