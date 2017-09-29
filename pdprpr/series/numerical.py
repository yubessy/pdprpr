from numbers import Number

from attr import attrs, attrib
from attr.validators import instance_of, optional, in_

from ._base import BaseSeriesPreprocessor


@attrs
class NumericalSeriesPreprocessor(BaseSeriesPreprocessor):
    kind = 'numerical'

    FILLMETHODS = ('min', 'max', 'mean', 'median', 'mode')

    fillval = attrib(default=None, validator=optional(instance_of(Number)))
    fillmethod = attrib(default=None, validator=optional(in_(FILLMETHODS)))
    minval = attrib(default=None, validator=optional(instance_of(Number)))
    maxval = attrib(default=None, validator=optional(instance_of(Number)))
    normalize = attrib(default=True, validator=instance_of(bool))

    def process(self, series):
        series = series.astype(float)
        df = series.to_frame('VALUE')
        if self.fillval is not None:
            df['VALUE'] = df['VALUE'].fillna(self.fillval)
        if self.fillmethod is not None:
            df['VALUE'] = self._fillna_method(df['VALUE'], self.fillmethod)
        if self.minval is not None:
            df['VALUE'] = self._minv(df['VALUE'], self.minval)
        if self.maxval is not None:
            df['VALUE'] = self._maxv(df['VALUE'], self.maxval)
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
    def _minv(series, minval):
        return series.map(lambda v: max(minval, v), na_action='ignore')

    @staticmethod
    def _maxv(series, maxval):
        return series.map(lambda v: min(maxval, v), na_action='ignore')

    @staticmethod
    def _normalize(series):
        smin = series.min()
        smax = series.max()
        return (series - smin) / (smax - smin)
