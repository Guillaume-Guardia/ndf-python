# -*- coding: utf-8 -*-

import os
import unittest
import tempfile
import shutil
import pandas as pd
from pyndf.reader.excel import ExcelReader
from pyndf.constants import CONFIG


class TestExcelReader(unittest.TestCase):
    """Test Class"""

    @classmethod
    def setUpClass(cls):
        """Before all tests"""
        cls.directory = tempfile.mkdtemp()
        cls.reader = ExcelReader()

    def create_xl(self, filename, n_rows=10, change_matricule=False):
        n_col = len(CONFIG["colonne"])
        list_df = list([[0 for i in range(n_col)] for j in range(n_rows)])
        for index, row in enumerate(list_df):
            if change_matricule:
                row[2] = index
            row[18] = "INDEMNITE"
        df = pd.DataFrame(list_df, columns=list(CONFIG["colonne"].values()))

        with pd.ExcelWriter(filename, engine="xlsxwriter") as writer:
            df.to_excel(writer, sheet_name="A")

    def setUp(self):
        """Before each test"""
        pass

    def test_read(self):
        filename = os.path.join(self.directory, "test_read.xlsx")
        self.create_xl(filename)
        records = self.reader.read(filename)

        # Check the dict info
        # 1 person with matricule 0 and 10 missions
        self.assertEqual(len(records), 1)
        self.assertEqual(len(records[0]["missions"]), 10)

    def test_read_big(self):
        filename = os.path.join(self.directory, "test_read_big.xlsx")
        self.create_xl(filename, n_rows=1000)

        records = self.reader.read(filename)

        # Check the dict info
        self.assertEqual(len(records), 1)
        self.assertEqual(len(records[0]["missions"]), 1000)

    def test_read_change_matricule(self):
        filename = os.path.join(self.directory, "test_read_change_matricule.xlsx")
        self.create_xl(filename, change_matricule=True)

        records = self.reader.read(filename)

        # Check the dict info
        self.assertEqual(len(records), 10)
        for record in records.values():
            self.assertEqual(len(record["missions"]), 1)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.reader = None
        cls.filename = None

        # destroy tempdir
        shutil.rmtree(cls.directory, ignore_errors=True)
        cls.directory = None


if __name__ == "__main__":
    unittest.main()
