#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from typing import Union, Optional, Any, Dict, Sequence

from ..parameters import getnames_major
from ..utils import closure

def tas_diagram(fmt: Optional[Dict[str, Any]] = None, ax: Optional[plt.Axes] = None) -> plt.Axes:
    """
    tas_diagram(fmt=None, ax=None) 

    Draw the TAS diagram. The fmt dictionary can change the default format of the
    elements in the diagram. 

    """
    fmt_default = {'title':"TAS diagram (Le Maitre et al., 1989)",
                    'abbrev':False,
                    'show':False
                    }
    if fmt is None: fmt = {}
    for key in fmt_default:
        if key not in fmt:
            fmt[key] = fmt_default[key]

    if ax is None:
        fig = plt.figure()
        ax  = fig.add_subplot(111)
    
    # Draw the lines
    ax.plot((41,41,45),(0.5,3,3), '-k') #picrobasalt
    ax.plot((45,45,52),(0.5,5,5), '-k') #basalt
    ax.plot((52,52,57),(0.5,5,5.9), '-k') #basaltic andesite
    ax.plot((57,57,63),(0.5,5.9,7), '-k') #andesite
    ax.plot((63,63,69),(0.5,7,8), '-k') #dacite
    ax.plot((69,69,77),(13,8,0.5), '-k') #rhyolite
    
    ax.plot((45,49.4,52),(5,7.3,5), '-k') #trachybasalt
    ax.plot((49.4,53,57),(7.3,9.3,5.9), '-k') #basaltic trachyandesite
    ax.plot((53,57.6,63),(9.3,11.7,7), '-k') #trachyandesite
    ax.plot((57.6,61),(11.7,13.5), '-k') #trachyte
    ax.plot((41,41,45),(3,7,9.4), '--k') #basanita / tephrita
    ax.plot((49.4,45,48.4),(7.3,9.4,11.5), '-k') #phonotephrite
    ax.plot((53,48.4,52.5),(9.3,11.5,14), '-k') #tephriphonolite
    ax.plot((57.6,52.5,49),(11.7,14,15.571), '-k') #phonolite

    ax.plot((39.2, 40, 43.2, 45, 48, 50, 53.7, 55, 60, 65, 77.4), \
            (0, 0.4, 2, 2.8, 4, 4.75, 6, 6.4, 8, 8.8, 10), 'k--', linewidth='0.7')

    # Set axis limits and text
    ax.set_xlim(40, 78)
    ax.set_ylim(0,15)    
    ax.set_xlabel('SiO$_2$ (%wt)')
    ax.set_ylabel('Na$_2$O + K$_2$O (wt%)')

    ax.set_title(fmt['title'])

    # Add labels in each field

    if fmt['abbrev']:
        ax.text(42.5,1,'PB', fontsize=8)
        ax.text(48,1,'B', fontsize=8)
        ax.text(54,1,'BA', fontsize=8)
        ax.text(59.5,1,'A', fontsize=8)
        ax.text(67,1,'D', fontsize=8)
        ax.text(74,8,'R', fontsize=8)

        ax.text(48.5,5.8,'TB', fontsize=8)
        ax.text(52,7,'BTA', fontsize=8)
        ax.text(57,8.2,'TA', fontsize=8)
        ax.text(64,10,'T', fontsize=8)
        ax.text(43.5,6.5,'TP', fontsize=8)
        ax.text(48,9.35,'PTP', fontsize=8)
        ax.text(52,11.6,'TPH', fontsize=8)
        ax.text(57,13.5,'PH', fontsize=8)
        ax.text(44,11,'F', fontsize=8)
    else:
        ax.text(41.5, 1.5, 'Picro-', fontsize=7)
        ax.text(41.5, 1, 'basalt', fontsize=7)
        ax.text(47.5, 1, 'Basalt', fontsize=7)
        ax.text(53, 1.5, 'Basaltic', fontsize=7)
        ax.text(53, 1, 'andesite', fontsize=7)
        ax.text(58.2, 1, 'Andesite', fontsize=7)
        ax.text(66, 1, 'Dacite', fontsize=7)
        ax.text(72, 7.5, 'Rhyolite', fontsize=7)
        ax.text(43, 7.5, 'Tephrite', fontsize=7)
        ax.text(42.5, 7, '(Ol < 10%)', fontsize=7)
        ax.text(42.2, 6.2, 'Basanite', fontsize=7)
        ax.text(42, 5.6, '(Ol > 10%)', fontsize=7)
        ax.text(47.6, 5.9, 'Trachy-', fontsize=7)
        ax.text(47.6, 5.4, 'basalt', fontsize=7)
        ax.text(51, 7.5, 'Basaltic', fontsize=7)
        ax.text(50.5, 7, 'trachyandesite', fontsize=7)
        ax.text(54.5, 9, 'Trachyandesite', fontsize=7)
        ax.text(61, 11.5, 'Trachyte', fontsize=7)
        ax.text(60.8, 11, '(Q < 20%)', fontsize=7)
        ax.text(61, 10, 'Trachydacite', fontsize=7)
        ax.text(61.4, 9.5, '(Q > 20%)', fontsize=7)
        ax.text(43, 12, 'Foidite', fontsize=7)
        ax.text(46, 9.3, 'Phonotephrite', fontsize=7)
        ax.text(50, 11.5, 'Tephriphonolite', fontsize=7)
        ax.text(55, 14, 'Phonolite', fontsize=7)

    if fmt['show']:
        plt.show()

def TAS(data: Union[pd.DataFrame, Sequence[np.ndarray]] = None, fmt: Optional[Dict[str, Any]] = None, opt: Optional[Dict[str, Any]] = None, ax: Optional[plt.Axes] = None) -> plt.Axes:
    """
    TAS(data=df, fmt=None, opt=None, ax=None)

    Creates a TAS diagram and plots the data given in df.
    The data must be in the format of a pandas DataFrame with the structure
    explained in the documentation files, OR a sequence of two 1D numpy arrays
    [SiO2, Na2O+K2O] for the x and y axes.

    The fmt dictionary can change the default format of the elements in the diagram. 
    fmt_default =  {'title':"TAS diagram (Le Maitre et al., 1989)",
                    'abbrev':False,
                    'groupby':None,
                    'marker':'o', 'linestyle':'', 'ms':6
                    }

    The opt dictionary can change the default behaviour/procedure.
    opt_default =  {'closure':True,   
                    'dropna':True}
    """
    opt_default =  {'closure':True, 
                    'dropna':True}
    if opt is None: opt = {}
    for key in opt_default:
        if key not in opt:
            opt[key] = opt_default[key]

    fmt_default =  {'title':"TAS diagram (Le Maitre et al., 1989)",
                    'abbrev':False,
                    'groupby':None,
                    'marker':'o', 'linestyle':'', 'ms':6,
                    'show':True
                    }
    if fmt is None: fmt = {}
    for key in fmt_default:
        if key not in fmt:
            fmt[key] = fmt_default[key]

    if ax is None:
        fig = plt.figure()
        ax  = fig.add_subplot(111)

    fmt_diag = fmt.copy()
    fmt_diag['show'] = False
    tas_diagram(fmt=fmt_diag,ax=ax)

    MAJOR_OXIDES = getnames_major()

    if isinstance(data, pd.DataFrame):     # Check that the data is in format of pandas Dataframe

        df_major = data[MAJOR_OXIDES].copy()

        Nrows_orig = df_major.shape[0]        #total number of samples
        Nrows_nan  = df_major.isnull().any(axis=1).sum()  #samples with NaN values

        #apply closure to the data
        if opt['closure']: 
            df_major = closure(df_major, 100)
        else:
            print("Major elements have not been normalized (closed) to 100 wt before plotting.")

        if fmt['groupby'] is not None:
            if fmt['groupby'] in data.columns:
                column_label = fmt['groupby']
                df_major[column_label] = data[column_label]
            else:
                print(f"No column with the name {fmt['groupby']}")
                fmt['groupby'] = None

        #drop samples with NaN
        if Nrows_nan>0 and opt['dropna']: 
            df_major.dropna(inplace=True)
            print(f"{Nrows_nan} samples of a total of {Nrows_orig} have been removed for having missing values.")
        elif Nrows_nan>0:
            print(f"{Nrows_nan} samples with missing values have been kept for plotting.")

        #create new column with alcalis from closed data
        df_major['alcalis'] = df_major['Na2O'] + df_major['K2O']

        #scatter plot silica vs alcalis on top of TAS diagram
        if fmt['groupby'] is not None:
            unique_groups = df_major[column_label].unique()
            try:
                cmap = cm.get_cmap('tab10') if len(unique_groups) <= 10 else cm.get_cmap('viridis')
            except AttributeError:
                cmap = plt.colormaps['tab10'] if len(unique_groups) <= 10 else plt.colormaps['viridis']
            colors = cmap(np.linspace(0, 1, len(unique_groups)))
            
            for i, (name, group) in enumerate(df_major.groupby(column_label)):
                color = colors[i]
                ax.plot(group.SiO2, group.alcalis, label=name, \
                        marker=fmt['marker'], linestyle=fmt['linestyle'], ms=fmt['ms'], color=color)
            ax.legend(bbox_to_anchor=(1.02, 1.05), loc='upper left')
        else:
            ax.plot(df_major.SiO2, df_major.alcalis, label='All data', \
                    marker=fmt['marker'], linestyle=fmt['linestyle'], ms=fmt['ms'])

    elif isinstance(data, (list, tuple)) and len(data) == 2:
        sio2 = np.array(data[0], dtype=float)
        alcalis = np.array(data[1], dtype=float)
        
        # apply dropna
        if opt['dropna']:
            valid = ~(np.isnan(sio2) | np.isnan(alcalis))
            sio2 = sio2[valid]
            alcalis = alcalis[valid]

        ax.plot(sio2, alcalis, label='All data', \
                marker=fmt['marker'], linestyle=fmt['linestyle'], ms=fmt['ms'])
    else:
        if data is not None:
            raise TypeError("Input data must be a pandas DataFrame or a sequence of two 1D numpy arrays: [SiO2, Na2O+K2O]")

    if fmt['show']:
        plt.show()
    return ax

