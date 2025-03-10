
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from mpl_toolkits.axes_grid1.inset_locator import inset_axes
def plot_one_set_t1(df,ax, E_e, subax_val, lname='ansatz', ctype=['EfficientSU2','noiseless'], L=2, legend = True):
    counts = np.arange(len(df[df.columns[1:][0]]))
    color_list = ['green','brown','cyan','pink','blue','magenta','purple']
    for i in range(len(df.columns[1:])):
        ax.plot(counts, df[df.columns[1:][i]], color = color_list[i], label = f'{lname}_{df.columns[1:][i][-2:]}')
    ax.axhline(E_e, color = 'red', linestyle = 'dotted', label = 'Exact energy')
    ax.set_xlabel("Eval count", fontsize = 13)
    ax.set_ylabel("Energy", fontsize = 13)

    ax.set_title(f'{ctype[0]} ({ctype[1]} simulator)',
          fontsize = 14)

    sub_ax = inset_axes(
        parent_axes=ax,
        width="40%",
        height="30%",
        borderpad=1  # padding between parent and inset axes
    )
    for i in range(len(df.columns[1:])):
        sub_ax.plot(counts, df[df.columns[1:][i]], color = color_list[i], label = f'{lname}_{df.columns[1:][i][-2:]}')
    sub_ax.axhline(E_e, color = 'red', linestyle = 'dotted', label = 'Exact energy')
    sub_ax.axis(subax_val)
    if legend:
        ax.legend(loc='best', bbox_to_anchor=(0.3, 0.19, 0.2, 0.8))