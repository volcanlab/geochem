#!/usr/bin/env python

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from typing import Union, List, Tuple, Optional, Any, Dict, Sequence

from ..parameters import getnames_major, getvalues_IB71xy
from ..utils import closure

def convert_abc_to_xy(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    x, y = convert_abc_to_xy(a, b, c)

    Convert the a, b, c coordinates of a triangle to x, y coordinates
    in the triangle plot.

    The triangle is defined by the vertices a, b, c, which are
    respectively the points (0,0), (0.5, sqrt(3)/2), (1,0); 
    a is the component on the bottom-left side, b is the component on 
    the top-middle side, and c is the component on the bottom-right side.

    a, b and c must be 1D numpy arrays
    """
    s = 2*(a+b+c)
    x = (b+(2*c))/s
    y = b*np.sqrt(3)/s
    return x, y

def triangle(fmt: Optional[Dict[str, Any]] = None, ax: Optional[plt.Axes] = None) -> plt.Axes:
    """
    triangle(fmt=None, ax=None)
    
    This function draws a triangle with labels at the vertices
    specified in the dictionary *fmt*.
    If *verts* is None in *fmt*, no labels are added to the plot.

    fmt_default = { 'title':None,
                    'verts':('X','Y','Z'),
                    'vertsize':12, #fontsize of labels in vertices
                    'fmt_plt': {'linestyle':'solid', 'color':'black'},
                    'show':False   #whether it shows it (plt.show)   
                }    
    """
    fmt_default = { 'title':None,
                    'verts':('X','Y','Z'),
                    'vertsize':12, #fontsize of labels in vertices
                    'fmt_plt': {'linestyle':'solid', 'color':'black'},
                    'show':False   #whether it shows the plot (plt.show)   
                    }
    if fmt is None: fmt = {}
    for key in fmt_default:
        if key not in fmt:
            fmt[key] = fmt_default[key]

    if ax is None:
        fig = plt.figure()
        ax  = fig.add_subplot(111)

    ax.set_frame_on(False)

    ax.plot((0, 1), (0, 0), **fmt['fmt_plt'])
    ax.plot((1, 0.5), (0, 0.86603), **fmt['fmt_plt'])
    ax.plot((0.5, 0), (0.86603, 0), **fmt['fmt_plt'])

    # Add names in the corners
    h1 = fmt['vertsize']/500 * len(fmt['verts'][0])
    h2 = (fmt['vertsize']/500 * len(fmt['verts'][1]))/2
    ax.text(-0.025-h1 , -0.02, fmt['verts'][0], fontsize=fmt['vertsize'])
    ax.text(0.5-h2   ,  0.89, fmt['verts'][1], fontsize=fmt['vertsize'])
    ax.text(1.02     , -0.02, fmt['verts'][2], fontsize=fmt['vertsize'])

    ax.set_xticks([])
    ax.set_yticks([])

    ax.set_aspect("equal")
    
    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-0.1, 1.)

    if fmt['title'] is not None:
        ax.set_title(fmt['title'])

    if fmt['show']:
        plt.show()
    return ax

def tridata(x: np.ndarray = None, y: np.ndarray = None, z: np.ndarray = None, fmt: Optional[Dict[str, Any]] = None, ax: Optional[plt.Axes] = None) -> Optional[plt.Axes]:
    """
    tridata(x, y, z, fmt=None, ax=None)
    
    This function plots 3-component compositional data: x, y, z
    
    Inputs
        x, y, z Numpy 1D arrays
        fmt: dictionary for changing the default format of the elements in the diagram

    fmt_default =  {'fmt_str':None,
                    'fmt_plt': {'marker':'o', 'linestyle':'', 'ms':6},
                    'label': None,
                    'show':True
                    }
    """
    fmt_default =  {'fmt_str':None,
                    'fmt_plt': {'marker':'o', 'linestyle':'', 'ms':6},
                    'label': None,
                    'show':True
                    }
    if fmt is None: fmt = {}
    for key in fmt_default:
        if key not in fmt:
            fmt[key] = fmt_default[key]

    if (x is not None) and (y is not None) and (z is not None):

        if ax is None:
            fig = plt.figure()
            ax  = fig.add_subplot(111)

            ax.set_frame_on(False)
            ax.set_xticks([])
            ax.set_yticks([])

            ax.set_aspect("equal")
            
            ax.set_xlim(-0.1, 1.1)
            ax.set_ylim(-0.1, 1.)

        xt, yt = convert_abc_to_xy(x, y, z)
        
        if fmt['fmt_str'] is None:
            ax.plot(xt,yt, label=fmt['label'], **fmt['fmt_plt'])
        else:
            ax.plot(xt,yt, fmt['fmt_str'], label=fmt['label'])

        if fmt['show']:
            plt.show()
        return ax
    else:
        print("No data provided to plot")
        return ax

def AFM(data: Union[pd.DataFrame, Sequence[np.ndarray]] = None, fmt: Optional[Dict[str, Any]] = None, opt: Optional[Dict[str, Any]] = None, ax: Optional[plt.Axes] = None) -> plt.Axes:
    """
    AFM(data=None, fmt=None, opt=None, ax=None)

    Creates the AFM diagram and plots the data given in df.
    The data must be in the format of a pandas DataFrame with the structure
    explained in the README.md file OR a sequence of three 1D numpy arrays
    [A, F, M] for the ternary plot components. 
    If a DataFrame, the following four fields must be present: 'Na2O','K2O','FeOT','MgO'.

    The fmt dictionary can change the default format of the elements in the diagram. 
    fmt_default =  {'title': "",
                    'verts':('A','F','M'),
                    'vertsize':12, #fontsize of labels in vertices
                    'groupby':None,
                    'fmt_str':None,
                    'fmt_plt': {'marker':'o', 'linestyle':'', 'ms':6},
                    'show':True
                    }

    The opt dictionary can change the default behaviour/procedure.
    opt_default =  {'closure':True,   
                    'dropna':True,
                    'I&B71':True
                    }    
    """
    fmt_default =  {'title':"",
                    'verts':('A','F','M'),
                    'vertsize':12, 
                    'groupby':None,
                    'fmt_str':None,
                    'fmt_plt': {'marker':'o', 'linestyle':'', 'ms':6},
                    'show':True
                    }
    if fmt is None: fmt = {}
    for key in fmt_default:
        if key not in fmt:
            fmt[key] = fmt_default[key]

    opt_default =  {'closure':True, 
                    'dropna':True,
                    'I&B71':True
                    }
    if opt is None: opt = {}
    for key in opt_default:
        if key not in opt:
            opt[key] = opt_default[key]

    if ax is None:
        fig = plt.figure()
        ax  = fig.add_subplot(111)

    # Draw the triangle
    fmt_fig = fmt.copy()
    fmt_fig['show'] = False
    fmt_fig['fmt_plt'] = {'linestyle':'solid', 'color':'black'}
    triangle(fmt=fmt_fig, ax=ax)

    # Draw the Irvine and Baragar's line 
    if opt['I&B71']:
        x,y = getvalues_IB71xy()
        ax.plot(x,y, label='Irvine & Baragar (1971)', 
                color='black', linestyle='-', linewidth=1)

    MAJOR_OXIDES = getnames_major()
    
    if isinstance(data, pd.DataFrame):     # Check that the data is in format of pandas Dataframe

        df_major = data[MAJOR_OXIDES].copy()

        #apply closure to the data
        if opt['closure']: 
            df_major = closure(df_major, 100)
        else:
            print("Major elements have not been normalized (closed) to 100 wt before plotting.")

        df_major = df_major[['Na2O','K2O','FeOT','MgO']]

        if fmt['groupby'] is not None:
            if fmt['groupby'] in data.columns:
                column_label = fmt['groupby']
                df_major[column_label] = data[column_label]
            else:
                print(f"No column with the name {fmt['groupby']}")
                fmt['groupby'] = None

        #total number of samples
        Nrows_orig = df_major.shape[0]
        #samples with NaN values
        Nrows_nan  = df_major.isnull().any(axis=1).sum()

        #drop samples with NaN
        if Nrows_nan>0 and opt['dropna']: 
            df_major.dropna(inplace=True)
            print(f"{Nrows_nan} samples of a total of {Nrows_orig} have been removed for having missing values.")
        elif Nrows_nan>0:
            print(f"{Nrows_nan} samples with missing values have been kept for plotting.")

        #create new column with alcalis from closed data
        df_major['alcalis'] = df_major['Na2O'] + df_major['K2O']

        #scatter plot A-F-M
        if fmt['groupby'] is not None:
            unique_groups = df_major[column_label].unique()
            try:
                cmap = cm.get_cmap('tab10') if len(unique_groups) <= 10 else cm.get_cmap('viridis')
            except AttributeError:
                cmap = plt.colormaps['tab10'] if len(unique_groups) <= 10 else plt.colormaps['viridis']
            colors = cmap(np.linspace(0, 1, len(unique_groups)))
            
            for i, (name, group) in enumerate(df_major.groupby(column_label)):
                A = group.alcalis
                F = group.FeOT
                M = group.MgO
                
                xt, yt = convert_abc_to_xy(A, F, M)
                color = colors[i]
                
                if fmt['fmt_str'] is None:
                    ax.plot(xt, yt, label=name, color=color, **fmt['fmt_plt'])
                else:
                    ax.plot(xt, yt, fmt['fmt_str'], label=name, color=color)

            ax.legend(bbox_to_anchor=(1.02, 1.05), loc='upper left')
        else:
            A = df_major.alcalis
            F = df_major.FeOT
            M = df_major.MgO

            xt, yt = convert_abc_to_xy(A, F, M)

            ax.plot(xt,yt, label='All data', **fmt['fmt_plt'])

    elif isinstance(data, (list, tuple)) and len(data) == 3:
        A = np.array(data[0], dtype=float)
        F = np.array(data[1], dtype=float)
        M = np.array(data[2], dtype=float)
        
        if opt['dropna']:
            valid = ~(np.isnan(A) | np.isnan(F) | np.isnan(M))
            A = A[valid]
            F = F[valid]
            M = M[valid]

        xt, yt = convert_abc_to_xy(A, F, M)
        if fmt['fmt_str'] is None:
            ax.plot(xt, yt, label='All data', **fmt['fmt_plt'])
        else:
            ax.plot(xt, yt, fmt['fmt_str'], label='All data')
    else:
        if data is not None:
            raise TypeError("Input data must be a pandas DataFrame or a sequence of three 1D numpy arrays: [A, F, M]")

    if fmt['show']:
        plt.show()
    return ax


def triangle_lineplot(icomp: int = 0, perc: Union[float, List[float], np.ndarray] = 0.5, dl: float = 0.01, fmt: Optional[Dict[str, Any]] = None, returnline: bool = False, ax: Optional[plt.Axes] = None) -> Optional[np.ndarray]:
    """
    x = triangle_lineplot(icomp=0, perc=0.5, dl=0.01, fmt=None, returnline=False)
    
    This function draws lines parallel to the sides of the triangle, at 
    percentages specified as fractions (0-1) in *perc*.
    
    Input 
        icomp: the index 0,1 or 2 of the component opposite to this line 
        perc: list/tuple/numpy 1darray with the percentages at which the lines are drawn
        dl: resolution of the line, as a sequence of points
        fmt: dictionary with detailed formatting 
        returnline: whether the function returns the line
        ax: figure axis to draw the lines on

    fmt_default =  {'fmt_str':None,
                    'fmt_plt': {'marker':'', 'linestyle':'solid', 'ms':6, 'color':'black'},
                    'label': None,
                    'show':False
                    }

    Output
        x (only if returnline is True) is a Numpy array with the points 
        that create the line(s)
    """
    fmt_default =  {'fmt_str':None,
                    'fmt_plt': {'marker':'', 'linestyle':'solid', 'ms':6},
                    'label': None,
                    'show':False
                    }
    if fmt is None: fmt = {}
    for key in fmt_default:
        if key not in fmt:
            fmt[key] = fmt_default[key]

    l  = np.arange(0.+dl, 1., dl)

    if isinstance(perc, (float, int)):
        perc = [perc]
        
    for p in perc:
        X  = np.array([[1.,0.,0.]])
        for v1 in l:
            if icomp == 0:
                row = (p, (1.-p)*v1, (1.-p)*(1.-v1))
            elif icomp == 1:
                row = ((1.-p)*v1, p, (1.-p)*(1.-v1))
            else:
                row = ((1.-p)*v1, (1.-p)*(1.-v1), p)
            X = np.vstack([X, row])
        X = np.delete(X, 0, 0)

        if not returnline:
            tridata(X[:,0], X[:,1], X[:,2], fmt=fmt, ax=ax)

    if returnline:
        return X
