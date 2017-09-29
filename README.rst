pdprpr
======

**PanDas PRePRocessor**: transform pandas objects (DataFrame / Series) into some form suitable for machine learning input.

Usage
-----

Assume you have this DataFrame to be preprocessed:

.. code-block:: python

    from pandas import DataFrame

    df = DataFrame({
        'num': [1, 3, float('nan')],  # numerical feature, needs to be scaled in [0, 1]
        'cat': ['p', 'q', 'r'],       # categorical feature, needs to be transformted to dummy var
        'bin': [False, False, True],  # binary feature, needs to be 0 / 1
    }, columns =['num', 'cat', 'bin'])
    #    num cat    bin
    # 0  1.0   p  False
    # 1  3.0   q  False
    # 2  NaN   r   True

Define preprocessing settings in JSON-like format:

.. code-block:: yaml

    # preprocessing.yml
    - name: num
      kind: numerical

    - name: cat
      kind: categorical

    - name: bin
      kind: binary

Then create `DataFramePreprocessor` instance with them:

.. code-block:: python

    import yaml

    with open('preprocessing.yml') as f:
        settings = yaml.load(f)

    from pdprpr import DataFramePreprocessor

    processor = DataFramePreprocessor(settings)

Finally use it to preprocess your DataFrame:

.. code-block:: python

  processor.process(df)
  #    num__VALUE  cat__p  cat__q  cat__r  bin__TRUE
  # 0         0.0       1       0       0          0
  # 1         1.0       0       1       0          0
  # 2         NaN       0       0       1          1

For more options please see `tests <./tests/>` untill docs get available...
