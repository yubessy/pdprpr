import numpy
from attr import attrs

from ._base import BaseSeriesPreprocessor


@attrs
class BinarySeriesPreprocessor(BaseSeriesPreprocessor):
    kind = 'binary'
    dtype = bool

    def process(self, series):
        series = series.map(bool)
        return series.astype(numpy.uint8).to_frame('TRUE')
