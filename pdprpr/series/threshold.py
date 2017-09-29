from attr import attrs, attrib

from attr.validators import instance_of

from .categorical import CategoricalSeriesPreprocessor


@attrs
class ThresholdSeriesPreprocessor(CategoricalSeriesPreprocessor):
    kind = 'threshold'

    thresholds = attrib(default=None, validator=instance_of(list))

    def get_category(self, value):
        for i, threshold in enumerate(self.thresholds):
            if value < threshold:
                return str(i)
        return str(len(self.thresholds))
