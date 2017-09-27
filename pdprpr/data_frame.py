from collections import namedtuple

from pandas import DataFrame

from .series.numerical import NumericalSeriesPreprocessor
from .series.categorical import CategoricalSeriesPreprocessor
from .series.binary import BinarySeriesPreprocessor
from .series.stepping import SteppingSeriesPreprocessor
from .series.regex import RegexSeriesPreprocessor


Column = namedtuple('Column', ['name', 'preprocessor'])

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
    def __init__(self, configs):
        kinds = _SERIES_PROCESSORS.keys()

        columns = []
        for config in configs:
            name, kind = config['name'], config['kind']

            if kind not in kinds:
                mes = "Unknown kind: '{}'".format(kind)
                raise ValueError(mes)

            opts = {
                k: v for k, v in config.items() if k not in ('name', 'kind')}

            pp = _SERIES_PROCESSORS[kind](**opts)
            columns.append(Column(name=name, preprocessor=pp))

        self._columns = columns

    def process(self, df):
        result = DataFrame(index=df.index)
        for column in self._columns:
            name = column.name
            processed = column.preprocessor.process(df[name])
            renamed = processed.rename(columns=lambda c: f'{name}/{c}')
            result = result.join(renamed)

        return result
