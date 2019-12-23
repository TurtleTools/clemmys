import numpy as np


def linewidth_from_data_units(linewidth, axis, reference='x'):
    """
    get relative linewidth

    Parameters
    ----------
    linewidth
    axis
    reference
    """
    fig = axis.get_figure()
    if reference == 'x':
        length = fig.bbox_inches.width * axis.get_position().width
        value_range = np.diff(axis.get_xlim())
    else:
        length = fig.bbox_inches.height * axis.get_position().height
        value_range = np.diff(axis.get_ylim())
    length *= 72
    return linewidth * (length / value_range)


def remove_spines(ax):
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    return ax
