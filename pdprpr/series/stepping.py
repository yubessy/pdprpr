from attr import attrs, attrib

from attr.validators import instance_of

from .categorical import CategoricalSeriesPreprocessor


@attrs
class SteppingSeriesPreprocessor(CategoricalSeriesPreprocessor):
    steps = attrib(default=None, validator=instance_of(list))

    def get_category(self, value):
        first = self.steps[0]
        last = self.steps[-1]
        if value < first:
            return f'~{first}-'  # '~1-'
        elif last <= value:
            return f'{last}~'  # '7~'
        else:
            prev = first
            for s in self.steps[1:]:
                if value < s:
                    return f'{prev}~{s}-'
                prev = s
