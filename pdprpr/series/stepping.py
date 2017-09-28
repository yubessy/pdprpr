from attr import attrs, attrib

from attr.validators import instance_of

from .categorical import CategoricalSeriesPreprocessor


@attrs
class SteppingSeriesPreprocessor(CategoricalSeriesPreprocessor):
    kind = 'stepping'
    steps = attrib(default=None, validator=instance_of(list))

    def get_category(self, value):
        for i, step in enumerate(self.steps):
            if value < step:
                return str(i)
        return str(len(self.steps))
