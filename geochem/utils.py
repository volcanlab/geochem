import numpy as np
import pandas as pd
from typing import Union, Sequence

def closure(data: Union[pd.DataFrame, np.ndarray] = None, total: float = 100.) -> Union[pd.DataFrame, np.ndarray]:
    """
    closure(data=df, total=100)

    Closure operation considering all columns in DataFrame 'data' or 
    the last axis of numpy array 'data', with closure constant equal to 'total'.

    'data' is a pandas DataFrame with geochemical components in the columns
    and samples in the rows, or a numpy array.
    
    Returns a new DataFrame or numpy array with every row summing to 'total'
    """
    if isinstance(data, pd.DataFrame):
        df_closed = data.copy()
        #get a list with the names of all the original columns
        columns = df_closed.columns.to_list()

        #create a column with the sum of all the original columns
        df_closed['Sum'] = df_closed.sum(axis=1)

        #normalize all the original columns
        for col in columns:
            df_closed[df_closed['Sum']<=0] = np.nan
            df_closed[col] = df_closed[col]/df_closed['Sum'] * total
        
        df_closed = df_closed[columns]
        return df_closed
    elif isinstance(data, np.ndarray):
        arr = np.array(data, dtype=float)
        if arr.ndim == 1:
            s = np.sum(arr)
            if s <= 0:
                return np.full_like(arr, np.nan)
            return arr / s * total
        elif arr.ndim == 2:
            s = np.sum(arr, axis=1, keepdims=True)
            with np.errstate(divide='ignore', invalid='ignore'):
                res = arr / s * total
            res[s.flatten() <= 0] = np.nan
            return res
        else:
            raise ValueError("numpy array must be 1D or 2D")
    else:
        raise TypeError("Input data must be a pandas DataFrame or numpy array")

def calculate_FeOT(data: Union[pd.DataFrame, Sequence[np.ndarray]]) -> Union[None, Sequence[np.ndarray]]:
    """
    If FeOT doesn't exist, it calculates the values based on FeO and Fe2O3.
    
    Args:
        data: A pandas DataFrame (modified in-place), OR
              A sequence (list or tuple) of exactly 3 numpy 1D arrays: [FeO, Fe2O3, FeOT].
              If using numpy arrays, returns the updated [FeO, Fe2O3, FeOT].
    """
    if isinstance(data, pd.DataFrame):
        df = data
        #Number of rows (samples) in the dataframe
        n_rows = df.shape[0]

        #Create numpy arrays with FeO and Fe2O3
        if "FeO" in df.columns:
            FeO = df["FeO"].to_numpy(dtype=float, copy=True)
            FeO[np.isnan(FeO)] = 0. #necessary for calculating FeOT
        else:
            FeO = np.zeros(n_rows)

        if "Fe2O3" in df.columns:
            Fe2O3 = df["Fe2O3"].to_numpy(dtype=float, copy=True)
            Fe2O3[np.isnan(Fe2O3)] = 0. #necessary for calculating FeOT
        else:
            Fe2O3 = np.zeros(n_rows)

        #Calculate the FeOT
        FeOT_calc = 0.8998*Fe2O3 + FeO

        if "FeOT" in df.columns:
            #I shouldn't modified FeOT, in a row, 
            #unless it's np.nan or 0, and FeO-Fe2O3 exist.
            FeOT = df["FeOT"].to_numpy(dtype=float, copy=True)
            for i,feot0 in enumerate(FeOT):
                #Check if FeOT has a value
                if np.isnan(feot0) or feot0==0:   
                    #Since FeOT doesn't have a value, check if 
                    #FeO and/or Fe2O3 has a value to calculate FeOT
                    if FeO[i]>0 or Fe2O3[i]>0:
                        FeOT[i] =FeOT_calc[i]
                    else:
                        FeOT[i] = np.nan
            df["FeOT"] = FeOT
        else:
            FeOT_calc[FeOT_calc <= 0] = np.nan
            #Add FeOT to the dataframe
            df['FeOT'] = FeOT_calc
        return None
    elif isinstance(data, (list, tuple)) and len(data) == 3:
        FeO_orig, Fe2O3_orig, FeOT_orig = data
        FeO = np.array(FeO_orig, dtype=float)
        Fe2O3 = np.array(Fe2O3_orig, dtype=float)
        FeOT = np.array(FeOT_orig, dtype=float)

        FeO_clean = FeO.copy()
        FeO_clean[np.isnan(FeO_clean)] = 0.

        Fe2O3_clean = Fe2O3.copy()
        Fe2O3_clean[np.isnan(Fe2O3_clean)] = 0.

        FeOT_calc = 0.8998 * Fe2O3_clean + FeO_clean

        for i, feot0 in enumerate(FeOT):
            if np.isnan(feot0) or feot0 == 0:
                if FeO_clean[i] > 0 or Fe2O3_clean[i] > 0:
                    FeOT[i] = FeOT_calc[i]
                else:
                    FeOT[i] = np.nan
        return [FeO_orig, Fe2O3_orig, FeOT]
    else:
        raise TypeError("Input must be a pandas DataFrame or a sequence of 3 numpy arrays: [FeO, Fe2O3, FeOT]")
