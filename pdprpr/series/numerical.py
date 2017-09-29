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
        if self.fillval is not None:
            series = series.fillna(self.fillval)
        if self.fillmethod is not None:
            series = self._fill_by_method(series)
        if self.minval is not None:
            series = self._min(series)
        if self.maxval is not None:
            series = self._max(series)
        if self.normalize:
            series = self._normalize(series)
        return series.to_frame('VALUE')

    def _fill_by_method(self, series):
        method = self.fillmethod
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

    def _min(self, series):
        return series.map(lambda v: max(self.minval, v), na_action='ignore')

    def _max(self, series):
        return series.map(lambda v: min(self.maxval, v), na_action='ignore')

    def _normalize(self, series):
        smin = series.min()
        smax = series.max()
        return (series - smin) / (smax - smin)
