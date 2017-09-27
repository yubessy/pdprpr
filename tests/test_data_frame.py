from unittest import TestCase

from pandas import DataFrame
from pandas.util.testing import assert_frame_equal

from pdprpr import DataFramePreprocessor

from .helper import array_float, array_uint8


class TestDataFramePreprocessor(TestCase):
    def test_process(self):
        pp = DataFramePreprocessor([
            {'name': 'n', 'kind': 'numerical'},
            {'name': 'c', 'kind': 'categorical'},
            {'name': 'b', 'kind': 'binary'},
            {'name': 's', 'kind': 'stepping', 'steps': [2, 4]},
            {'name': 'r', 'kind': 'regex', 'groups': [
                {'name': 'a', 'regex': r'a+'},
            ]},
        ])
        target = DataFrame({
            'n': [1, 3, float('nan')],
            'c': ['P', 'Q', 'R'],
            'b': [0, 0, 1],
            's': [1, 3, 5],
            'r': ['a', 'aa', 'b'],
        })
        result = pp.process(target)
        expected = DataFrame({
            'n/value': array_float([0.0, 1.0, float('nan')]),
            'c/P': array_uint8([1, 0, 0]),
            'c/Q': array_uint8([0, 1, 0]),
            'c/R': array_uint8([0, 0, 1]),
            'b/True': array_uint8([0, 0, 1]),
            'b/False': array_uint8([1, 1, 0]),
            's/~2-': array_uint8([1, 0, 0]),
            's/2~4-': array_uint8([0, 1, 0]),
            's/4~': array_uint8([0, 0, 1]),
            'r/a': array_uint8([1, 1, 0]),
        }, columns=[
            'n/value', 'c/P', 'c/Q', 'c/R', 'b/False', 'b/True',
            's/2~4-', 's/4~', 's/~2-', 'r/a',
        ])
        assert_frame_equal(result, expected)

    def test_process_ignore_unknown_columns(self):
        pp = DataFramePreprocessor([{'name': 'n', 'kind': 'numerical'}])
        target = DataFrame({
            'n': [1, 3, float('nan')],
            'x': [..., ..., ...],
        })
        result = pp.process(target)
        expected = DataFrame({'n/value': array_float([0, 1, float('nan')])})
        assert_frame_equal(result, expected)

    def test_process_fail_when_columns_do_not_exist(self):
        pp = DataFramePreprocessor([{'name': 'n', 'kind': 'numerical'}])
        target = DataFrame({'x': [..., ..., ...]})
        with self.assertRaises(KeyError):
            pp.process(target)
