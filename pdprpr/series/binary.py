import numpy
from attr import attrs, attrib
from attr.validators import optional, instance_of

from ._base import BaseSeriesPreprocessor


@attrs
class BinarySeriesPreprocessor(BaseSeriesPreprocessor):
    kind = 'binary'
    dtype = bool

    fillna = attrib(default=True, validator=optional(instance_of(dtype)))

    def process(self, series):
        series = series.map(bool, na_action='ignore')

        if self.fillna is not None:
            series = series.fillna(self.fillna)

        return series.astype(numpy.uint8).to_frame('TRUE')
