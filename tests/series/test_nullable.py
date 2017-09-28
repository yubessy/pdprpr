from unittest import TestCase

from pandas import Series, DataFrame
from pandas.util.testing import assert_frame_equal

from pdprpr.series import NullableSeriesPreprocessor

from ..helper import array_uint8


class TestNullableSeriesPreprocessor(TestCase):
    def test_process(self):
        pp = NullableSeriesPreprocessor()
        target = Series([0, None, float('nan')])
        result = pp.process(target)
        expected = DataFrame({
            'NULL': array_uint8([0, 1, 1]),
        })
        assert_frame_equal(result, expected)

    def test_process_nullval_none(self):
        pp = NullableSeriesPreprocessor(nullval=None)
        target = Series([0, None, float('nan')])
        result = pp.process(target)
        expected = DataFrame({
            'NULL': array_uint8([0, 1, 0]),
        })
        assert_frame_equal(result, expected)

    def test_process_nullval_nan(self):
        pp = NullableSeriesPreprocessor(nullval=None)
        target = Series([0, None, float('nan')])
        result = pp.process(target)
        expected = DataFrame({
            'NULL': array_uint8([0, 0, 1]),
        })
        assert_frame_equal(result, expected)
