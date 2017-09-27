from numbers import Real

import numpy
from attr import attrs, attrib
from attr.validators import instance_of, optional

from .base import BaseSeriesPreprocessor


@attrs
class NumericalSeriesPreprocessor(BaseSeriesPreprocessor):
    kind = 'numerical'
    dtype = Real

    fillna_method = attrib(default=None)
    minv = attrib(default=None, validator=optional(instance_of(Real)))
    maxv = attrib(default=None, validator=optional(instance_of(Real)))
    normalize = attrib(default=True, validator=instance_of(bool))
    append_isnan = attrib(default=False, validator=instance_of(bool))

    @fillna_method.validator
    def validate_fillna_method(self, attribute, value):
        if self.fillna is not None and value is not None:
            mes = "fillna and fillna_method cannot be used together"
            raise ValueError(mes)

        methods = ('min', 'max', 'mean', 'median', 'mode')
        if value is not None and value not in methods:
            mes = "method must be one of {}".format(', '.join(methods))
            raise ValueError(mes)

    def process(self, series):
        series = series.astype(float)
        df = super().process(series)
        if self.fillna_method is not None:
            df.value = self._fillna_method(df.value, self.fillna_method)
        if self.minv is not None:
            df.value = self._minv(df.value, self.minv)
        if self.maxv is not None:
            df.value = self._maxv(df.value, self.maxv)
        if self.normalize:
            df.value = self._normalize(df.value)
        if self.append_isnan:
            df['nan'] = self._isnan(series)
        return df

    @staticmethod
    def _fillna_method(series, method):
        if method == 'min':
            fillv = series.min()
        elif method == 'max':
            fillv = series.max()
        elif method == 'mean':
            fillv = series.mean()
        elif method == 'median':
            fillv = series.median()
        elif method == 'mode':
            fillv = series.mode()[0]
        return series.fillna(fillv)

    @staticmethod
    def _minv(series, minv):
        return series.map(lambda v: max(minv, v), na_action='ignore')

    @staticmethod
    def _maxv(series, maxv):
        return series.map(lambda v: min(maxv, v), na_action='ignore')

    @staticmethod
    def _normalize(series):
        smin = series.min()
        smax = series.max()
        return (series - smin) / (smax - smin)

    @staticmethod
    def _isnan(series):
        return series.astype(float).isnull().astype(numpy.uint8)
