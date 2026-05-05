import numpy as np
import pandas as pd
from typing import Any
from .parameters import getnames_all
from .utils import calculate_FeOT

def _parse_geochem_value(value: Any) -> float:
    # Handle direct numeric types first (simplest)
    if isinstance(value, (int, float)):
        return float(value)

    # Handle string types
    if isinstance(value, str):
        s_value = value.strip()
        # Case 1: Starts with '<'
        if s_value.startswith('<'):
            try:
                # Extract numeric part after '<'
                numeric_part = s_value[1:].strip()
                # Check if the extracted part is a valid number representation
                if numeric_part and numeric_part.replace('.', '', 1).isdigit():
                    return float(numeric_part) / 2.0
                else:
                    # Invalid format like '<' alone or '<abc'
                    return np.nan
            except (ValueError, IndexError):
                 # Error during processing the part after '<'
                 return np.nan
        # Case 2: Doesn't start with '<', try direct float conversion
        else:
            try:
                return float(s_value)
            except ValueError:
                # String is not a simple float
                return np.nan

    # Handle other types (None, pd.NA, etc.)
    return np.nan

def preproc_strip_whitespace(df: pd.DataFrame) -> None:
    """
    Removes leading/trailing whitespace from column names in the DataFrame.

    Modifies the DataFrame in place.

    Args:
        df (pd.DataFrame): The input DataFrame.
    """
    # Strip whitespaces from the column names
    print("Strip whitespaces from column names")
    print(">  column names before:\n", df.columns.to_list())

    df.rename(columns=lambda x: str(x).strip(), inplace=True)
    print(">  column names after:\n", df.columns.to_list())
    print("")

def preproc_make_numeric_columns(df: pd.DataFrame) -> None:
    """
    Ensures that columns expected to contain geochemical data are numeric.

    Identifies relevant columns based on `getnames_all()`.
    For string/object columns, attempts to parse values:
    - Converts numeric strings to float.
    - Handles strings like '<X' by converting to X/2.0 using _parse_geochem_value.
    - Converts unparseable strings to NaN using _parse_geochem_value.
    Coerces all relevant columns to numeric using pd.to_numeric(errors='coerce').
    Ensures the final data type of numeric columns is float.
    Modifies the DataFrame in place.

    Args:
        df (pd.DataFrame): The input DataFrame.
    """
    print("Ensuring geochemical data columns are numeric")
    COLUMN_NAMES = getnames_all()
    # Use a dictionary to track processing steps for each column
    processing_log = {cname: [] for cname in df.columns}

    # Identify relevant columns actually present in the DataFrame
    relevant_cols = [cname for cname in COLUMN_NAMES if cname in df.columns]

    # Step 1: Apply custom parsing only to object/string columns
    for cname in relevant_cols:
        if pd.api.types.is_object_dtype(df[cname].dtype) or pd.api.types.is_string_dtype(df[cname].dtype):
            df[cname] = df[cname].apply(_parse_geochem_value)
            # Check if parsing actually changed the column content significantly
            # (ignoring type changes for now, focusing on values like string -> NaN/float)
            # This check might be complex; simply logging parsing is easier.
            processing_log[cname].append("parsed")


    # Step 2: Coerce all relevant columns to numeric, handling errors
    for cname in relevant_cols:
        # Apply to_numeric to handle parsed values (now float/NaN) and other non-numeric types
        # errors='coerce' turns problematic values into NaN
        if not pd.api.types.is_numeric_dtype(df[cname].dtype):
             original_dtype_kind = df[cname].dtype.kind # Check before coercion
             original_nan_count = df[cname].isnull().sum()

             df[cname] = pd.to_numeric(df[cname], errors='coerce')

             final_dtype_kind = df[cname].dtype.kind
             final_nan_count = df[cname].isnull().sum()

             # Log if coercion changed type kind (e.g., 'O' to 'f') or introduced NaNs
             type_changed = original_dtype_kind != final_dtype_kind and final_dtype_kind in ('f', 'i', 'u') # float, int, unsigned int
             nans_introduced = final_nan_count > original_nan_count

             if type_changed:
                 processing_log[cname].append("coerced_type")
             if nans_introduced:
                 processing_log[cname].append("coerced_nans")


    # Step 3: Ensure final type is float for all numeric relevant columns
    for cname in relevant_cols:
         # Check if column still exists and is numeric
         if cname in df.columns and pd.api.types.is_numeric_dtype(df[cname].dtype):
             if not pd.api.types.is_float_dtype(df[cname].dtype):
                 df[cname] = df[cname].astype(float)
                 processing_log[cname].append("finalized_float")


    # Construct final log messages
    final_log_entries = []
    for cname in relevant_cols:
        steps = processing_log.get(cname, [])
        if steps:
            step_desc = []
            if "parsed" in steps: step_desc.append("parsed")
            if "coerced_type" in steps: step_desc.append("coerced")
            if "coerced_nans" in steps: step_desc.append("coerced (NaNs introduced)")
            if "finalized_float" in steps: step_desc.append("type set to float")
            # Remove duplicates if coercion resulted in both type change and NaNs logged separately
            unique_desc = []
            seen_coerced = False
            for desc in step_desc:
                if "coerced" in desc:
                    if not seen_coerced:
                        unique_desc.append(desc)
                        seen_coerced = True
                else:
                    unique_desc.append(desc)

            final_log_entries.append(f"{cname} ({', '.join(unique_desc)})")


    if final_log_entries:
        print(f">  Processed/verified numeric columns: {'; '.join(final_log_entries)}")
    else:
        print(">  No relevant columns found or required processing.")
    print("")


def preproc_calculate_feot(df: pd.DataFrame) -> None:
    """
    Checks for FeO and Fe2O3 columns and calculates FeOT (Total Fe as FeO).

    Uses the `calculate_FeOT` utility function. If 'FeOT' column doesn't
    exist, it will be created.
    Modifies the DataFrame in place.

    Args:
        df (pd.DataFrame): The input DataFrame.
    """
    # Check columns with Fe oxides
    print("Check columns with Fe oxides and calculate FeOT")
    if "FeO" in df.columns:
        print(".. FeO column in database")
    else:
        print(".. FeO column missing")
    if "Fe2O3" in df.columns:
        print(".. Fe2O3 column in database")
    else:
        print(".. Fe2O3 column missing")
    if "FeOT" in df.columns:
        print(".. FeOT column in database")
    else:
        print(".. FeOT column created")

    print('.. Calculating FeOT where necessary')
    calculate_FeOT(df)

def preproc(df: pd.DataFrame) -> None:
    """
    Applies a sequence of preprocessing steps to the DataFrame.

    1. Strips whitespace from column names.
    2. Ensures relevant geochemical columns are numeric.
    3. Calculates FeOT.

    Modifies the DataFrame in place.

    Args:
        df (pd.DataFrame): The input DataFrame.
    """
    preproc_strip_whitespace(df)
    preproc_make_numeric_columns(df)
    preproc_calculate_feot(df)
