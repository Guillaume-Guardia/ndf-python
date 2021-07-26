# -*- coding: utf-8 -*-

import re
import unittest


class Test(unittest.TestCase):
    """Test Class"""

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def test_(self):
        regex = re.compile(r"^.*_(?P<matricule>\d{1,})_.*$")

        matricule = None
        match = regex.match("djdjdj_150_jdjddj")
        if match is not None:
            matricule = int(match.groupdict()["matricule"])

        self.assertEqual(matricule, 150)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()
