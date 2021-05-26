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
        Utils.getattr(CONST.STATUS, ["hh"])

    def test_property_for_class(self):
        class test:
            @property
            def test_(self):
                return "test"

        print(test.test_)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()
