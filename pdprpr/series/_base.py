from attr import attrs, attrib


@attrs
class BaseSeriesPreprocessor:
    dtype = object

    fillna = attrib(default=None)

    @fillna.validator
    def validate_fillna(self, attribute, value):
        if value is not None and not isinstance(value, self.dtype):
            mes = "{} is not subclass of {}".format(type(value), self.dtype)
            raise ValueError(mes)

    def process(self, series):
        df = series.to_frame('VALUE')
        if self.fillna is not None:
            df['VALUE'] = self._fillna(df['VALUE'], self.fillna)
        return df

    @staticmethod
    def _fillna(series, fillna):
        return series.fillna(fillna)
