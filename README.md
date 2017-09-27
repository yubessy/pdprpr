# pdprpr

Pdprpr preprocesses pandas objects (DataFrame, Series) for machine learning input.

## Usage

Assume you have this DataFrame to be preprocessed:

```python
df = DataFrame({
    'num': [1, 3, float('nan')],  # numerical feature to be scaled in [0, 1]
    'cat': ['P', 'Q', 'R'],       # categorical feature to be transformted to dummy var
    'bin': [0, 0, 1],             # binary (true/false) feature
}, columns =['num', 'cat', 'bin'])
#    num cat  bin
# 0  1.0   P    0
# 1  3.0   Q    0
# 2  NaN   R    1
```

You can define preprocessing settings in JSON-like format:

```yaml
- name: num
  kind: numerical

- name: cat
  kind: categorical

- name: bin
  kind: binary
```

Then `DataFramePreprocessor` instance can be created with them:

```python
import yaml

with open('<filename>') as f:
    settings = yaml.load(f)

from pdprpr import DataFramePreprocessor

processor = DataFramePreprocessor(settings)
```

Finary you can use it to preprocess your DataFrame:

```python
processor.process(df)
#    num/value  cat/P  cat/Q  cat/R  bin/False  bin/True
# 0        0.0      1      0      0          1         0
# 1        1.0      0      1      0          1         0
# 2        NaN      0      0      1          0         1
```

For more options please see [tests](./tests/) untill docs are available...
