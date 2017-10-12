from pandas import DataFrame

from .binder import Binder


class DataFrameProcessor:

    def __init__(self):
        self.binders = {
            prefix: binder
            for prefix, binder in self.__class__.__dict__.items()
            if not prefix.startswith('_') and isinstance(binder, Binder)
        }

    def process(self, df):
        result = DataFrame(index=df.index)
        for prefix, binder in self.binders.items():
            applied = binder.apply(df)
            renamed = applied.rename(
                columns=lambda column: '{}__{}'.format(prefix, column))
            result = result.join(renamed)
        return result
