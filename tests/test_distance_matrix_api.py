# -*- coding: utf-8 -*-

import unittest
from pyndf.constants import CONFIG
from pyndf.process.distance import DistanceMatrixAPI


class TestDistanceMatrixAPI(unittest.TestCase):
    """Test Class"""

    @classmethod
    def setUpClass(cls):
        cls.api = DistanceMatrixAPI()

    def setUp(self):
        pass

    def test_api(self):
        origin = "7 Rue George Sand, 29200 Brest"
        destination = "90 Rue Ernest Hemingway, 29200 Brest"

        status, (distance, duration) = self.api.run(origin, destination)

        # Check status
        self.assertIn(status, CONFIG["good_status"])
        self.assertEqual(round(distance, 1), 2.0)
        self.assertEqual(round(duration / 60), 4)

    def test_extract_address(self):
        """test function"""
        examples = ["90 rue Ernest Hemingway 29200  BREST", "90 rue Ernest Hemingway CS85416  29200  BREST"]
        format_examples = ["90 rue Ernest Hemingway,29200,BREST", "90 rue Ernest Hemingway CS85416,29200,BREST"]
        for example, correction in zip(examples, format_examples):
            self.assertEqual(self.api.format_address(example), correction)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()
