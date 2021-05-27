# -*- coding: utf-8 -*-

import os
import unittest
import tempfile
import shutil
from pyndf.process.writer.factory import Writer
from pyndf.constants import CONST


class TestPngWriter(unittest.TestCase):
    """Test Class"""

    @classmethod
    def setUpClass(cls):
        cls.directory = tempfile.mkdtemp()

    def setUp(self):
        pass

    def test_(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        # destroy tempdir
        shutil.rmtree(cls.directory, ignore_errors=True)
        cls.directory = None


if __name__ == "__main__":
    unittest.main()
