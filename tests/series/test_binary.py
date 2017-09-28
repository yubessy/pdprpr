from unittest import TestCase

from pandas import Series, DataFrame
from pandas.util.testing import assert_frame_equal

from pdprpr.series import BinarySeriesPreprocessor

from ..helper import array_uint8


class TestBinarySeriesPreprocessor(TestCase):
    def test_process(self):
        pp = BinarySeriesPreprocessor()
        target = Series([0, 1, float('nan')])
        result = pp.process(target)
        expected = DataFrame({
            'TRUE': array_uint8([0, 1, 1]),
        })
        assert_frame_equal(result, expected)

    def test_process_fillna(self):
        pp = BinarySeriesPreprocessor(fillna=True)
        target = Series([0, 1, float('nan')])
        result = pp.process(target)
        expected = DataFrame({
            'TRUE': array_uint8([0, 1, 1]),
        })
        assert_frame_equal(result, expected)
