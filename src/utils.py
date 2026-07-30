import inspect  # for check()
import re  # for check()
from src.dependency import *

# import numpy as np

# import matplotlib.pyplot as plt
# import matplotlib.gridspec as gridspec

# import pandas as pd
# import time


def check(arg):
    """
    Print information of input arg

    Example
    -------
    import numpy as np

    a = np.zeros((2, 4))

    check(a)

    a+=1

    check(a)

    check(len(a))

    TERMINAL OUTPUT:

    d:\Yu0702\casper-gradient-code\\testofcheckpoint.py @45 a : ndarray(array([[0., 0., 0., 0.], [0., 0., 0., 0.]])) [shape=(2, 4)]

    d:\Yu0702\casper-gradient-code\\testofcheckpoint.py @47 a : ndarray(array([[1., 1., 1., 1.], [1., 1., 1., 1.]])) [shape=(2, 4)]

    d:\Yu0702\casper-gradient-code\\testofcheckpoint.py @48 len(a) : int(2)

    d:\Yu0702\casper-gradient-code\\testofcheckpoint.py @49 a.shape : tuple((2, 4)) [len=2]

    Copyright info:
    ------
    Adopted from https://gist.github.com/HaleTom/125f0c0b0a1fb4fbf4311e6aa763844b

    Author: Tom Hale

    Original comment: Print the line and filename, function call, the class, str representation and some other info
                    Inspired by https://stackoverflow.com/a/8856387/5353461
    """
    frame = inspect.currentframe()
    callerframeinfo = inspect.getframeinfo(frame.f_back)
    try:
        context = inspect.getframeinfo(frame.f_back).code_context
        caller_lines = "".join([line.strip() for line in context])
        m = re.search(r"check\s*\((.+?)\)$", caller_lines)
        if m:
            caller_lines = m.group(1)
            position = (
                str(callerframeinfo.filename) + " line " + str(callerframeinfo.lineno)
            )

            # Add additional info such as array shape or string length
            additional = ""
            if hasattr(arg, "shape"):
                additional += "[shape={}]".format(arg.shape)
            elif hasattr(arg, "__len__"):  # shape includes length information
                additional += "[len={}]".format(len(arg))

            # Use str() representation if it is printable
            str_arg = str(arg)
            str_arg = str_arg if str_arg.isprintable() else repr(arg)

            print(position, "" + caller_lines + " : ", end="")
            print(arg.__class__.__name__ + "(" + str_arg + ")", additional)
        else:
            print("check: couldn't find caller context")
    finally:
        del frame
        del callerframeinfo


okabe_ito_colors = [
    "#000000",  # black
    "#E69F00",  # orange
    "#56B4E9",  # sky blue
    "#009E73",  # bluish green
    # "#F0E442",  # yellow
    # "#0072B2",  # blue
    "#D55E00",  # vermillion
    "#CC79A7",  # reddish purple
]

tab10 = [
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#d62728",
    "#9467bd",
    "#8c564b",
    "#e377c2",
    "#7f7f7f",
    "#bcbd22",
    "#17becf",
]

high_contrast_extended = [
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#d62728",
    "#9467bd",
    "#8c564b",
    "#e377c2",
    "#17becf",
    "#bcbd22",
    "#7f7f7f",
    "#393b79",
    "#637939",
    "#8c6d31",
    "#843c39",
    "#7b4173",
    "#3182bd",
    "#31a354",
    "#756bb1",
    "#636363",
    "#e6550d",
    "#969696",
    "#dd1c77",
]

vivid_colors = [
    "#e41a1c",
    "#377eb8",
    "#4daf4a",
    "#984ea3",
    "#ff7f00",
    "#ffff33",
    "#a65628",
    "#f781bf",
    "#999999",
]

dark_contrast = [
    "#0b3c5d",
    "#b82601",
    "#1c6e8c",
    "#2f4858",
    "#6a994e",
    "#bc4749",
    "#3a0ca3",
    "#4361ee",
]

soft_contrast = [
    "#a6cee3",
    "#fdbf6f",
    "#b2df8a",
    "#fb9a99",
    "#cab2d6",
    "#ffff99",
    "#1f78b4",
    "#33a02c",
]

grayscale_safe = ["#000000", "#444444", "#888888", "#bbbbbb"]

linestyles = ["-", "--", "-.", ":"]
markers = [
    ".",
    ",",
    "o",
    "v",
    "^",
    "<",
    ">",
    "1",
    "2",
    "3",
    "4",
    "8",
    "s",
    "p",
    "P",
    "*",
    "h",
    "H",
    "+",
    "x",
    "X",
    "D",
    "d",
    "|",
    "_",
]


def axion_lineshape(v_0, v_lab, nu_a, nu, case="non-grad", alpha=0.0):
    """
    Calculate analytical lineshapes.

    Parameters
    ----------

    Return
    ------
    A float array of the axion lineshape

    Reference
    ---------
    A. Gramolin: https://github.com/gramolin/lineshape

    """
    c = 299792458.0  # Speed of light (in m/s)
    v_0, v_lab = np.abs(v_0), np.abs(v_lab)

    shift = 0  # max(1 - np.amin(nu), 1 + np.abs(nu_a))
    nu_a += shift
    nu += shift

    full_lineshape = np.zeros(len(nu))

    # Find the index of the first non-zero element
    positive_indices = np.where(nu > nu_a)[0]
    if positive_indices.size > 0:
        nu_a_index = positive_indices[0]
    else:
        return full_lineshape

    freq = nu[nu_a_index:-1]

    assert case in [
        "non-grad",
        "grad_par",
        "grad_perp",
    ], "Case should be 'non-grad', 'grad_par', or 'grad_perp'!"

    beta = 2 * c * v_lab * np.sqrt(2 * (freq - nu_a) / nu_a) / v_0**2  # Eq. (13)
    # *np.sqrt(2 * (nu - nu_a) / nu_a)
    # for arr in [beta]:
    #     print('beta check')
    #     has_nan = np.isnan(arr).any()  # Check for NaN
    #     has_inf = np.isinf(arr).any()  # Check for Inf

    #     print(f"Contains NaN: {has_nan}")  # Output: True
    #     print(f"Contains Inf: {has_inf}")  # Output: True
    if case == "non-grad":  # Non-gradient case, Eq. (12)
        ax_sq_lineshape = (
            2
            * c**2
            * np.exp(-((0.5 * beta * v_0 / v_lab) ** 2) - (v_lab / v_0) ** 2)
            * np.sinh(beta)
            / (np.sqrt(np.pi) * v_0 * v_lab * nu_a)
        )

    elif case == "grad_par":  # Parallel gradient case, Eq. (19)
        factor = (
            np.cos(alpha) ** 2
            - (1 / np.tanh(beta) - 1.0 / beta) * (2 - 3 * np.sin(alpha) ** 2) / beta
        )
        ax_sq_lineshape = (
            (4 * c**2 / (v_0**2 + 2 * (v_lab * np.cos(alpha)) ** 2))
            * (freq / nu_a - 1)
            * factor
            * axion_lineshape(v_0, v_lab, nu_a, nu)
        )
    elif case == "grad_perp":  # Perpendicular gradient case, Eq. (20)
        factor = (
            np.sin(alpha) ** 2
            + (1.0 / np.tanh(beta) - 1.0 / beta)
            * (2.0 - 3.0 * np.sin(alpha) ** 2)
            / beta
        )
        ax_sq_lineshape = (
            (2 * c**2 / (v_0**2 + (v_lab * np.sin(alpha)) ** 2))
            * (freq / nu_a - 1)
            * factor
            * axion_lineshape(v_0, v_lab, nu_a, nu)[nu_a_index:-1]
        )
    else:  # adding this to try and get rid of an error message
        return np.zeros(nunit.shape)

    full_lineshape[nu_a_index:-1] += ax_sq_lineshape
    # nu_a -= shift
    nu -= shift
    return full_lineshape


def candidate_table_text_to_dicts(table_text: str) -> list[dict[str, object]]:
    """Parse a LaTeX-like candidate table into structured dictionaries.

    Expected input rows look like:

        1 & 27, 5 & 1348668.58 & 5.57764506\\

    The returned dictionaries use this schema:

        {
            "Index": int,
            "Step indices": list[int],
            "Frequency": Quantity in Hz,
            "Mass": Quantity in neV / c^2,
        }
    """
    rows = []
    for raw_line in table_text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("\\hline"):
            continue
        if "&" not in line:
            continue

        line = line.rstrip("\\\\").strip()
        parts = [part.strip() for part in line.split("&")]
        if len(parts) != 4:
            continue
        if not parts[0].isdigit():
            continue

        step_indices = [
            int(step.strip()) for step in parts[1].split(",") if step.strip()
        ]
        step_indices.sort()
        rows.append(
            {
                "Index": int(parts[0]),
                "Step indices": step_indices,
                "Frequency": unit.Quantity(float(parts[2]), unit.Hz),
                "Mass": (
                    unit.Quantity(float(parts[3]), unit.neV / const.c**2)
                    if parts[3] is not None and parts[3].strip()
                    else None
                ),
            }
        )
    return rows


def candidate_dicts_to_table_rows(
    items: list[dict[str, object]],
    frequency_format: str = ".2f",
    mass_format: str = ".8f",
) -> list[str]:
    """Serialize candidate dictionaries back into LaTeX table rows."""
    rows = []
    for item in items:
        step_indices = ", ".join(str(step) for step in sorted(item["Step indices"]))
        frequency = unit.Quantity(item["Frequency"], unit.Hz).to_value(unit.Hz)
        mass = item.get("Mass")
        mass_text = ""
        if mass is not None:
            mass = unit.Quantity(mass, unit.neV / const.c**2).to_value(
                unit.neV / const.c**2
            )
            mass_text = format(mass, mass_format)
        rows.append(
            f'{item["Index"]} & {step_indices} & {format(frequency, frequency_format)} & {mass_text}\\\\'
        )
    return rows


def candidate_dicts_fill_mass(
    items: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Fill the Mass field from Frequency when Mass is missing or None."""
    filled = []
    for item in items:
        new_item = dict(item)
        if new_item.get("Mass") is None:
            frequency = unit.Quantity(new_item["Frequency"], unit.Hz)
            new_item["Mass"] = (const.h * frequency / const.c**2).to(
                unit.neV / const.c**2
            )
        filled.append(new_item)
    return filled
