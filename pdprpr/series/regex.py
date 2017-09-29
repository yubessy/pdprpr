import numpy

import re
from collections import namedtuple

from attr import attrs, attrib
from attr.validators import instance_of

from .categorical import CategoricalSeriesPreprocessor


Group = namedtuple('Group', ['name', 'regex'])


@attrs
class RegexSeriesPreprocessor(CategoricalSeriesPreprocessor):
    kind = 'regex'

    groups = attrib(default=None, validator=instance_of(list))

    def __attrs_post_init__(self):
        self._regex_groups = [
            Group(name=g['name'], regex=re.compile(g['regex']))
            for g in self.groups]

    def get_category(self, value):
        for name, regex in self._regex_groups:
            if regex.match(value):
                return name
        return numpy.nan
