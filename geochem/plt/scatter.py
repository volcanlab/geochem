#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from typing import Union, Optional, Dict, Any, Sequence

def scatter(data: Union[pd.DataFrame, Sequence[np.ndarray]], x_col: str = 'X', y_col: str = 'Y', fmt: Optional[Dict[str, Any]] = None, opt: Optional[Dict[str, Any]] = None, ax: Optional[plt.Axes] = None) -> plt.Axes:
    """
    scatter(data, x_col, y_col, fmt=None, opt=None, ax=None)

    Creates a scatter plot of two specified columns from a DataFrame,
    OR from a sequence of two 1D numpy arrays [x_array, y_array].

    Args:
        data: The input DataFrame containing the data OR sequence of two numpy arrays.
        x_col (str): The name of the column to plot on the x-axis (or x-axis label for numpy array).
        y_col (str): The name of the column to plot on the y-axis (or y-axis label for numpy array).
        fmt (dict, optional): Dictionary to override default formatting.
            Defaults:
                'title': f"{y_col} vs {x_col}",
                'groupby': None,  # Column name to group data by for different symbols/colors
                'marker': 'o',
                'linestyle': '',
                'ms': 6,          # Marker size
                'show': True,     # Call plt.show() at the end
                'legend': True    # Add a legend when using groupby
        opt (dict, optional): Dictionary to override default behavior/options.
            Defaults:
                'dropna': True    # Drop rows with NaN in x_col or y_col
        ax (matplotlib.axes.Axes, optional): An existing Axes object to plot on.
                                            If None, a new figure and axes are created.

    Returns:
        matplotlib.axes.Axes: The Axes object containing the plot.
    """
    opt_default = {'dropna': True}
    if opt is None: opt = {}
    for key in opt_default:
        if key not in opt:
            opt[key] = opt_default[key]

    fmt_default = {
        'title': f"{y_col} vs {x_col}",
        'groupby': None,
        'marker': 'o',
        'linestyle': '',
        'ms': 6,
        'show': True,
        'legend': True
    }
    if fmt is None: fmt = {}
    for key in fmt_default:
        if key not in fmt:
            fmt[key] = fmt_default[key]

    if ax is None:
        fig, ax = plt.subplots()
    else:
        # Get the figure associated with the existing axes
        fig = ax.get_figure()

    if isinstance(data, pd.DataFrame):
        # Check if specified columns exist
        required_cols = [x_col, y_col]
        if fmt['groupby'] is not None:
            if fmt['groupby'] in data.columns:
                required_cols.append(fmt['groupby'])
            else:
                print(f"Warning: Grouping column '{fmt['groupby']}' not found. Plotting all data together.")
                fmt['groupby'] = None # Reset groupby if column not found

        missing_cols = [col for col in required_cols if col not in data.columns]
        if missing_cols:
            raise ValueError(f"Required columns not found in DataFrame: {', '.join(missing_cols)}")

        # Select relevant data and handle NaNs
        plot_data = data[required_cols].copy()
        Nrows_orig = plot_data.shape[0]

        # Define columns to check for NaNs based on plotting requirements
        nan_check_cols = [x_col, y_col]
        if Nrows_orig > 0:
            Nrows_nan = plot_data[nan_check_cols].isnull().any(axis=1).sum()
        else:
            Nrows_nan = 0

        if Nrows_nan > 0 and opt['dropna']:
            plot_data.dropna(subset=nan_check_cols, inplace=True)
            print(f"{Nrows_nan} samples out of {Nrows_orig} removed due to missing values in '{x_col}' or '{y_col}'.")
        elif Nrows_nan > 0:
            print(f"Warning: {Nrows_nan} samples with missing values in '{x_col}' or '{y_col}' are being plotted (may cause errors or be ignored by plotting function).")

        # Plotting logic
        if fmt['groupby'] is not None:
            unique_groups = plot_data[fmt['groupby']].unique()
            try:
                cmap = cm.get_cmap('tab10') if len(unique_groups) <= 10 else cm.get_cmap('viridis')
            except AttributeError:
                cmap = plt.colormaps['tab10'] if len(unique_groups) <= 10 else plt.colormaps['viridis']
            colors = cmap(np.linspace(0, 1, len(unique_groups)))

            try:
                for i, (name, group) in enumerate(plot_data.groupby(fmt['groupby'])):
                    color = colors[i]
                    ax.plot(group[x_col], group[y_col], label=name,
                            marker=fmt['marker'], linestyle=fmt['linestyle'], ms=fmt['ms'], color=color)
                if fmt['legend']:
                    # Place legend outside plot area if possible, adjust as needed
                    ax.legend(bbox_to_anchor=(1.02, 1.0), loc='upper left', borderaxespad=0.)
                    # Adjust layout to prevent legend overlap
                    plt.tight_layout(rect=[0, 0, 0.85, 1]) # Adjust right boundary to make space for legend
            except Exception as e:
                 print(f"An error occurred during grouped plotting: {e}")
                 # Fallback or re-raise depending on desired robustness
                 ax.plot(plot_data[x_col], plot_data[y_col], label='All data (grouped plot failed)',
                        marker=fmt['marker'], linestyle=fmt['linestyle'], ms=fmt['ms'])
        else:
            ax.plot(plot_data[x_col], plot_data[y_col],
                    marker=fmt['marker'], linestyle=fmt['linestyle'], ms=fmt['ms'])

        # Set labels and title
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_title(fmt['title'])
        ax.grid(True, linestyle='--', alpha=0.6) # Add a light grid for better readability

    elif isinstance(data, (list, tuple)) and len(data) == 2:
        x_data = np.array(data[0], dtype=float)
        y_data = np.array(data[1], dtype=float)
        
        if opt['dropna']:
            valid = ~(np.isnan(x_data) | np.isnan(y_data))
            x_data = x_data[valid]
            y_data = y_data[valid]

        ax.plot(x_data, y_data, marker=fmt['marker'], linestyle=fmt['linestyle'], ms=fmt['ms'])
        
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_title(fmt['title'])
        ax.grid(True, linestyle='--', alpha=0.6)
    else:
        raise TypeError("Input data must be a pandas DataFrame or a sequence of two 1D numpy arrays: [x_array, y_array]")

    if fmt['show']:
        # If legend was potentially added outside, ensure layout is adjusted before showing
        if fmt.get('groupby') is not None and isinstance(data, pd.DataFrame):
             try:
                 # Ensure tight_layout is called again in case it wasn't called due to plotting error
                 fig.tight_layout(rect=[0, 0, 0.85, 1])
             except Exception: # Handle cases where figure might not be valid
                 pass
        else:
             try:
                 fig.tight_layout()
             except Exception:
                 pass
        plt.show()

    return ax
