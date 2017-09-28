
class BaseSeriesPreprocessor:
    @property
    def kind(self):
        raise NotImplementedError

    @property
    def dtype(self):
        raise NotImplementedError

    @property
    def process(self, series):
        raise NotImplementedError
