from collections import namedtuple

from pandas import DataFrame

from .series.numerical import NumericalSeriesPreprocessor
from .series.categorical import CategoricalSeriesPreprocessor
from .series.binary import BinarySeriesPreprocessor
from .series.stepping import SteppingSeriesPreprocessor
from .series.regex import RegexSeriesPreprocessor


Column = namedtuple('Column', ['name', 'preprocessor'])


class DataFramePreprocessor:
    def __init__(self, configs):
        pp_classes = {
            'numerical': NumericalSeriesPreprocessor,
            'categorical': CategoricalSeriesPreprocessor,
            'binary': BinarySeriesPreprocessor,
            'stepping': SteppingSeriesPreprocessor,
            'regexp': RegexSeriesPreprocessor,
        }
        pp_class_names = pp_classes.keys()

        columns = []
        for config in configs:
            name, kind = config['name'], config['kind']

            if kind not in pp_class_names:
                mes = "Unknown kind: '{}'".format(kind)
                raise ValueError(mes)

            opts = {
                k: v for k, v in config.items() if k not in ('name', 'kind')}

            pp = pp_classes[kind](**opts)
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
