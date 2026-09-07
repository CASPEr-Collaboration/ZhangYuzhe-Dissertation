import inspect  # for check()
import re  # for check()
from src.dependency import *
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d


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
    # ",",
    "<",
    "1",
    "p",
    "*",
    "h",
    "+",
    "x",
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
        return np.zeros(nu.shape)

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


def Lorentzian(x, center, FWHM, area: float = 1.0, offset: float = 0.0):
    """
    Return the value of the Lorentzian function
        offset + 0.5*FWHM*area / (np.pi * ( (x-center)**2 + (0.5*FWHM)**2 )      )

                           FWHM A
        offset + ───────────────────────
                  2π ((x-c)^2+(FWHM/2)^2 )

    Parameters
    ----------

    x : scalar or array_like
        argument of the Lorentzian function
    center : scalar
        the position of the Lorentzian peak
    FWHM : scalar
        full width of half maximum (FWHM) / linewidth of the Lorentzian peak
    area : scalar
        area under the Lorentzian curve (without taking offset into consideration)
    offset : scalar
        offset for the curve


    Returns
    -------
    the value of the Lorentzian function : ndarray or scalar

    Examples
    --------
    >>>

    Reference
    ----------
    Null

    """
    return offset + 0.5 * abs(FWHM) * area / (
        np.pi * ((x - center) ** 2 + (0.5 * FWHM) ** 2)
    )


class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.get_proj())
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        FancyArrowPatch.draw(self, renderer)

    def do_3d_projection(self, renderer=None):  #
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.get_proj())
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        return np.min(zs)


def Init_3020sphere(ax, verbose=False):
    plt.gca().invert_yaxis()
    ax.grid(False)
    ax.xaxis.set_pane_color((1, 1, 1, 0.0))
    ax.yaxis.set_pane_color((1, 1, 1, 0.0))
    ax.zaxis.set_pane_color((1, 1, 1, 0.0))
    # draw the cooridnate frame
    a = Arrow3D(
        [0, 2],
        [0, 0],
        [0, 0],
        mutation_scale=10,
        lw=1,
        arrowstyle="->",
        color="k",
        shrinkA=0,
        shrinkB=0,
    )
    ax.add_artist(a)
    a = Arrow3D(
        [0, 0],
        [0, 1.4],
        [0, 0],
        mutation_scale=10,
        lw=1,
        arrowstyle="->",
        color="k",
        shrinkA=0,
        shrinkB=0,
    )
    ax.add_artist(a)
    a = Arrow3D(
        [0, 0],
        [0, 0],
        [0, 1.3],
        mutation_scale=10,
        lw=1,
        arrowstyle="->",
        color="k",
        shrinkA=0,
        shrinkB=0,
    )
    ax.add_artist(a)

    ax.text(0.8, 1.55, 0, "y", color="black")
    ax.text(2.4, 0.35, 0, "x", color="black")
    ax.text(0, 0.05, 1.25, "z", color="black")
    # draw the sphere
    r = 1
    u, v = np.mgrid[0 : 2 * np.pi : 40j, 0 : np.pi : 20j]
    x = np.cos(u) * np.sin(v)
    y = np.sin(u) * np.sin(v)
    z = np.cos(v)
    ax.plot_surface(x, y, z, cmap=plt.cm.YlGnBu_r, alpha=0.2)
    # draw B0
    a = Arrow3D(
        [0, 0],
        [-0.95, -0.95],
        [0.75, 1.25],
        mutation_scale=10,
        lw=1.6,
        arrowstyle="->",
        color="k",
        shrinkA=0,
        shrinkB=0,
    )
    ax.add_artist(a)
    ax.text(0, -0.85, 1.15, "$\mathbf{B}_0$", color="black")
    # ax.text(1, 0.85, 1.25, '$\mathbf{M}$', color='g')

    # draw magnetization vectors
    # timestamp = np.linspace(start=0, stop=1, num=1000)
    # magz = np.cos(2*np.pi*nu/10*timestamp)
    # magx = np.sqrt(1 - magz**2) * np.cos(2*np.pi*nu*1*timestamp)
    # magy = np.sqrt(1 - magz**2) * np.sin(2*np.pi*nu*1*timestamp)
    # ax.quiver(
    #         0, 0, 0, # <-- starting point of vector
    #         1, 1, 1, # <-- directions of vector
    #         color = 'g', alpha = 1, lw = 1.6, length=1, normalize=False,
    #         arrow_length_ratio=.25, label='$\\vec{M}$'
    #     )
    try:
        ax.set_aspect("equal")
    except NotImplementedError:
        pass
    ax.set_xlim3d([-0.8, 0.99])
    ax.set_ylim3d([-0.8, 0.99])
    ax.set_zlim3d([-0.8, 0.99])
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.axis("off")
    # ax.legend(loc='upper right')
    ax.set_box_aspect((1, 1, 1))


def Init_0090sphere(ax, verbose=False):
    plt.gca().invert_yaxis()
    ax.grid(False)
    ax.xaxis.set_pane_color((1, 1, 1, 0.0))
    ax.yaxis.set_pane_color((1, 1, 1, 0.0))
    ax.zaxis.set_pane_color((1, 1, 1, 0.0))
    # draw the cooridnates
    # draw the cooridnate frame
    a = Arrow3D(
        [-1, 1.2],
        [0, 0],
        [0, 0],
        mutation_scale=10,
        lw=1,
        arrowstyle="->",
        color="k",
        shrinkA=0,
        shrinkB=0,
    )
    ax.add_artist(a)
    a = Arrow3D(
        [0, 0],
        [-1, 1.2],
        [0, 0],
        mutation_scale=10,
        lw=1,
        arrowstyle="->",
        color="k",
        shrinkA=0,
        shrinkB=0,
    )
    ax.add_artist(a)
    # a = Arrow3D([0,0],[0,0],[0,1.3], mutation_scale=10, lw=1, arrowstyle="->", color="k", shrinkA=0, shrinkB=0)
    # ax.add_artist(a)
    ax.text(1.2, 0.15, 0, "x", color="black")
    ax.text(0.15, 1.2, 0, "y", color="black")

    # ax.text(0, 0.05, 1.25, 'z', color='black')
    # draw the sphere
    r = 1
    u, v = np.mgrid[0 : 2 * np.pi : 40j, 0 : np.pi : 20j]
    x = np.cos(u) * np.sin(v)
    y = np.sin(u) * np.sin(v)
    z = np.cos(v)
    ax.plot_surface(x, y, z, cmap=plt.cm.YlGnBu_r, alpha=0.2)
    try:
        ax.set_aspect("equal")
    except NotImplementedError:
        pass
    ax.set_xlim3d([-0.8, 0.99])
    ax.set_ylim3d([-0.8, 0.99])
    ax.set_zlim3d([-0.8, 0.99])
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.axis("off")
    # ax.legend(loc='upper right')
    ax.set_box_aspect((1, 1, 1))


def Add_vector(
    ax,
    start=None,
    end=None,
    mutation_scale=10,
    lw=1.6,
    color="k",
    alpha=1,
    zorder=5,
    linestyle="-",
    verbose=False,
):
    a = Arrow3D(
        [start[0], end[0]],
        [start[1], end[1]],
        [start[2], end[2]],
        mutation_scale=mutation_scale,
        lw=lw,
        arrowstyle="->",
        color=color,
        alpha=alpha,
        shrinkA=0,
        shrinkB=0,
        zorder=zorder,
        linestyle=linestyle,
    )
    ax.add_artist(a)

    # ax.quiver(
    #         start[0], start[1], start[2], # <-- starting point of vector
    #         end[0], end[1], end[2], # <-- directions of vector
    #         color = 'g', alpha = 1, lw = linewidth, length=1, normalize=False,
    #         arrow_length_ratio=.25, label=''
    #     )


def sph2orth1d(vec=None):
    orth = np.zeros(3)
    orth[0] = vec[0] * np.sin(vec[1]) * np.cos(vec[2])
    orth[1] = vec[0] * np.sin(vec[1]) * np.sin(vec[2])
    orth[2] = vec[0] * np.cos(vec[1])
    return orth


def get_FWHMin(x, y):
    """
    Calculate the Full Width at Half Maximum (FWHM) of a dip.

    Parameters:
        x (array-like): The x-values of the curve.
        y (array-like): The y-values of the curve.

    Returns:
        float: The FWHM of the curve.
    """
    # Ensure inputs are numpy arrays
    x = np.array(x)
    y = np.array(y)

    # Find the maximum value of y and its half-maximum
    y_min = np.amin(y)
    Twice_min = y_min * 2.0

    # Find indices where y crosses the half-maximum
    # check(np.where(y <= Twice_min))
    indices = np.where(y <= Twice_min)[0]
    if len(indices) < 2:
        raise ValueError(
            "Cannot calculate FWHM: The curve does not have two points crossing the half-maximum."
        )

    # Extract the first and last indices crossing the half-maximum
    left_index = indices[0]
    right_index = indices[-1]

    # # Interpolate to find more precise crossing points
    # x_left = np.interp(Twice_min, [y[left_index - 1], y[left_index]], [x[left_index - 1], x[left_index]])
    # x_right = np.interp(Twice_min, [y[right_index], y[right_index + 1]], [x[right_index], x[right_index + 1]])
    x_left = x[left_index]
    x_right = x[right_index]

    # Calculate FWHM
    FWHMin = abs(x_right - x_left)

    return FWHMin


class Exclusion:
    def __init__(
        self,
        name="blank",
        nu_start=None,
        nu_end=None,
        fraction=1 / 1000.0,
        frequencies=None,
        discovery_threshold=5,
        detuning_correction=1.0,
        gr=1.0,
        gDM=120.0,  # GeV.Hz
        Q=10**6,
        sigma=1e-12,  # reference noise level [Phi0^2/Hz]
        Phipito2=1e-8,  # reference SQUID flux [Phi0/sqrt(Hz)]
        T=1e-20,  # initial measurement time approx 0
    ):
        """
        Initialize the (class) LIAsignal object

        Parameters
        ----------
        name: str
            name of the Exclusion.

        frequencies : np.array
            measurement range

        """
        self.name = name

        if (nu_start is not None) and (nu_end is not None) and (fraction is not None):
            # Nnu = int(np.log(nu_end / nu_start) / np.log(1 + fraction))
            Nnu = int(1 / fraction)
            DeltaNu = abs(nu_end - nu_start) * fraction
            self.frequencies = nu_start + DeltaNu * np.arange(Nnu)
        elif frequencies is not None:
            self.frequencies = np.sort(frequencies)

        self.discovery_threshold = discovery_threshold
        self.detuning_correction = detuning_correction
        self.gr = gr
        self.gDM = gDM
        self.Q = Q
        self.sigma = sigma
        self.Phipito2 = Phipito2
        self.T = T
        self.Teff_arr = T * np.ones(shape=self.frequencies.shape)
        self.SNR = 1e-20 * np.ones(shape=self.frequencies.shape)
        self.sensi = np.sqrt(self.SNR)
        self.gaNNexc = 1.0 / self.sensi
        del (
            frequencies,
            discovery_threshold,
            detuning_correction,
            gr,
            gDM,
            Q,
            sigma,
            Phipito2,
            T,
        )

    def UpdateExc(
        self,
        freq_arr=None,
        PSD=None,
        T2star=None,
        acqDelay=None,
        acqTime=None,
        measurementT=None,
        sigma=None,
        verbose=False,
    ):

        if (
            (freq_arr is None)
            or (PSD is None)
            or (measurementT is None)
            or (sigma is None)
        ):
            if verbose:
                print("Updating gaNNexc without new spectrum")
            self.gaNNexc = (
                np.sqrt(self.discovery_threshold * self.sigma)
                * self.Teff_arr ** (-0.25)
                * (self.Q / self.frequencies) ** (-1.25)
                * (0.5 * self.gr * self.gDM * self.Phipito2) ** (-1)
            )
            return 0

        if T2star is None or acqDelay is None or acqTime is None:
            raise ValueError("Input T2star / acqDelay / acqTime is None. ")

        PSDcorrection_val = (
            T2star
            / (4 * acqTime)
            * (1 - np.exp(-2 * acqTime / T2star))
            * np.exp(-2 * acqDelay / T2star)
        ) ** (-1.0)
        PSD_corrected = PSDcorrection_val * PSD

        nustart = np.amin(freq_arr)
        nustop = np.amax(freq_arr)

        if nustart < self.frequencies[0]:
            istart = 0
        elif nustart > self.frequencies[-1]:
            raise ValueError("nustart > self.frequencies[-1]")
        else:
            argminindex_start = np.argmin(abs(self.frequencies - nustart))
            if self.frequencies[argminindex_start] >= nustart:
                istart = argminindex_start
            else:
                istart = argminindex_start + 1

        if nustop > self.frequencies[-1]:
            istop = len(self.frequencies) - 1
        elif nustop < self.frequencies[0]:
            check(nustop)
            check(self.frequencies[0])
            raise ValueError("nustop < self.frequencies[0]")
        else:
            argminindex_stop = np.argmin(abs(self.frequencies - nustop))
            if self.frequencies[argminindex_stop] <= nustop:
                istop = argminindex_stop
            else:
                istop = argminindex_stop - 1
        # yinterp = np.interp(xvals, x, y)
        PSDinterp = np.interp(
            self.frequencies[istart : istop + 1], freq_arr, PSD_corrected
        )

        # self.Teff_arr
        Phipito2_new = np.sqrt(
            PSDinterp * 2
        )  #  abs(self.frequencies[istart:istop+1] * 2. / self.Q)
        # check(np.mean(Phipito2_new))

        self.Teff_arr[istart : istop + 1] += (
            measurementT
            * (np.sqrt(sigma) / Phipito2_new) ** (-4.0)
            / (np.sqrt(self.sigma) / self.Phipito2) ** (-4.0)
        )

        self.gaNNexc = (
            np.sqrt(self.discovery_threshold * self.sigma)
            * self.Teff_arr ** (-0.25)
            * (self.Q / self.frequencies / 2) ** (-1.25)
            * (0.5 * self.gr * self.gDM * self.Phipito2) ** (-1)
        )

    def updateExc_SNR(
        self,
        freq_arr=None,
        SNR=None,
        verbose=False,
    ):
        nustart = np.amin(freq_arr)
        nustop = np.amax(freq_arr)

        if nustart < self.frequencies[0]:
            istart = 0
        elif nustart > self.frequencies[-1]:
            raise ValueError("nustart > self.frequencies[-1]")
        else:
            argminindex_start = np.argmin(abs(self.frequencies - nustart))
            if self.frequencies[argminindex_start] >= nustart:
                istart = argminindex_start
            else:
                istart = argminindex_start + 1

        if nustop > self.frequencies[-1]:
            istop = len(self.frequencies) - 1
        elif nustop < self.frequencies[0]:
            check(nustop)
            check(self.frequencies[0])
            raise ValueError("nustop < self.frequencies[0]")
        else:
            argminindex_stop = np.argmin(abs(self.frequencies - nustop))
            if self.frequencies[argminindex_stop] <= nustop:
                istop = argminindex_stop
            else:
                istop = argminindex_stop - 1
        # yinterp = np.interp(xvals, x, y)
        SNRinterp = np.interp(self.frequencies[istart : istop + 1], freq_arr, SNR)

        self.SNR[istart : istop + 1] = (
            (self.SNR[istart : istop + 1]) ** (2) + SNRinterp ** (2)
        ) ** (0.5)
        self.sensi = np.sqrt(self.SNR)
        self.gaNNexc = 1.0 / self.sensi
        # self.gaNNexc = np.sqrt(self.discovery_threshold * self.sigma) * \
        #     self.Teff_arr ** (-0.25) * (self.Q / self.frequencies / 2) ** (-1.25) * \
        #         (0.5 * self.gr * self.gDM * self.Phipito2) ** (-1)

    def PlotExc(self, verbose=False):
        self.UpdateExc(verbose=verbose)
        hbar = 6.582119569e-16  # eV.s
        c = 299792458  # m/s
        # plt.rc("font", size=12)
        # plt.rcParams["font.family"] = "Times New Roman"
        # # plt.rcParams["font.family"] = "serif"
        # # plt.rcParams["font.serif"] = ["Times New Roman"]
        # plt.rcParams["mathtext.fontset"] = "cm"  # 'dejavuserif'

        fig = plt.figure(figsize=(8, 6), dpi=150)  #
        gs = gridspec.GridSpec(nrows=1, ncols=1)  #
        # fig.subplots_adjust(left=left_spc, top=top_spc, right=right_spc,
        #                     bottom=bottom_spc, wspace=xgrid_spc, hspace=ygrid_spc)
        ax = fig.add_subplot(gs[0, 0])
        # ax.plot(GammaandSAmp_arr[:, 0], GammaandSAmp_arr, label='PSD Signal Amp', color='tab:cyan', alpha=1)
        ax.plot(
            hbar / c**2 * self.frequencies,
            self.gaNNexc,
            label="",
            color=[0 / 256.0, 88 / 256.0, 155 / 256.0],
            alpha=1,
        )  # 0, 88, 155
        # \definecolor{JGUred}{RGB}{193, 0, 42} [/256., /256., /256.]
        # \definecolor{JGUgrey}{RGB}{99, 99, 99}
        # \definecolor{HIMblue}{RGB}{0, 88, 155}
        # ax.scatter(GammaandSAmp_arr, GammaandSAmp_arr, marker='x', s=30, color='tab:blue', alpha=1)

        # ax.plot(GammaandSAmp_arr, GammaandSAmp_arr, label='SNR', alpha=1)
        # ax.step(, , where='post', label='', alpha=1)
        ax.set_ylabel("$\\mathrm{g_{aNN}} / \\mathrm{GeV^{-1}}$")
        ax.set_xlabel("ALP mass / $\\mathrm{eV}$")
        # ax.set_title('PSD Signal Amplitude')
        # ax.set_xscale('log')
        ax.set_yscale("log")
        # ax.set_xticks([])
        # ax.set_yticks([])
        # ax.set_xlim(-10, 10)
        # ax.set_ylim(-0.05, 1.1)
        # ax.text(x=-10, y=1,s='(a)')
        # ax.vlines(x=taua, ymin = 1e-5, ymax = 1e3, colors='grey', linestyles='dotted', label='')
        # ax.hlines(y=1 / ((np.pi * homog0 * 1e6) + 1 / T2), xmin = 1e2, xmax = 1e6, colors='black', linestyles='dotted', label='')
        # ax.yaxis.set_major_locator(plt.NullLocator())
        # ax.xaxis.set_major_formatter(plt.NullFormatter())
        # for tick in ax.xaxis.get_major_ticks():
        #         tick.tick1line.set_visible(False)
        #         tick.tick2line.set_visible(False)
        #         tick.label1.set_visible(False)
        #         tick.label2.set_visible(False)
        ax.grid()
        plt.tight_layout()
        plt.show()
        return self.frequencies, self.gaNNexc

    def PlotExc_1PSD(
        self,
        freqoffset=0,
        PSDfreq_range=[-80, 80],
        specxaxis=None,
        spectrum=None,
        specxunit=None,
        specyunit=None,
        massfactor=1e31,
        ax_yticks=None,
        verbose=False,
    ):

        hbar = 6.582119569e-16  # eV.s
        # c = 299792458  # m/s
        # hbar = 1
        c = 1

        self.UpdateExc(verbose=verbose)

        # plt.rc("font", size=12)
        # plt.rcParams["font.family"] = "Times New Roman"
        # # plt.rcParams["font.family"] = "serif"
        # # plt.rcParams["font.serif"] = ["Times New Roman"]
        # plt.rcParams["mathtext.fontset"] = "cm"  # 'dejavuserif'
        fig = plt.figure(figsize=(8 * 0.8, 6 * 0.8), dpi=150)  #
        if (
            PSDfreq_range is None
            or specxaxis is None
            or spectrum is None
            or specxunit is None
            or specyunit is None
        ):
            raise ValueError(
                "PSDfreq_range is None specxaxis is None or spectrum is None or specxunit is None or specyunit is None"
            )
        else:
            gs = gridspec.GridSpec(nrows=2, ncols=1)  #
            PSD_ax = fig.add_subplot(gs[0, 0])
            ax = fig.add_subplot(gs[1, 0])
        # fig.subplots_adjust(left=left_spc, top=top_spc, right=right_spc,
        #                     bottom=bottom_spc, wspace=xgrid_spc, hspace=ygrid_spc)
        PSD_ax.plot(
            specxaxis - freqoffset,
            spectrum,
            label="PSD ",
            color=[0 / 256.0, 88 / 256.0, 155 / 256.0],
            alpha=1,
        )
        PSD_ax.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
        PSD_ax.xaxis.set_label_position("top")
        if freqoffset == 0:
            PSD_ax.set_xlabel(f"Frequency / " + specxunit)  # $\\mathrm{Hz}$
        else:
            PSD_ax.set_xlabel(
                f"Frequency - {freqoffset:.0f} / " + specxunit
            )  # $\\mathrm{Hz}$
        PSD_ax.set_ylabel("PSD / " + specyunit)  # $\Phi_{0}^{2}/\\mathrm{Hz}$
        PSD_ax.grid()
        PSD_ax.set_xlim(PSDfreq_range[0], PSDfreq_range[1])
        # PSD_ax.set_ylim(top=3.2, bottom=-0.1)
        freq_start, freq_stop = PSD_ax.get_xlim()
        PSDxticks = PSD_ax.get_xticks()

        ax.plot(
            2 * np.pi * hbar / c**2 * massfactor * (self.frequencies - freqoffset),
            self.gaNNexc,
            label="gaNN",
            color=np.array([193, 0, 42]) / 256.0,
            alpha=1,
        )  # 0, 88, 155
        # ax.scatter(GammaandSAmp_arr, GammaandSAmp_arr, marker='x', s=30, color='tab:blue', alpha=1)
        ax.set_xlabel(
            f"ALP mass - {hbar / c ** 2 * freqoffset * massfactor:.0f}"
            + " / $10^{-%.0f}\\mathrm{eV} c^{-2}$" % (np.log10(massfactor))
        )
        ax.set_ylabel("$\\mathrm{g_{aNN}}$" + " / " + "$\\mathrm{GeV^{-1}}$")
        # ax.set_title('PSD Signal Amplitude')
        # ax.set_xscale('log')
        ax.set_yscale("log")
        ax.set_xticks(2 * np.pi * hbar / c**2 * massfactor * PSDxticks)
        ax.xaxis.set_major_formatter("{x:.2f}")
        # ax.set_yticks([])
        ax.set_xlim(
            2 * np.pi * hbar / c**2 * massfactor * (freq_start),
            2 * np.pi * hbar / c**2 * massfactor * (freq_stop),
        )
        ax.set_ylim(top=10 ** (-1.8), bottom=10 ** (-6.2))
        if ax_yticks is not None:
            ax.set_yticks(ax_yticks)
        ax.fill_between(
            2 * np.pi * hbar / c**2 * massfactor * (self.frequencies - freqoffset),
            self.gaNNexc,
            1e5,
            color="r",
            alpha=0.2,
        )

        ax.grid()
        letters = [
            "(a)     ",
            "(b)     ",
            "(c)",
            " (d)",
            " (e)",
            " (f)",
            " (g)",
            " (h)",
            " (i)",
        ]
        for i, axi in enumerate([PSD_ax]):
            xleft, xright = axi.get_xlim()
            ybottom, ytop = axi.get_ylim()
            axi.text(
                x=xleft,
                y=ytop,
                s=letters[i],
                ha="right",
                va="center",
                color="blue",
                fontsize=14,
            )
        for i, axi in enumerate([ax]):
            xleft, xright = axi.get_xlim()
            ybottom, ytop = axi.get_ylim()
            axi.text(
                x=xleft,
                y=ytop,
                s=letters[i + 1],
                ha="right",
                va="top",
                color="blue",
                fontsize=14,
            )
        plt.tight_layout()
        plt.show()
        return self.frequencies, self.gaNNexc
