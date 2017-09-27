from unittest import TestCase

from pandas import Series, DataFrame
from pandas.util.testing import assert_frame_equal

from pdprpr import RegexSeriesPreprocessor

from ..helper import array_uint8


class RegexSeriesPreprocessorTest(TestCase):
    def test_process(self):
        pp = RegexSeriesPreprocessor(groups=[
            {'name': 'a1', 'regex': r'^a$'},
            {'name': 'an', 'regex': r'^a+$'},
        ])
        target = Series(['a', 'aa', 'b', float('nan')])
        result = pp.process(target)
        expected = DataFrame({
            'a1': array_uint8([1, 0, 0, 0]),
            'an': array_uint8([0, 1, 0, 0]),
        })
        assert_frame_equal(result, expected)
