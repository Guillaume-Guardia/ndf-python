# -*- coding: utf-8 -*-

import unittest
from pyndf.constants import CONST
from pyndf.utils import Utils


class TestProgress(unittest.TestCase):
    """Test Class"""

    @classmethod
    def setUpClass(cls):
        cls.msg = "test"

    def setUp(self):
        pass

    def test_status_getattr(self):
        status = Utils.getattr(CONST.STATUS, ["hh"])

        self.assertEqual(status, CONST.STATUS.hh)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()
