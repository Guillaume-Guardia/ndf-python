# -*- coding: utf-8 -*-

import unittest
from pyndf.process.data.progress import Progress


class TestProgress(unittest.TestCase):
    """Test Class"""

    @classmethod
    def setUpClass(cls):
        cls.msg = "test"

    def setUp(self):
        pass

    @staticmethod
    def custom_print(value, msg):
        return msg, value

    def test_progress_sub(self, maxi=1000):

        a = Progress(TestProgress.custom_print, 0, 10)
        a.set_maximum(maxi)
        for b in range(1, maxi):
            msg, value = a.send(msg=self.msg)

            self.assertEqual(msg, self.msg + f": {b} / {maxi}")
            self.assertEqual(value, round(b / maxi * 10))

    def test_progress_sub_max(self, maxi=500):
        a = Progress(TestProgress.custom_print, 10, 20, maxi)

        for b in range(1, maxi):
            msg, value = a.send(msg=self.msg)

            self.assertEqual(msg, self.msg + f": {b} / {maxi}")
            self.assertEqual(value, round(10 + b / maxi * 10))

    def test_progress_sub_redefine_max(self, maxi=30):
        a = Progress(TestProgress.custom_print, 10, 20)
        a.send(50)

        a.set_maximum(maxi)

        for b in range(1, maxi):
            msg, value = a.send(msg=self.msg)

            self.assertEqual(msg, self.msg + f": {b} / {maxi}")
            self.assertEqual(value, round(15 + b / maxi * 5))

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()
