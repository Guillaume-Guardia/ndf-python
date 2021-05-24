# -*- coding: utf-8 -*-

import os
import unittest
import tempfile
import shutil
from pyndf.utils import Utils


class TestPath(unittest.TestCase):
    """Test Class"""

    @classmethod
    def setUpClass(cls):
        cls.directory = tempfile.mkdtemp()

    def setUp(self):
        pass

    def test_insert_on_path(self):
        """test function."""
        path = "un/deux.pdf"
        result = Utils.insert(path, path.index("."), f"_page-5")
        self.assertEqual(result, "un/deux_page-5.pdf")

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        # destroy tempdir
        shutil.rmtree(cls.directory, ignore_errors=True)
        cls.directory = None


if __name__ == "__main__":
    unittest.main()
