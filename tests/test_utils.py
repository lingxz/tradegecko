import unittest
from app.utils import apply_changes


class UtilTests(unittest.TestCase):

    def test_apply_changes(self):
        original = {
            'prop1': 'value1',
            'prop2': 'value2'
        }
        change = {
            'prop2': 'value3'
        }
        result = apply_changes(original, change)
        expected = {
            'prop1': 'value1',
            'prop2': 'value3',
        }
        self.assertDictEqual(expected, result)