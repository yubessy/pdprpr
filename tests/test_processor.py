from unittest import TestCase

import numpy
from pandas import DataFrame
from pandas.util.testing import assert_frame_equal

from pdprpr import DataFrameProcessor, Binder
from pdprpr.series import (
    NumericalSeriesPreprocessor,
    NullableSeriesPreprocessor,
    BinarySeriesPreprocessor,
    CategoricalSeriesPreprocessor,
)

from .helper import array_float, array_uint8


class TestDataFramePreprocessor(TestCase):

    def test_process(self):
        class ExampleProcessor(DataFrameProcessor):
            num = Binder(NumericalSeriesPreprocessor(), 'raw_num')
            nul = Binder(NullableSeriesPreprocessor(), 'raw_nul')
            bin = Binder(BinarySeriesPreprocessor(), 'raw_bin')
            cat = Binder(CategoricalSeriesPreprocessor(), 'raw_cat')

        ep = ExampleProcessor()
        target = DataFrame({
            'raw_num': [1, 3, numpy.nan],
            'raw_nul': [0, None, numpy.nan],
            'raw_bin': [0, 2, numpy.nan],
            'raw_cat': ['p', 'q', 'r'],
        })
        result = ep.process(target)
        expected = DataFrame({
            'num__VALUE': array_float([0.0, 1.0, numpy.nan]),
            'nul__NULL':  array_uint8([0, 1, 1]),
            'bin__TRUE':  array_uint8([0, 1, 1]),
            'cat__p': array_uint8([1, 0, 0]),
            'cat__q': array_uint8([0, 1, 0]),
            'cat__r': array_uint8([0, 0, 1]),
        }, columns=[
            'num__VALUE',
            'nul__NULL',
            'bin__TRUE',
            'cat__p', 'cat__q', 'cat__r',
        ])
        assert_frame_equal(result, expected)

    def test_process_ignore_unknown_columns(self):
        class ExampleProcessor(DataFrameProcessor):
            num = Binder(NumericalSeriesPreprocessor(), 'raw_num')

        ep = ExampleProcessor()
        target = DataFrame({
            'raw_num': [1, 3, numpy.nan],
            'unknown': [..., ..., ...],
        })
        result = ep.process(target)
        expected = DataFrame({'num__VALUE': array_float([0, 1, numpy.nan])})
        assert_frame_equal(result, expected)

    def test_process_fail_when_columns_do_not_exist(self):
        class ExampleProcessor(DataFrameProcessor):
            num = Binder(NumericalSeriesPreprocessor(), 'raw_num')

        ep = ExampleProcessor()
        target = DataFrame({'unknown': [..., ..., ...]})
        with self.assertRaises(KeyError):
            ep.process(target)
