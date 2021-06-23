# -*- coding: utf-8 -*-

import unittest
from pyndf.constants import CONST
from pyndf.utils import Utils


class TestReadYaml(unittest.TestCase):
    """Test Class"""

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def test_read_yaml(self):
        self.assertEqual(Utils.dict2obj(CONST.FILE.YAML).csv.montant, "Montant salarial Ind. Déplac.")

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()
