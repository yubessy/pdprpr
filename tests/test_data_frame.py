from unittest import TestCase

from pandas import DataFrame
from pandas.util.testing import assert_frame_equal

from pdprpr import DataFramePreprocessor

from .helper import array_float, array_uint8


class TestDataFramePreprocessor(TestCase):
    def test_process(self):
        pp = DataFramePreprocessor([
            {'name': 'n', 'kind': 'numerical'},
            {'name': 'nul', 'kind': 'nullable'},
            {'name': 'c', 'kind': 'categorical'},
            {'name': 'b', 'kind': 'binary'},
            {'name': 's', 'kind': 'stepping', 'options': {
                'steps': [2, 4],
            }},
            {'name': 'r', 'kind': 'regex', 'options': {
                'groups': [{'name': 'a', 'regex': r'a+'}],
            }},
        ])
        target = DataFrame({
            'n': [1, 3, float('nan')],
            'nul': [0, None, float('nan')],
            'c': ['P', 'Q', 'R'],
            'b': [0, 0, 1],
            's': [1, 3, 5],
            'r': ['a', 'aa', 'b'],
        })
        result = pp.process(target)
        expected = DataFrame({
            'n__VALUE': array_float([0.0, 1.0, float('nan')]),
            'nul__NULL': array_uint8([0, 1, 1]),
            'c__P': array_uint8([1, 0, 0]),
            'c__Q': array_uint8([0, 1, 0]),
            'c__R': array_uint8([0, 0, 1]),
            'b__TRUE': array_uint8([0, 0, 1]),
            'b__FALSE': array_uint8([1, 1, 0]),
            's__0': array_uint8([1, 0, 0]),
            's__1': array_uint8([0, 1, 0]),
            's__2': array_uint8([0, 0, 1]),
            'r__a': array_uint8([1, 1, 0]),
        }, columns=[
            'n__VALUE', 'nul__NULL',
            'c__P', 'c__Q', 'c__R', 'b__FALSE', 'b__TRUE',
            's__0', 's__1', 's__2', 'r__a',
        ])
        assert_frame_equal(result, expected)

    def test_process_ignore_unknown_columns(self):
        pp = DataFramePreprocessor([{'name': 'n', 'kind': 'numerical'}])
        target = DataFrame({
            'n': [1, 3, float('nan')],
            'x': [..., ..., ...],
        })
        result = pp.process(target)
        expected = DataFrame({'n__VALUE': array_float([0, 1, float('nan')])})
        assert_frame_equal(result, expected)

    def test_process_fail_when_columns_do_not_exist(self):
        pp = DataFramePreprocessor([{'name': 'n', 'kind': 'numerical'}])
        target = DataFrame({'x': [..., ..., ...]})
        with self.assertRaises(KeyError):
            pp.process(target)
