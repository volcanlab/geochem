#!/usr/bin/env python

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from typing import Union, List, Optional, Any, Dict

from ..parameters import getvalues_SM89
#from ..utils import closure

def spiderplot(data: Union[pd.DataFrame, np.ndarray], elements: List[str] = None, fmt: Optional[Dict[str, Any]] = None, opt: Optional[Dict[str, Any]] = None, ax: Optional[plt.Axes] = None) -> plt.Axes:
    """
    spiderplot(data, elements=None, fmt=None, opt=None, ax=None)

    Plots the dataframe or array values with a logarithmic scale on the y-axis.
    
    Parameters:
    - data: The input dataframe with the elements (column names) and values ready to be plotted, or a 2D numpy array (samples x elements).
    - elements: A list of columns names of the elements to be plotted. Required.
    - fmt: dictionary for changing the default format in the diagram
    - opt: dictionary for changing the default options for processing the data
    - ax: The axis object to plot on. If not provided, a new figure and axis will be created.
    """
    if elements is None:
        raise ValueError("elements list must be provided")

    fmt_default =  {'title':"",
                    'groupby':None,
                    'markers': ['o', 's', '^', 'v', '<', '>', 'p', 'x', 'H', '+', '*', 'D', '|', '_', 'd'],
                    'markersize': 6,
                    'fmt_plt': None,
                    'label': None,
                    'show':True
                    }
    if fmt is None: fmt = {}
    for key in fmt_default:
        if key not in fmt:
            fmt[key] = fmt_default[key]

    opt_default =  {'dropna':False}
    if opt is None: opt = {}
    for key in opt_default:
        if key not in opt:
            opt[key] = opt_default[key]

    if ax is None:
        _, ax = plt.subplots()
    
    markers = fmt['markers']
    ms = fmt['markersize']
    
    if isinstance(data, pd.DataFrame):
        for element in elements:
            if element not in data.columns:
                print(f'{element} is not in the data')
                elements.remove(element)

        df = data[elements].copy()

        if opt['dropna']:
            df.dropna(inplace=True)

        if (fmt['groupby'] is not None) and (fmt['fmt_plt'] is None):
            if fmt['groupby'] in data.columns:
                column_label = fmt['groupby']
                df[column_label] = data[column_label]
                df = df.set_index(column_label)

                grouped = df.groupby(column_label)
                num_groups = len(grouped)
                try:
                    cmap = cm.get_cmap('tab10') if num_groups <= 10 else cm.get_cmap('viridis')
                except AttributeError:
                    cmap = plt.colormaps['tab10'] if num_groups <= 10 else plt.colormaps['viridis']
                colors = cmap(np.linspace(0, 1, num_groups))

                i_category = -1
                for (name, group) in grouped:
                    i_category += 1
                    color = colors[i_category]
                    marker = markers[i_category % len(markers)]
                    new_category = True
                    for index, row in group.iterrows():
                        label = name if new_category else None
                        ax.plot(row.index, row.values, marker=marker, color=color, label=label, linestyle='-', ms=ms)
                        new_category = False

                ax.legend(bbox_to_anchor=(1.02, 1.05), loc='upper left')
            else:
                print(f"No column with the name {fmt['groupby']}")
                fmt['groupby'] = None        
        else:
            num_samples = len(df)
            try:
                cmap = cm.get_cmap('tab10') if num_samples <= 10 else cm.get_cmap('viridis')
            except AttributeError:
                cmap = plt.colormaps['tab10'] if num_samples <= 10 else plt.colormaps['viridis']
            colors = cmap(np.linspace(0, 1, num_samples))
            
            for index, (_, row) in enumerate(df.iterrows()):
                if fmt['fmt_plt'] is None:
                    marker = markers[index % len(markers)]
                    color = colors[index % len(colors)] if len(colors) > 0 else 'b'
                    ax.plot(row.index, row.values, marker=marker, color=color, linestyle='-', ms=ms)
                else:
                    ax.plot(row.index, row.values, label=fmt['label'], **fmt['fmt_plt'])

    elif isinstance(data, np.ndarray):
        arr = np.array(data, dtype=float)
        if arr.ndim == 1:
            arr = arr.reshape(1, -1)
        
        if arr.shape[1] != len(elements):
            raise ValueError(f"Array shape {arr.shape} does not match elements length {len(elements)}")

        if opt['dropna']:
            valid = ~np.isnan(arr).any(axis=1)
            arr = arr[valid]

        num_samples = arr.shape[0]
        try:
            cmap = cm.get_cmap('tab10') if num_samples <= 10 else cm.get_cmap('viridis')
        except AttributeError:
            cmap = plt.colormaps['tab10'] if num_samples <= 10 else plt.colormaps['viridis']
        colors = cmap(np.linspace(0, 1, num_samples))

        x_coords = np.arange(len(elements))
        for i in range(num_samples):
            if fmt['fmt_plt'] is None:
                marker = markers[i % len(markers)]
                color = colors[i]
                ax.plot(x_coords, arr[i], marker=marker, color=color, linestyle='-', ms=ms)
            else:
                ax.plot(x_coords, arr[i], label=fmt['label'], **fmt['fmt_plt'])

        ax.set_xticks(x_coords)
        ax.set_xticklabels(elements)

    else:
        raise TypeError("Input data must be a pandas DataFrame or a 2D numpy array.")

    ax.set_yscale('log')
    ax.set_title(fmt['title'])

    if fmt['show']:
        plt.show()
    return ax

def spider_norm(data: Union[pd.DataFrame, np.ndarray], elements: List[str] = None, values: Dict[str, float] = None) -> Union[pd.DataFrame, np.ndarray, None]:
    """
    spider_norm(data, elements=None, values=None):

    This function returns a new DataFrame or numpy array with the elements in 'data' normalized
    by the values found in 'values'.
    """
    if elements is None or values is None:
        return None

    if isinstance(data, pd.DataFrame):
        found_values = []
        present_elements = []
        for element in elements:
            if (element in values) and (element in data.columns):
                found_values.append(values[element])
                present_elements.append(element)

        if len(present_elements) > 0:
            df = data[present_elements].copy()
            df = df / np.array(found_values)
            return df
        else:
            print('No normalization values for the elements selected, or the elements are not in the data.')
            return None
    elif isinstance(data, np.ndarray):
        arr = np.array(data, dtype=float)
        if arr.ndim == 1:
            arr = arr.reshape(1, -1)
        if arr.shape[1] != len(elements):
            raise ValueError("Array columns do not match elements length")
            
        found_values = []
        for element in elements:
            if element in values:
                found_values.append(values[element])
            else:
                found_values.append(np.nan) # Handle missing normalizations safely
        
        return arr / np.array(found_values)
    return None

def spider(data: Union[pd.DataFrame, np.ndarray], elements: List[str] = None, norm: str = 'chondrite', fmt: Optional[Dict[str, Any]] = None, opt: Optional[Dict[str, Any]] = None, ax: Optional[plt.Axes] = None) -> plt.Axes:
    """
    spider(data, elements=None, normalize='chondrite', fmt=None, opt=None, ax=None)

    Parameters:
    - data is a pandas DataFrame or 2D numpy array with the dataset
    - elements is the list of column names (elements) that will be plotted
    - normalize options from the Sun and McDonough (1989) dataset
        "chondrite" -> C1 chondrite
        "mantle"    -> Primtive Mantle
        "nmorb"     -> N-type MORB
    """
    if elements is None:
        raise ValueError("elements must be provided")

    values = getvalues_SM89(norm)

    norm_data = spider_norm(data, elements, values)

    if norm_data is not None:
        if isinstance(norm_data, pd.DataFrame):
            # Maintain groupby column if present and needed
            if isinstance(data, pd.DataFrame) and fmt is not None and fmt.get('groupby') is not None:
                if fmt['groupby'] in data.columns:
                    norm_data[fmt['groupby']] = data[fmt['groupby']]
            # Only keep elements that successfully normalized
            elements = list(norm_data.columns)
            if fmt is not None and fmt.get('groupby') in elements:
                elements.remove(fmt['groupby'])

        if norm == 'mantle':
            normalization = 'Primitive Mantle'
        elif norm == 'nmorb':
            normalization = 'N-MORB'
        else:
            normalization = norm

        if fmt is None: 
            fmt = {}
            show_after = True
        else:
            show_after = fmt.get('show', True)
            
        fmt_spider = fmt.copy()
        fmt_spider['show'] = False

        if ax is None:
            _, ax = plt.subplots()
            
        spiderplot(norm_data, elements, fmt=fmt_spider, opt=opt, ax=ax)
        ax.set_ylabel('Rock/'+normalization)

        if show_after:
            plt.show()
        return ax
    else:
        raise ValueError('Error normalizing the data')
