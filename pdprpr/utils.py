import math
from numbers import Number

from numpy import float_, int_, bool_, isnan


def is_nan(value):
    if (isinstance(value, float_)
         or isinstance(value, int_)
         or isinstance(value, bool_)):
        return isnan(value)
    elif isinstance(value, Number):
        return math.isnan(value)
    else:
        return False
