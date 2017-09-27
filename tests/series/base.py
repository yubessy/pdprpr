from unittest import TestCase

from pandas import Series, DataFrame
from pandas.util.testing import assert_frame_equal

from pdprpr.series.base import BaseSeriesPreprocessor


class TestNumericalSeriesPreprocessor(TestCase):
    def test_process(self):
        pp = BaseSeriesPreprocessor()
        target = Series(['a', 'b', 'c'])
        result = pp.process(target)
        expected = DataFrame({'value': ['a', 'b', 'c']})
        assert_frame_equal(result, expected)

    def test_process_fillna(self):
        pp = BaseSeriesPreprocessor(fillna='na')
        target = Series(['a', 'b', None])
        result = pp.process(target)
        expected = DataFrame({'value': ['a', 'b', 'na']})
        assert_frame_equal(result, expected)
