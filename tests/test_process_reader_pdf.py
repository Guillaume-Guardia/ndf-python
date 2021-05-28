# -*- coding: utf-8 -*-

import os
import unittest
import tempfile
import shutil
from pyndf.process.reader.factory import Reader
from pyndf.process.writer.factory import Writer
from pyndf.process.reader.useclass.pdf import PdfReader
from pyndf.constants import CONST


class TestPdfReader(unittest.TestCase):
    """Test Class"""

    @classmethod
    def setUpClass(cls):
        """Before all tests"""
        cls.directory = tempfile.mkdtemp()
        cls.headers = CONST.FILE.YAML[CONST.TYPE.CSV]
        cls.date = "300012"
        cls.writer = Writer(CONST.TYPE.PDF, cls.date, CONST.WRITER.PDF.COLOR, directory=cls.directory)
        cls.reader = PdfReader()

    def setUp(self):
        """Before each test"""
        self.filename = self.create_pdf()

    def create_pdf(self):
        data = dict()
        data["matricule"] = "0150"
        data["agence"] = "BREST"

        (filename, status), time_spend = self.writer.write(data, data)
        return filename

    def test_check_path(self):
        result = self.reader.check_path("")
        self.assertFalse(result)

        result = self.reader.check_path(self.filename)
        self.assertTrue(result)

    def test_can_read(self):
        # No
        result = PdfReader.can_read("")
        self.assertIsNone(result)

        # Yes
        result = PdfReader.can_read(self.filename)
        self.assertEqual(result, CONST.TYPE.PDF)

    def test_read(self):
        # The reader create a png file
        png_paths, status = Reader(self.filename, temp_dir=self.directory, ratio=3)

        self.assertEqual(self.filename.replace(CONST.EXT.PDF, CONST.EXT.PNG), png_paths[0])

    def tearDown(self):
        os.remove(self.filename)

    @classmethod
    def tearDownClass(cls):
        # destroy tempdir
        shutil.rmtree(cls.directory, ignore_errors=True)
        cls.directory = None


if __name__ == "__main__":
    unittest.main()
