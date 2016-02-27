import unittest

from rcblog import utils


class TestUtils(unittest.TestCase):
    def test_difference_of_dictionaries(self):
        d1 = {'a': 'A', 'b': 'B'}
        d2 = {'a': 'A'}
        result = {'b': 'B'}
        self.assertEqual(utils.difference_of_dictionaries(d1, d2), result)

        self.assertEqual(utils.difference_of_dictionaries(d1, d1), {})

        self.assertEqual(utils.difference_of_dictionaries(d2, d1), {})
