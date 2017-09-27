from unittest import TestCase

from pandas import Series, DataFrame
from pandas.util.testing import assert_frame_equal

from pdprpr.series import SteppingSeriesPreprocessor

from ..helper import array_uint8


class TestSteppingSeriesPreprocessor(TestCase):
    def test_process(self):
        pp = SteppingSeriesPreprocessor(steps=[2.0, 4.0])
        target = Series([1.0, 2.0, 3.0, 4.0, 5.0, float('nan')])
        result = pp.process(target)
        expected = DataFrame({
            '~2.0-': array_uint8([1, 0, 0, 0, 0, 0]),
            '2.0~4.0-': array_uint8([0, 1, 1, 0, 0, 0]),
            '4.0~': array_uint8([0, 0, 0, 1, 1, 0]),
        })
        assert_frame_equal(result, expected)
