# -*- coding: utf-8 -*-

import os
import unittest
import tempfile
import shutil
from collections import defaultdict
from pyndf.process.reader.factory import Reader
from pyndf.process.data.records.abstract import Record
from pyndf.process.writer.factory import Writer
from pyndf.process.reader.useclass.csv import CsvReader
from pyndf.constants import CONST

counter = 0


class TestCsvReader(unittest.TestCase):
    """Test Class"""

    @classmethod
    def setUpClass(cls):
        """Before all tests"""
        cls.directory = tempfile.mkdtemp()

        # Create headers
        cls.headers = CONST.FILE.YAML[CONST.TYPE.CSV]
        for i in range(10000, 10010):
            cls.headers[f"montant{i}"] = CONST.FILE.YAML[CONST.TYPE.CSV]["montant"] + str(i)
            cls.headers[f"nombre{i}"] = CONST.FILE.YAML[CONST.TYPE.CSV]["nombre"] + str(i)

        cls.writer = Writer(CONST.TYPE.CSV, directory=cls.directory)
        cls.reader = CsvReader()

    def setUp(self):
        """Before each test"""
        global counter

        counter += 1
        filename = os.path.join(self.directory, f"test_read_{counter}.csv")
        self.n_rows = 10
        self.filename = self.create_csv(filename)

    def create_csv(self, filename):
        data = defaultdict(list)
        for matricule in range(self.n_rows):
            for header in self.headers.values():
                if Record.regexes["total"].match(header):
                    indice = Record.regexes["total"].match(header).groupdict()["indice"].strip()
                    value = f"{int(indice)}"
                elif Record.regexes["quantite_payee"].match(header):
                    indice = Record.regexes["quantite_payee"].match(header).groupdict()["indice"].strip()
                    value = f"{int(indice) / 1000}"
                elif header == self.headers["matricule"]:
                    value = matricule
                else:
                    value = f"{header}_{matricule}"
                data[header].append(value)
        (filename, status), time_spend = self.writer.write(data, filename)
        return filename

    def test_check_path(self):
        result = self.reader.check_path("")
        self.assertFalse(result)

        result = self.reader.check_path(self.filename)
        self.assertTrue(result)

    def test_can_read(self):
        # No
        result = CsvReader.can_read("")
        self.assertIsNone(result)

        # Yes
        result = CsvReader.can_read(self.filename)
        self.assertEqual(result, CONST.TYPE.CSV)

    def test_can_read_2(self):
        result, status = Reader("")
        self.assertIsNone(result)
        self.assertEqual(status, CONST.STATUS.CANT_READ)

    def test_read(self):
        manager_records, status = Reader(self.filename)
        for record in manager_records:
            for indice, indemnite in record.indemnites.items():
                self.assertEqual(indemnite.total, int(indice))
                self.assertEqual(indemnite.quantite_payee, int(indice) / 1000)

    def tearDown(self):
        os.remove(self.filename)

    @classmethod
    def tearDownClass(cls):
        # destroy tempdir
        shutil.rmtree(cls.directory, ignore_errors=True)
        cls.directory = None


if __name__ == "__main__":
    unittest.main()
