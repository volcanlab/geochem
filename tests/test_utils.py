import numpy as np
import pandas as pd
import pytest

from geochem.utils import closure, calculate_FeOT

def test_closure_pandas():
    df = pd.DataFrame({"A": [10, 20], "B": [40, 30]})
    # Row sums: 50, 50. Total=100. Should become [20, 80] and [40, 60].
    closed = closure(df, 100)
    assert isinstance(closed, pd.DataFrame)
    np.testing.assert_allclose(closed["A"].values, [20, 40])
    np.testing.assert_allclose(closed["B"].values, [80, 60])

def test_closure_numpy_1d():
    arr = np.array([10, 40])
    closed = closure(arr, 100)
    assert isinstance(closed, np.ndarray)
    np.testing.assert_allclose(closed, [20, 80])

def test_closure_numpy_2d():
    arr = np.array([[10, 40], [20, 30]])
    closed = closure(arr, 100)
    assert isinstance(closed, np.ndarray)
    np.testing.assert_allclose(closed, [[20, 80], [40, 60]])

def test_closure_invalid_type():
    with pytest.raises(TypeError):
        closure([10, 20])

def test_calculate_FeOT_pandas():
    df = pd.DataFrame({
        "FeO": [10, np.nan, 5],
        "Fe2O3": [5, 10, np.nan],
        "FeOT": [np.nan, 20, np.nan]
    })
    # FeOT = FeO + 0.8998 * Fe2O3
    calculate_FeOT(df)
    assert "FeOT" in df.columns
    np.testing.assert_allclose(df["FeOT"].values[0], 10 + 0.8998 * 5)
    np.testing.assert_allclose(df["FeOT"].values[1], 20)  # should not overwrite existing value
    np.testing.assert_allclose(df["FeOT"].values[2], 5)  # Fe2O3 is nan, so FeOT = FeO

def test_calculate_FeOT_numpy():
    FeO = np.array([10.0, np.nan, 5.0])
    Fe2O3 = np.array([5.0, 10.0, np.nan])
    FeOT = np.array([np.nan, 20.0, np.nan])
    
    res_FeO, res_Fe2O3, res_FeOT = calculate_FeOT([FeO, Fe2O3, FeOT])
    np.testing.assert_allclose(res_FeOT[0], 10 + 0.8998 * 5)
    np.testing.assert_allclose(res_FeOT[1], 20)
    np.testing.assert_allclose(res_FeOT[2], 5)

def test_calculate_FeOT_invalid():
    with pytest.raises(TypeError):
        calculate_FeOT({"FeO": [10]})
