# -*- coding: utf-8 -*-

import unittest
import tempfile
import shutil
from pyndf.utils import Utils
from pyndf.constants import CONST


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
        result = Utils.insert(path, path.index("."), "_page-5")
        self.assertEqual(result, "un/deux_page-5.pdf")

    def test_get_agence_from_yaml(self):
        self.assertEqual(CONST.FILE.YAML[CONST.TYPE.AGENCE]["NORD1"], "NORD 1|100 rue Nationale 59000 LILLE")
        agence, address = Utils.pretty_split(CONST.FILE.YAML[CONST.TYPE.AGENCE]["NORD1"])
        self.assertEqual(agence, "NORD 1")
        self.assertEqual(address, "100 rue Nationale 59000 LILLE")

    def test_get_date_from_file(self):
        path = "diuhzehzhoiezhz_150012yyezyuzgcyu"
        result = Utils.get_date_from_file(path)
        self.assertEqual(result.strftime("%Y%m"), "150012")

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        # destroy tempdir
        shutil.rmtree(cls.directory, ignore_errors=True)
        cls.directory = None


if __name__ == "__main__":
    unittest.main()
