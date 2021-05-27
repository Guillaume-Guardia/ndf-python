# -*- coding: utf-8 -*-

import os
import unittest
import tempfile
import shutil
from collections import defaultdict
from pyndf.process.reader.factory import Reader
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
        cls.headers = CONST.FILE.YAML[CONST.TYPE.CSV]

        for i in range(10):
            cls.headers[f"montant{i}"] = CONST.FILE.YAML[CONST.TYPE.CSV]["montant"] + str(i)

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
        for row in range(self.n_rows):
            for header in self.headers.values():
                if self.reader.record_regex.match(header):
                    value = row * 10
                elif header == self.headers["matricule"]:
                    value = row
                else:
                    value = row, header
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

    def test_read(self):
        records = Reader(self.filename)

        for row in range(self.n_rows):
            value = 0
            for header in self.headers.values():
                if self.reader.record_regex.match(header):
                    value += row * 10
            self.assertEqual(records[row], value)

    def tearDown(self):
        os.remove(self.filename)

    @classmethod
    def tearDownClass(cls):
        # destroy tempdir
        shutil.rmtree(cls.directory, ignore_errors=True)
        cls.directory = None


if __name__ == "__main__":
    unittest.main()
