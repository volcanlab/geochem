import numpy as np
import pandas as pd

from geochem.preproc import (
    preproc_strip_whitespace,
    _parse_geochem_value,
    preproc_make_numeric_columns,
    preproc
)

def test_parse_geochem_value():
    assert _parse_geochem_value(10.5) == 10.5
    assert _parse_geochem_value(" 15.2 ") == 15.2
    assert _parse_geochem_value("<1.0") == 0.5
    assert _parse_geochem_value("< 2.0 ") == 1.0
    assert np.isnan(_parse_geochem_value("invalid"))
    assert np.isnan(_parse_geochem_value("<"))
    assert np.isnan(_parse_geochem_value("<abc"))

def test_preproc_strip_whitespace():
    df = pd.DataFrame({" SiO2 ": [1], "TiO2": [2], " Al2O3  ": [3]})
    preproc_strip_whitespace(df)
    assert list(df.columns) == ["SiO2", "TiO2", "Al2O3"]

def test_preproc_make_numeric_columns():
    df = pd.DataFrame({
        "SiO2": ["50.5", "<1.0", "invalid", 45.0],
        "TiO2": [1.0, 2.0, 3.0, 4.0],
        "OtherCol": ["a", "b", "c", "d"]
    })
    
    preproc_make_numeric_columns(df)
    
    assert pd.api.types.is_float_dtype(df["SiO2"])
    np.testing.assert_allclose(df["SiO2"].values[:2], [50.5, 0.5])
    assert np.isnan(df["SiO2"].values[2])
    np.testing.assert_allclose(df["SiO2"].values[3], 45.0)
    
    # OtherCol should be unchanged since it's not a geochemical name
    assert list(df["OtherCol"]) == ["a", "b", "c", "d"]

def test_preproc_pipeline():
    df = pd.DataFrame({
        " SiO2 ": ["50.0", "55.0"],
        "FeO": [5.0, 6.0],
        "Fe2O3": [2.0, "<2.0"]
    })
    preproc(df)
    
    assert "SiO2" in df.columns
    assert "FeOT" in df.columns
    np.testing.assert_allclose(df["SiO2"].values, [50.0, 55.0])
    np.testing.assert_allclose(df["FeOT"].values[0], 5.0 + 0.8998 * 2.0)
    np.testing.assert_allclose(df["FeOT"].values[1], 6.0 + 0.8998 * 1.0) # <2.0 -> 1.0
