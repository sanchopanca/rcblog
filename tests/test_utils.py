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

    def test_parse_accept_language(self):
        result = utils.parse_accept_language('da, en-gb;q=0.8, en;q=0.7, ru;q=0.5')
        expected = ['dan', 'eng', 'rus']
        self.assertEqual(result, expected)
