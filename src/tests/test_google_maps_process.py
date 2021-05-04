# -*- coding: utf-8 -*-

import unittest
from pyndf.google_maps_process import DistanceMatrixAPI


class TestGoogleMapsProcess(unittest.TestCase):
    """Test Class

    Args:
        unittest (module): python module
    """

    @classmethod
    def setUpClass(cls):
        cls.examples = ["90 rue Ernest Hemingway 29200  BREST", "90 rue Ernest Hemingway CS85416  29200  BREST"]
        cls.format_examples = ["90 rue Ernest Hemingway,29200,BREST", "90 rue Ernest Hemingway CS85416,29200,BREST"]

        cls.test_class = DistanceMatrixAPI()

    def setUp(self):
        pass

    def test_extract_address(self):
        """test function"""
        for example, correction in zip(self.examples, self.format_examples):
            self.assertEqual(self.test_class.format_address(example), correction)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()
