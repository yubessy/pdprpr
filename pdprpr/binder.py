from attr import attrs, attrib
from attr.validators import instance_of


from .series._base import BaseSeriesPreprocessor


@attrs
class Binder:
    processor = attrib(validator=instance_of(BaseSeriesPreprocessor))
    binding = attrib(validator=instance_of(str))

    def apply(self, df):
        return self.processor.process(df[self.binding])
