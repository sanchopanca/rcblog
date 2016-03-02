import time
import unittest

from rcblog import crypto


class TestPasswordHash(unittest.TestCase):
    def test_make_hash(self):
        start = time.time()
        n = 10
        for i in range(n):
            crypto.make_hash('password')
        average_time = (time.time() - start) / n
        self.assertGreater(average_time, 0.2)

    def test_check_password(self):
        self.assertTrue(crypto.check_password('password', *crypto.make_hash('password')))
