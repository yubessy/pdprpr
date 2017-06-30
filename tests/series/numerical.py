from unittest import TestCase

from pandas import Series, DataFrame
from pandas.util.testing import assert_frame_equal

from pandas_preprocessing import NumericalSeriesPreprocessor

from ..helper import array_float, array_uint8


class NumericalSeriesPreprocessorTest(TestCase):
    def test_process(self):
        pp = NumericalSeriesPreprocessor()
        target = Series([1, 3, float('nan')])
        result = pp.process(target)
        expected = DataFrame({'value': array_float([0.0, 1.0, float('nan')])})
        assert_frame_equal(result, expected)

    def test_process_minmax(self):
        pp = NumericalSeriesPreprocessor(minv=2.0, maxv=4.0)
        target = Series([1, 2, 3, 4, 5])
        result = pp.process(target)
        expected = DataFrame({'value': array_float([0.0, 0.0, 0.5, 1.0, 1.0])})
        assert_frame_equal(result, expected)

    def test_process_without_normalize(self):
        pp = NumericalSeriesPreprocessor(normalize=False)
        target = Series([1, 3, float('nan')])
        result = pp.process(target)
        expected = DataFrame({'value': array_float([1.0, 3.0, float('nan')])})
        assert_frame_equal(result, expected)

    def test_process_fillna(self):
        pp = NumericalSeriesPreprocessor(fillna=0)
        target = Series([1, 2, float('nan')])
        result = pp.process(target)
        expected = DataFrame({'value': array_float([0.5, 1.0, 0.0])})
        assert_frame_equal(result, expected)

    def test_process_fillna_method(self):
        pp = NumericalSeriesPreprocessor(fillna_method='mean')
        target = Series([1, 2, float('nan')])
        result = pp.process(target)
        expected = DataFrame({'value': array_float([0.0, 1.0, 0.5])})
        assert_frame_equal(result, expected)

    def test_process_append_isnan(self):
        pp = NumericalSeriesPreprocessor(append_isnan=True)
        target = Series([1, 3, float('nan')])
        result = pp.process(target)
        expected = DataFrame({
            'value': array_float([0.0, 1.0, float('nan')]),
            'nan': array_uint8([0, 0, 1]),
        }, columns=['value', 'nan'])
        assert_frame_equal(result, expected)


