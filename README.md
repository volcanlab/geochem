# geochem

`geochem` is a small Python package for exploring, preprocessing, plotting, and
analyzing geochemical data. It is designed for notebook-based work with
volcanic and igneous geochemical datasets, while still exposing reusable
functions for custom figures and workflows.

The package works primarily with `pandas.DataFrame` objects where rows are
samples and columns are geochemical components named with conventional symbols
such as `SiO2`, `FeOT`, `MgO`, `La`, `Rb`, and `Sr`. Many plotting and numerical
functions also accept NumPy arrays or sequences of arrays for users who prefer a
lower-level workflow.

## Main Features

- Standard geochemical component lists for major oxides, trace elements, and
  rare earth elements.
- Preprocessing helpers for common geochemical datasets:
  - strip whitespace from column names;
  - convert geochemical values to numeric data;
  - parse values such as `<0.5` as half the detection limit;
  - calculate `FeOT` from `FeO` and `Fe2O3`.
- Closure normalization for DataFrames and NumPy arrays.
- Matplotlib-based geochemical diagrams:
  - TAS diagram;
  - AFM ternary diagram;
  - spider diagrams;
  - Harker diagrams;
  - generic scatter plots.
- Low-level plotting helpers for building customized figures.
- Compositional data analysis utilities in `geochem.coda`.

## Installation

The simplest installation method is:

```bash
python -m pip install git+https://github.com/volcanlab/geochem.git
```

If you are using conda, activate your environment first:

```bash
conda activate my_env
python -m pip install git+https://github.com/volcanlab/geochem.git
```

## Quick Start

```python
import pandas as pd
import geochem as gc

df = pd.read_csv("data_example.csv")
gc.preproc(df)

df.head()
```

For plotting:

```python
import pandas as pd
import geochem.plt as gc

df = pd.read_csv("data_example.csv")
gc.preproc(df)

gc.TAS(df, fmt={"groupby": "Source"})
gc.AFM(df, fmt={"groupby": "Source"})
```

## Data Model

For DataFrame workflows:

- each row is a sample;
- each geochemical component is a column;
- standard names in DataFrames should follow the symbols defined in `geochem.parameters`;
- metadata columns such as `Sample`, `Source`, `Type`, or `Description` can be
  kept alongside the geochemical data.

Useful column-name helpers:

```python
import geochem as gc

gc.getnames_major()
gc.getnames_trace()
gc.getnames_REE()
gc.getnames_all()
```

## High-Level And Low-Level Workflows

The package is intended to support both quick analysis and custom figure
construction.

High-level functions do common tasks in one call:

```python
gc.preproc(df)
gc.TAS(df)
gc.AFM(df)
gc.spider(df, elements=gc.getnames_trace())
gc.harker(df)
```

Low-level functions expose the pieces needed for custom work:

```python
import matplotlib.pyplot as plt
import geochem.plt as gc

fig, ax = plt.subplots()
gc.tas_diagram(ax=ax)

major = df[gc.getnames_major()].copy()
major = gc.closure(major)
major["alkalis"] = major["Na2O"] + major["K2O"]

ax.plot(major["SiO2"], major["alkalis"], marker="o", linestyle="")
```

NumPy-style inputs are also supported by many functions:

```python
import numpy as np
import geochem as gc

arr = np.array([[10, 40], [20, 30]])
gc.closure(arr, total=100)
```

## Documentation

Tutorial notebooks live in `docs/`. They demonstrate loading data,
preprocessing, TAS diagrams, AFM diagrams, spider diagrams, and custom plotting
workflows. The notebooks are being revised to replace local `sys.path` hacks
with normal package installation.

Example datasets are also included in `docs/`.

## Package Structure

```text
geochem/
  parameters.py      Standard names and reference values
  preproc.py         DataFrame preprocessing pipeline
  utils.py           Closure and FeOT utilities
  plt/               Plotting functions and diagrams
  coda/              Compositional data analysis utilities
docs/                Tutorial notebooks and example data
tests/               Pytest test suite
```

## Author

José Luis Palma, PhD.   
Department of Earth Sciences. 
University of Concepción. Chile.  
jose at udec.cl. 
