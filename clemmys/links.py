import numpy as np
from matplotlib import patches as m_patches
from matplotlib.path import Path as m_Path


def make_semicircle(x1: float, x2: float, y: float, valley: bool, color: str, opacity: float = 1., linewidth: float = 1.):
    """
    Makes a semicircular link between (x1, y) and (x2, y)
    
    Parameters
    ----------
    x1
    x2
    y
    valley
        if True, ∪ else ∩
    color
    opacity
    linewidth

    Returns
    -------
    maximum height of the semicircle (to use when deciding the axis limit), matplotlib patch
    """
    middle = (x1 + x2) / 2
    height = 2 * np.abs(x1 - middle)
    if height == 0:
        return 0, None
    if valley:
        return -height, m_patches.Arc((middle, y), -height, -height, angle=-180, theta1=180, theta2=360,
                                      lw=linewidth, color=color, alpha=opacity)
    else:
        return height, m_patches.Arc((middle, y), height, height, angle=0, theta1=0, theta2=180,
                                     lw=linewidth, color=color, alpha=opacity)


def make_range_semicircle_bracket(x11: float, x12: float, x21: float, x22: float, y: float, valley: bool, color: str, opacity: float = 1.,
                                  linewidth: float = 1.):
    """
    Makes two brackets, one from (x11, y) to (x12, y) and the second from (x21, y) to (x22, y), and connects them with a semicircle

    Parameters
    ----------
    x11
    x12
    x21
    x22
    y
    valley
        if True, ∪ else ∩
    color
    opacity
    linewidth

    Returns
    -------
    maximum height of the semicircle (to use when deciding the axis limit), list of matplotlib patches
    """
    middle_1 = (x11 + x21) / 2
    middle_2 = (x12 + x22) / 2
    if valley:
        y1 = y - 1
    else:
        y1 = y + 1
    p1 = m_patches.FancyArrowPatch(path=m_Path([(middle_1, y), (middle_1, y1)],
                                               [m_Path.MOVETO, m_Path.LINETO]),
                                   fc="none", lw=linewidth, color=color, alpha=opacity,
                                   arrowstyle=m_patches.ArrowStyle.BracketA(widthA=middle_1,
                                                                            lengthA=3,
                                                                            angleA=None))
    height, p2 = make_semicircle(middle_1, middle_2, y1, valley, color, opacity, linewidth)
    p3 = m_patches.FancyArrowPatch(path=m_Path([(middle_2, y), (middle_2, y1)],
                                               [m_Path.MOVETO, m_Path.LINETO]),
                                   fc="none", lw=linewidth, color=color, alpha=opacity,
                                   arrowstyle=m_patches.ArrowStyle.BracketA(widthA=middle_2,
                                                                            lengthA=3,
                                                                            angleA=None))
    return height, [p1, p2, p3]


def make_connection(x1: float, y1: float, x2: float, y2: float, color: str, opacity: float = 1.,
                    linewidth: float = 1., arrow_style: m_patches.ArrowStyle = m_patches.ArrowStyle.Curve()):
    """
    Makes a line (with a particular arrow style) between (x1, y1) and (x2, y2)

    Parameters
    ----------
    x1
    y1
    x2
    y2
    arrow_style
    color
    opacity
    linewidth

    Returns
    -------
    matplotlib patch
    """
    return m_patches.ConnectionPatch((x1, y1), (x2, y2),
                                     "data", "data",
                                     arrowstyle=arrow_style,
                                     edgecolor=color, alpha=opacity, linewidth=linewidth)


def make_range_connection_bracket(x11: float, x12: float, x21: float, x22: float, y1: float, y2: float, arrow_style: m_patches.ArrowStyle, color: str,
                                  opacity: float = 1., linewidth: float = 1.):
    """
    Makes two brackets, one from (x11, y1) to (x12, y1) and the second from (x21, y2) to (x22, y2), and connects them with a line (with given arrow style)

    Parameters
    ----------
    x11
    x12
    x21
    x22
    y1
    y2
    arrow_style
    color
    opacity
    linewidth

    Returns
    -------
    list of matplotlib patches
    """
    middle_1 = (x11 + x21) / 2
    middle_2 = (x12 + x22) / 2
    y11 = y1 + 1
    y21 = y2 + 1
    p1 = m_patches.FancyArrowPatch(path=m_Path([(middle_1, y1), (middle_1, y11)],
                                               [m_Path.MOVETO, m_Path.LINETO]),
                                   fc="none", lw=linewidth, color=color, alpha=opacity,
                                   arrowstyle=m_patches.ArrowStyle.BracketA(widthA=middle_1,
                                                                            lengthA=3,
                                                                            angleA=None))
    p2 = make_connection(middle_1, y11, middle_2, y21, color, opacity, linewidth, arrow_style)
    p3 = m_patches.FancyArrowPatch(path=m_Path([(middle_2, y2), (middle_2, y21)],
                                               [m_Path.MOVETO, m_Path.LINETO]),
                                   fc="none", lw=linewidth, color=color, alpha=opacity,
                                   arrowstyle=m_patches.ArrowStyle.BracketA(widthA=middle_2,
                                                                            lengthA=3,
                                                                            angleA=None))
    return [p1, p2, p3]


def make_curve(x1: float, x2: float, y: float, valley: bool, color: str, opacity: float = 1.,
               linewidth: float = 1., arrow_style: m_patches.ArrowStyle = m_patches.ArrowStyle.Curve()):
    """
    Makes a curved link between (x1, y) and (x2, y) with a given arrow style

    Parameters
    ----------
    x1
    x2
    y
    arrow_style
    valley
        if True, ∪ else ∩
    color
    opacity
    linewidth

    Returns
    -------
    maximum height of the curve (to use when deciding the axis limit), matplotlib patch
    """
    middle = (x1 + x2) // 2
    height = 2 * np.abs(x1 - middle)
    if valley:
        return -height, m_patches.FancyArrowPatch(path=m_Path([(x1, y), (middle, y - height), (x2, y)],
                                                              [m_Path.MOVETO, m_Path.CURVE3, m_Path.CURVE3]),
                                                  fc="none", lw=linewidth, color=color, alpha=opacity,
                                                  arrowstyle=arrow_style)
    else:
        return height, m_patches.FancyArrowPatch(path=m_Path([(x1, y), (middle, y + height), (x2, y)],
                                                             [m_Path.MOVETO, m_Path.CURVE3, m_Path.CURVE3]),
                                                 fc="none", lw=linewidth, color=color, alpha=opacity,
                                                 arrowstyle=arrow_style)


def make_range_curve_bracket(x11: float, x12: float, x21: float, x22: float, y: float, arrow_style: m_patches.ArrowStyle, valley: bool, color: str,
                             opacity: float = 1., linewidth: float = 1.):
    """
    Makes two brackets, one from (x11, y) to (x12, y) and the second from (x21, y) to (x22, y), and connects them with a curve (with given arrow style)

    Parameters
    ----------
    x11
    x12
    x21
    x22
    y
    arrow_style
    valley
        if True, ∪ else ∩
    color
    opacity
    linewidth

    Returns
    -------
    maximum height of the curve (to use when deciding the axis limit), list of matplotlib patches
    """
    middle_1 = (x11 + x21) / 2
    middle_2 = (x12 + x22) / 2
    if valley:
        y1 = y - 1
    else:
        y1 = y + 1
    p1 = m_patches.FancyArrowPatch(path=m_Path([(middle_1, y), (middle_1, y1)],
                                               [m_Path.MOVETO, m_Path.LINETO]),
                                   fc="none", lw=linewidth, color=color, alpha=opacity,
                                   arrowstyle=m_patches.ArrowStyle.BracketA(widthA=middle_1,
                                                                            lengthA=3,
                                                                            angleA=None))
    height, p2 = make_curve(middle_1, middle_2, y1, valley, color, opacity, linewidth, arrow_style)
    p3 = m_patches.FancyArrowPatch(path=m_Path([(middle_2, y), (middle_2, y1)],
                                               [m_Path.MOVETO, m_Path.LINETO]),
                                   fc="none", lw=linewidth, color=color, alpha=opacity,
                                   arrowstyle=m_patches.ArrowStyle.BracketA(widthA=middle_2,
                                                                            lengthA=3,
                                                                            angleA=None))
    return height, [p1, p2, p3]
