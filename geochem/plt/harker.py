import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Union, List, Optional, Any, Dict, Sequence

from .scatter import scatter
from ..parameters import getnames_major

def harker(data: Union[pd.DataFrame, Sequence[np.ndarray]], x_col: str = 'SiO2', y_cols: Optional[List[str]] = None, fmt: Optional[Dict[str, Any]] = None, opt: Optional[Dict[str, Any]] = None) -> plt.Figure:
    """
    Creates a Harker diagram (grid of scatter plots) for geochemical data.
    
    Args:
        data: pd.DataFrame or a sequence of numpy arrays [x_array, y_array_1, y_array_2, ...].
        x_col: The column name for the x-axis (default 'SiO2').
        y_cols: List of column names for the y-axes. If None, defaults to major oxides.
        fmt: Formatting options (see scatter function). When using `groupby`,
            the Harker figure shows a single shared legend. Optional
            figure-level legend keys are:
            `legend_loc`, `legend_bbox_to_anchor`, and `legend_ncol`.
        opt: Options dictionary.
        
    Returns:
        plt.Figure: The generated figure containing the grid of subplots.
    """
    if fmt is None: fmt = {}
    if opt is None: opt = {}
    
    if y_cols is None:
        if isinstance(data, pd.DataFrame):
            all_majors = getnames_major()
            y_cols = [col for col in all_majors if col in data.columns and col != x_col]
        elif isinstance(data, (list, tuple)):
            y_cols = [f'Y{i}' for i in range(1, len(data))]
            
    num_plots = len(y_cols)
    if num_plots == 0:
        raise ValueError("No y-variables specified or found for plotting.")
        
    # Determine grid size
    ncols = 3
    nrows = math.ceil(num_plots / ncols)
    
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(ncols * 4, nrows * 3.5))
    if nrows * ncols == 1:
        axes = np.array([axes])
    axes = axes.flatten()
    
    fmt_scatter = fmt.copy()
    show_final = fmt_scatter.pop('show', True)
    fmt_scatter['show'] = False
    
    main_title = fmt_scatter.pop('title', 'Harker Diagrams')
    legend_loc = fmt_scatter.pop('legend_loc', 'lower center')
    legend_bbox_to_anchor = fmt_scatter.pop('legend_bbox_to_anchor', (0.5, 0.0))
    legend_ncol = fmt_scatter.pop('legend_ncol', None)
    grouped = isinstance(data, pd.DataFrame) and fmt_scatter.get('groupby') is not None
    
    for i, y_col in enumerate(y_cols):
        ax = axes[i]
        
        fmt_sub = fmt_scatter.copy()
        fmt_sub['title'] = '' 
        if grouped:
            fmt_sub['legend'] = False
        
        if isinstance(data, pd.DataFrame):
            scatter(data=data, x_col=x_col, y_col=y_col, fmt=fmt_sub, opt=opt, ax=ax)
        elif isinstance(data, (list, tuple)):
            scatter(data=[data[0], data[i+1]], x_col=x_col, y_col=y_col, fmt=fmt_sub, opt=opt, ax=ax)

    if grouped:
        handles_by_label = {}
        for ax in axes[:num_plots]:
            handles, labels = ax.get_legend_handles_labels()
            for handle, label in zip(handles, labels):
                handles_by_label.setdefault(label, handle)
            legend = ax.get_legend()
            if legend is not None:
                legend.remove()

        if handles_by_label:
            if legend_ncol is None:
                legend_ncol = min(len(handles_by_label), 4)
            fig.legend(
                handles_by_label.values(),
                handles_by_label.keys(),
                loc=legend_loc,
                bbox_to_anchor=legend_bbox_to_anchor,
                ncol=legend_ncol,
            )
            
    # Hide unused axes
    for j in range(num_plots, len(axes)):
        fig.delaxes(axes[j])
        
    fig.suptitle(main_title, fontsize=16)
    if grouped and legend_loc in ('lower center', 'upper center'):
        fig.tight_layout(rect=[0, 0.08, 1, 0.95])
    elif grouped and legend_loc in ('center left', 'center right', 'upper left', 'upper right', 'lower left', 'lower right'):
        fig.tight_layout(rect=[0, 0.03, 0.88, 0.95])
    else:
        fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    if show_final:
        plt.show()
        
    return fig
