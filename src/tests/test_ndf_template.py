# -*- coding: utf-8 -*-

import unittest
from pyndf.ndf_template import NdfTemplate


class TestAddress(unittest.TestCase):
    """Test Class

    Args:
        unittest (module): python module
    """

    @classmethod
    def setUpClass(cls):
        directory = r"C:\Users\guill\Documents\Projets\NDF_python\venv\src\output"
        cls.template = NdfTemplate(directory=directory)

        cls.data = {
            "nom": "Moise",
            "matricule": 261,
            "societe": "APSID",
            "agence": "BRES1",
            "agence_o": "BRES1",
            "adresse_intervenant": "140 BIS RUE ROBESPIERRE 29200 BREST",
            "missions": [
                {
                    "client": "BREST 1",
                    "periode_production": "2020-12",
                    "adresse_client": "90 rue Ernest Hemingway 29200 BREST",
                    "quantite_payee": 12,
                    "prix_unitaire": 5.4,
                    "total": 64.8,
                    "nbrkm_mois": 92.85600000000001,
                    "forfait": 0.697854742827604,
                },
                {
                    "client": "BREST 2",
                    "periode_production": "2020-12",
                    "adresse_client": "8 rue truc muche 29200 BREST",
                    "quantite_payee": 8,
                    "prix_unitaire": 4.8,
                    "total": 80,
                    "nbrkm_mois": 85,
                    "forfait": 0.35,
                },
            ],
        }

    def setUp(self):
        pass

    def test_create_table_collaborator(self):
        """test function."""
        self.template.create_table_collaborator(self.data)

    def test_create_table_missions(self):
        """test function."""
        self.template.create_table_missions(self.data)

    def test_create(self):
        """test function."""
        self.template.create(self.data)

    def test_check_path(self):
        """test function."""
        # Check if transform path
        path = ""
        test_path = self.template.check_path(path)
        self.assertEqual(path, test_path)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.template = None
        cls.data = None


if __name__ == "__main__":
    unittest.main()
