from unittest import TestCase

from pandas import Series, DataFrame
from pandas.util.testing import assert_frame_equal

from pdprpr import BinarySeriesPreprocessor

from ..helper import array_uint8


class TestBinarySeriesPreprocessor(TestCase):
    def test_process(self):
        pp = BinarySeriesPreprocessor()
        target = Series([0, 1, float('nan')])
        result = pp.process(target)
        expected = DataFrame({
            'True': array_uint8([0, 1, 0]),
            'False': array_uint8([1, 0, 0]),
        }, columns=['False', 'True'])
        assert_frame_equal(result, expected)

    def test_process_fillna(self):
        pp = BinarySeriesPreprocessor(fillna=False)
        target = Series([0, 1, float('nan')])
        result = pp.process(target)
        expected = DataFrame({
            'True': array_uint8([0, 1, 0]),
            'False': array_uint8([1, 0, 1]),
        }, columns=['False', 'True'])
        assert_frame_equal(result, expected)

    def test_process_default(self):
        pp = BinarySeriesPreprocessor(default=True)
        target = Series([0, 1, float('nan')])
        result = pp.process(target)
        expected = DataFrame({
            'False': array_uint8([1, 0, 0]),
            'nan': array_uint8([0, 0, 1]),
        }, columns=['False', 'nan'])
        assert_frame_equal(result, expected)
