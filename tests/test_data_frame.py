from unittest import TestCase

from pandas import DataFrame
from pandas.util.testing import assert_frame_equal

from pdprpr import DataFramePreprocessor

from .helper import array_float, array_uint8


class TestDataFramePreprocessor(TestCase):
    def test_process(self):
        pp = DataFramePreprocessor([
            {'name': 'num', 'kind': 'numerical'},
            {'name': 'nul', 'kind': 'nullable'},
            {'name': 'bin', 'kind': 'binary'},
            {'name': 'cat', 'kind': 'categorical'},
            {'name': 'stp', 'kind': 'stepping', 'options': {
                'steps': [2, 4],
            }},
            {'name': 'reg', 'kind': 'regex', 'options': {
                'groups': [{'name': 'a', 'regex': r'a+'}],
            }},
        ])
        target = DataFrame({
            'num': [1, 3, float('nan')],
            'nul': [0, None, float('nan')],
            'bin': [0, 2, float('nan')],
            'cat': ['p', 'q', 'r'],
            'stp': [1, 3, 5],
            'reg': ['a', 'aa', 'b'],
        })
        result = pp.process(target)
        expected = DataFrame({
            'num__VALUE': array_float([0.0, 1.0, float('nan')]),
            'nul__NULL':  array_uint8([0, 1, 1]),
            'bin__TRUE':  array_uint8([0, 1, 1]),
            'cat__p': array_uint8([1, 0, 0]),
            'cat__q': array_uint8([0, 1, 0]),
            'cat__r': array_uint8([0, 0, 1]),
            'stp__0': array_uint8([1, 0, 0]),
            'stp__1': array_uint8([0, 1, 0]),
            'stp__2': array_uint8([0, 0, 1]),
            'reg__a': array_uint8([1, 1, 0]),
        }, columns=[
            'num__VALUE',
            'nul__NULL',
            'bin__TRUE',
            'cat__p', 'cat__q', 'cat__r',
            'stp__0', 'stp__1', 'stp__2',
            'reg__a',
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
