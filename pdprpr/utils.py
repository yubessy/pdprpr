from numbers import Number

import numpy


def is_nan(value):
    return isinstance(value, Number) and numpy.isnan(value)
