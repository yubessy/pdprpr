import numpy
from attr import attrs, attrib
from attr.validators import optional, instance_of

from ._base import BaseSeriesPreprocessor


@attrs
class BinarySeriesPreprocessor(BaseSeriesPreprocessor):
    kind = 'binary'

    fillval = attrib(default=True, validator=optional(instance_of(bool)))

    def process(self, series):
        series = series.map(bool, na_action='ignore')

        if self.fillval is not None:
            series = series.fillna(self.fillval)

        return series.astype(numpy.uint8).to_frame('TRUE')
