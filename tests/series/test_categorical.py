from unittest import TestCase

import numpy
from pandas import Series, DataFrame
from pandas.util.testing import assert_frame_equal

from pdprpr.series import CategoricalSeriesPreprocessor

from ..helper import array_uint8


class TestCategoricalSeriesPreprocessor(TestCase):
    def test_process(self):
        pp = CategoricalSeriesPreprocessor()
        target = Series(['P', 'Q', 'R', numpy.nan])
        result = pp.process(target)
        expected = DataFrame({
            'P': array_uint8([1, 0, 0, 0]),
            'Q': array_uint8([0, 1, 0, 0]),
            'R': array_uint8([0, 0, 1, 0]),
        }, columns=['P', 'Q', 'R'])
        assert_frame_equal(result, expected)

    def test_process_fillna(self):
        pp = CategoricalSeriesPreprocessor(fillval='P')
        target = Series(['P', 'Q', 'R', numpy.nan])
        result = pp.process(target)
        expected = DataFrame({
            'P': array_uint8([1, 0, 0, 1]),
            'Q': array_uint8([0, 1, 0, 0]),
            'R': array_uint8([0, 0, 1, 0]),
        }, columns=['P', 'Q', 'R'])
        assert_frame_equal(result, expected)

    def test_process_default(self):
        pp = CategoricalSeriesPreprocessor(defaultval='P')
        target = Series(['P', 'Q', 'R', numpy.nan])
        result = pp.process(target)
        expected = DataFrame({
            'Q': array_uint8([0, 1, 0, 0]),
            'R': array_uint8([0, 0, 1, 0]),
            'NAN': array_uint8([0, 0, 0, 1]),
        }, columns=['NAN', 'Q', 'R'])
        assert_frame_equal(result, expected)
