# -*- coding: utf-8 -*-

import os
import unittest
import tempfile
import shutil
from pyndf.writer.pdf import PdfWriter
from pyndf.constants import CONFIG


class TestPdfWriter(unittest.TestCase):
    """Test Class"""

    @classmethod
    def setUpClass(cls):
        cls.directory = tempfile.mkdtemp()
        cls.writer = PdfWriter(directory=cls.directory)

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
                    "status": CONFIG["good_status"][0],
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
                    "status": CONFIG["good_status"][0],
                },
            ],
        }

    def setUp(self):
        pass

    def test_create_table_collaborator(self):
        """test function."""
        table = self.writer.create_table_collaborator(self.data)

        # Check table
        data = [
            ["Nom Prénom:", self.data["nom"]],
            ["Matricule:", self.data["matricule"]],
            ["Adresse:", self.data["adresse_intervenant"]],
        ]

        self.assertListEqual(table._cellvalues, data)

    def test_create_table_missions(self):
        """test function."""
        table = self.writer.create_table_missions(self.data)

        # Check number of row -> mission
        self.assertEqual(table._nrows, len(self.data["missions"]) + 1)

    def test_check_path(self):
        """test function."""
        # Check if transform path
        path = "un_path"
        test_path = self.writer.check_path(path)
        self.assertEqual(os.path.join(self.directory, path + ".pdf"), test_path)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.writer = None
        cls.data = None

        # destroy tempdir
        shutil.rmtree(cls.directory, ignore_errors=True)
        cls.directory = None


if __name__ == "__main__":
    unittest.main()
