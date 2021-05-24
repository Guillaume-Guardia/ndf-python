# -*- coding: utf-8 -*-

import unittest
from pyndf.process.progress import Progress


class TestProgress(unittest.TestCase):
    """Test Class"""

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def test_progress_sub(self):
        a = Progress(print, 0, 10)
        a.set_maximum(1000)

        for b in range(1000):
            a.send()

    def test_progress_sub_max(self):
        a = Progress(print, 10, 20, 500)

        for b in range(500):
            a.send()

    def test_progress_sub_redefine_max(self):
        a = Progress(print, 10, 20)
        a.send(50)

        a.set_maximum(30)

        for b in range(30):
            a.send()

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()
