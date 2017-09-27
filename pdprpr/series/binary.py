from attr import attrs

from .categorical import CategoricalSeriesPreprocessor


@attrs
class BinarySeriesPreprocessor(CategoricalSeriesPreprocessor):
    kind = 'binary'
    dtype = bool

    @staticmethod
    def get_category(value):
        return bool(value)

    @staticmethod
    def get_column(category):
        return str(category)
