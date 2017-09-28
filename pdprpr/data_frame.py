from collections import namedtuple

from pandas import DataFrame

from .series import (
    NumericalSeriesPreprocessor,
    CategoricalSeriesPreprocessor,
    BinarySeriesPreprocessor,
    SteppingSeriesPreprocessor,
    RegexSeriesPreprocessor,
)


Column = namedtuple('Column', ['name', 'processor'])

_SERIES_PROCESSORS = {
    p.kind: p for p in (
        NumericalSeriesPreprocessor,
        CategoricalSeriesPreprocessor,
        BinarySeriesPreprocessor,
        SteppingSeriesPreprocessor,
        RegexSeriesPreprocessor,
    )
}


class DataFramePreprocessor:
    def __init__(self, settings):
        kinds = _SERIES_PROCESSORS.keys()

        columns = []
        for setting in settings:
            name, kind = setting['name'], setting['kind']

            if kind not in kinds:
                mes = "Unknown kind: '{}'".format(kind)
                raise ValueError(mes)

            opts = {
                k: v for k, v in setting.items() if k not in ('name', 'kind')}

            pp = _SERIES_PROCESSORS[kind](**opts)
            columns.append(Column(name=name, processor=pp))

        self._columns = columns

    def process(self, df):
        result = DataFrame(index=df.index)
        for column in self._columns:
            name = column.name
            processed = column.processor.process(df[name])
            renamed = processed.rename(columns=lambda c: f'{name}__{c}')
            result = result.join(renamed)

        return result
