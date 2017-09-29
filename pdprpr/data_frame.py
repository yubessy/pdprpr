from collections import namedtuple

from pandas import DataFrame

from .series import (
    NumericalSeriesPreprocessor,
    NullableSeriesPreprocessor,
    CategoricalSeriesPreprocessor,
    BinarySeriesPreprocessor,
    ThresholdSeriesPreprocessor,
    RegexSeriesPreprocessor,
)


_SERIES_PREPROCESSORS = {
    processor.kind: processor for processor in (
        NumericalSeriesPreprocessor,
        NullableSeriesPreprocessor,
        CategoricalSeriesPreprocessor,
        BinarySeriesPreprocessor,
        ThresholdSeriesPreprocessor,
        RegexSeriesPreprocessor,
    )
}


Column = namedtuple('Column', ['name', 'processor'])


class DataFramePreprocessor:
    def __init__(self, settings):
        kinds = _SERIES_PREPROCESSORS.keys()

        columns = []
        for setting in settings:
            name, kind = setting['name'], setting['kind']
            options = setting.get('options', {})

            if kind not in kinds:
                mes = "Unknown kind: '{}'".format(kind)
                raise ValueError(mes)

            processor = _SERIES_PREPROCESSORS[kind](**options)
            columns.append(Column(name=name, processor=processor))

        self._columns = columns

    def process(self, df):
        result = DataFrame(index=df.index)
        for column in self._columns:
            name = column.name
            processed = column.processor.process(df[name])
            renamed = processed.rename(
                columns=lambda c: '{}__{}'.format(name, c))
            result = result.join(renamed)

        return result
