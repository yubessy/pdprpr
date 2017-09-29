from numbers import Number

from attr import attrs, attrib
from attr.validators import instance_of, optional

from ._base import BaseSeriesPreprocessor


@attrs
class NumericalSeriesPreprocessor(BaseSeriesPreprocessor):
    kind = 'numerical'

    fillna = attrib(default=None, validator=optional(instance_of(Number)))
    fillna_method = attrib(default=None)
    minv = attrib(default=None, validator=optional(instance_of(Number)))
    maxv = attrib(default=None, validator=optional(instance_of(Number)))
    normalize = attrib(default=True, validator=instance_of(bool))

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
        df = series.to_frame('VALUE')
        if self.fillna is not None:
            df['VALUE'] = df['VALUE'].fillna(self.fillna)
        if self.fillna_method is not None:
            df['VALUE'] = self._fillna_method(df['VALUE'], self.fillna_method)
        if self.minv is not None:
            df['VALUE'] = self._minv(df['VALUE'], self.minv)
        if self.maxv is not None:
            df['VALUE'] = self._maxv(df['VALUE'], self.maxv)
        if self.normalize:
            df['VALUE'] = self._normalize(df['VALUE'])
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
