# -*- coding: utf-8 -*-

import os
import unittest
import tempfile
import shutil
from collections import defaultdict
from pyndf.process.reader.factory import Reader
from pyndf.process.writer.factory import Writer
from pyndf.constants import CONST

counter = 0


class TestExcelReader(unittest.TestCase):
    """Test Class"""

    @classmethod
    def setUpClass(cls):
        """Before all tests"""
        cls.directory = tempfile.mkdtemp()
        cls.dico = CONST.FILE.YAML[CONST.TYPE.EXC]

    def setUp(self):
        """Before each test"""
        global counter

        counter += 1
        self.filename = os.path.join(self.directory, f"test_read_{counter}.xlsx")

    def create_xl(self, filename, oneperson=None, n_rows=10):
        headers = list(self.dico.values())

        data = defaultdict(list)
        for row in range(n_rows):
            for header in headers:
                if oneperson is not None and header == self.dico["matricule"]:
                    value = oneperson
                elif header == self.dico["libelle"]:
                    value = "DEPLACEMENT"
                else:
                    value = f"{row} {header}"

                data[header].append(value)

        writer = Writer(CONST.TYPE.EXC, directory=self.directory)
        (filename, status), time_spend = writer.write(data, filename)
        return filename

    def test_read(self):
        oneperson = "ALBERT"
        self.filename = self.create_xl(self.filename, oneperson=oneperson)
        records, status = Reader(self.filename)

        # Check the dict info
        # 1 person with matricule ALBERT and 10 missions
        self.assertEqual(len(records), 1)
        self.assertEqual(len(records[oneperson]["missions"]), 10)

    def test_read_big(self):
        oneperson = "ALBERT"
        self.filename = self.create_xl(self.filename, oneperson=oneperson, n_rows=1000)
        records, status = Reader(self.filename)

        # Check the dict info
        self.assertEqual(len(records), 1)
        self.assertEqual(len(records[oneperson]["missions"]), 1000)

    def test_read_change_matricule(self):
        self.filename = self.create_xl(self.filename)
        records, status = Reader(self.filename)

        # Check the dict info
        self.assertEqual(len(records), 10)
        for record in records.values():
            self.assertEqual(len(record["missions"]), 1)

    def tearDown(self):
        os.remove(self.filename)

    @classmethod
    def tearDownClass(cls):
        # destroy tempdir
        shutil.rmtree(cls.directory, ignore_errors=True)
        cls.directory = None


if __name__ == "__main__":
    unittest.main()
