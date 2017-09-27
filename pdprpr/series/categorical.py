import numpy
from attr import attrs, attrib
from pandas import get_dummies

from .base import BaseSeriesPreprocessor


@attrs
class CategoricalSeriesPreprocessor(BaseSeriesPreprocessor):
    kind = 'categorical'
    default = attrib(default=None)

    @default.validator
    def validate_default(self, attribute, value):
        if value is not None and not isinstance(value, self.dtype):
            mes = "{} is not subclass of {}".format(type(value), self.dtype)
            raise ValueError(mes)

    def process(self, series):
        df = super().process(series)
        df.value = df.value.map(self.get_category, na_action='ignore')
        if self.default is not None:
            df.value = self._default_to_nan(df.value, self.default)
        dummies = get_dummies(df.value).astype(numpy.uint8)
        return dummies.rename(columns=self.get_column)

    @staticmethod
    def _default_to_nan(series, default):
        def replacer(x):
            if isinstance(x, float) and numpy.isnan(x):
                return 'nan'
            elif x == default:
                return float('nan')
            else:
                return x

        return series.map(replacer)

    @staticmethod
    def get_category(value):
        return value

    @staticmethod
    def get_column(category):
        return str(category)


