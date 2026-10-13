"""Combine the eigenstate spectrum and radial wavefunctions in a 1 x 2 figure.

Preserve each source example's frequency, grid, and state selection. Set
USE_MARKERS to True to add sparse markers from axionbloch.utils to the curves.
Run from the repository root with the axionbloch environment activated::

    python -m examples.EarthBoundAxionHalo.state-amplitude-and-radial-wavefunctions
"""

"""Plot eigenstate amplitudes against their eigenenergy shifts.

All states from 1s through 4f are included with equal input coefficients.
``plotStateAmplitudeVsEigenEnergy`` normalizes the coefficients before plotting,
so every displayed amplitude is 1 / sqrt(number of states).
"""

# from pathlib import Path
from src.dependency import *

from axionbloch.EarthBoundAxionHalo import EarthBoundAxionHalo
from src.utils import linestyles, markers

# # from pathlib import Path
# from axionbloch.dependency import unit, plt, gridspec, np, const

# from axionbloch.EarthBoundAxionHalo import EarthBoundAxionHalo
# from src.utils import linestyles, markers

halo = EarthBoundAxionHalo(
    # specify axion Compton frequency
    # nu_a=1.348570 * unit.MHz,
    nu_a=1.0 * unit.MHz,
    # you can use a fixed axion mass instead of nu_a, e.g.
    # m_a=10**(-11.5) * unit.eV / const.c**2,
    # number of grid points for the radial solver
    N=2**14,
    # radial extent of the solver grid
    extent=2**8 * unit.R_earth,
    verbose=True,
)

if halo.nu_a == 1.348570 * unit.MHz:
    r_lims = (-0.2 * unit.R_earth, 5.2 * unit.R_earth)
    mass_limits = (-5.5, 0.16)
elif halo.nu_a == 1.0 * unit.MHz:
    r_lims = (-0.2 * unit.R_earth, 10.2 * unit.R_earth)
    mass_limits = (-4.2, 0.2) * unit.attoelectronvolt / const.c**2

halo.solve_TISE_3D(
    l_vals=[0, 1, 2, 3],
    # l_vals=[0],
    max_n_r=20,
    verbose=False,
)


state_names = [
    "1s",
    "2s",
    "3s",
    "2p",
    "4s",
    "3d",
    "5s",
]


# # Solve enough radial states
# halo.solve_TISE_3D(
#     l_vals=[0],
#     max_n_r=20,
#     verbose=False,
# )
# # Plot the radial wavefunctions
# state_names = ["1s", "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s", "10s"]

text_heights = [
    1,
    1,
    1,
    1,
    1,
    1.2,
    1,
    # 1.5,
    # 1,
    # 1.5
]  #

colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]

fig = plt.figure(figsize=(13 / 2.54, 5.0 / 2.54), dpi=300)  # initialize a figure

gs = gridspec.GridSpec(nrows=1, ncols=2)
# gs = gridspec.GridSpec(nrows=2, ncols=1)
# fix the margins
left = 0.063
bottom = 0.23
right = 0.977
top = 0.79
wspace = 0.294
hspace = 0.2
fig.subplots_adjust(
    left=left, top=top, right=right, bottom=bottom, wspace=wspace, hspace=hspace
)

state_ax = fig.add_subplot(gs[0, 0])
WF_ax = fig.add_subplot(gs[0, 1])

# state_ax = fig.add_subplot(gs[0, 0])
# WF_ax = fig.add_subplot(gs[1, 0])

# fig, _, _, _ = halo.plotStateAmplitudeVsEigenEnergy(
#     stateCoefficients=stateCoefficients,
#     energy_unit=unit.attoelectronvolt,
#     frequency_unit=unit.mHz,
#     ax=state_ax,
#     showPlot=False,
# )

energy_unit = unit.attoelectronvolt
frequency_unit = unit.mHz

for idx, name in enumerate(state_names):
    state = halo.states[name]
    state_ax.vlines(
        state["eigenE"].to_value(energy_unit),
        ymin=0,
        # ymax=text_heights[idx],
        ymax=1.0,
        color=colors[idx % len(colors)],
        # linewidth=1.5,
    )
    state_ax.scatter(
        state["eigenE"].to_value(energy_unit),
        # text_heights[idx],
        1,
        color=colors[idx % len(colors)],
        marker=markers[idx],
        s=10,
    )
    # for index, (energy, amplitude, state_name) in enumerate(
    #     zip(
    #         energy_values,
    #         amplitudes,
    #         spectrum["state_names"],
    #     )
    # ):
    state_ax.annotate(
        state["name"],
        xy=(state["eigenE"].to_value(energy_unit), text_heights[idx]),
        xytext=(0, 4),
        textcoords="offset points",
        ha="center",
        va="bottom",
    )

# The upper x axis represents the same E_n values as frequency shifts.
# twiny() is used because this is a second horizontal scale, not a
# second dependent variable.


start_idx = 0

for idx, name in enumerate(state_names):
    state = halo.states[name]
    WF_ax.plot(
        halo.r[start_idx:].to_value(unit.R_earth),
        state["u_r"][start_idx:].real,
        label=name,
        color=colors[idx % len(colors)],
        # linestyle=linestyles[idx % len(linestyles)],
        linestyle="-",
        # linewidth=0.5,
        # markerfacecolor=colors[idx % len(colors)],
        marker=markers[idx],
        markevery=0.1,
        markersize=2,
        # markeredgewidth=.5,
    )
    # WF_ax.plot(
    #     halo.r[start_idx:].to_value(unit.R_earth),
    #     state["u_r"][start_idx:].real,
    #     label=name,
    #     color=colors[idx % len(colors)],
    #     # linestyle=linestyles[idx % len(linestyles)],
    #     linestyle="none",
    #     # linewidth=1.4,
    #     # markerfacecolor=colors[idx % len(colors)],
    #     marker=markers[idx],
    #     markevery=0.01,
    #     markersize=0.5,
    # )

energy_unit_label = energy_unit.to_string("latex_inline")[1:-1]
# state_ax.set_xlim(-0.05 * np.amax(energy_values), 1.05 * np.max(energy_values))
state_ax.set_xlabel("$m-m_a\\,$" + f"$\\left({energy_unit_label}/c^2\\right)$")
# Leave vertical room for the staggered state labels.

# for 1.348 MHz
# state_ax.set_xlim(-5.5, 0.16)
# for 1 MHz
state_ax.set_xlim(mass_limits.to_value(energy_unit / const.c**2))

state_ax.set_ylim(0, np.amax(text_heights) + 0.5)
state_ax.set_ylabel("")
state_ax.set_yticklabels([])
state_ax.set_yticks([])
# state_ax.set_xscale("log")

frequency_ax = state_ax.twiny()
state_limits = np.asarray(state_ax.get_xlim()) * energy_unit
freq_limits = (state_limits / const.h).to_value(frequency_unit)
frequency_ax.set_xlim(freq_limits)
frequency_unit_label = frequency_unit.to_string("latex_inline")[1:-1]
frequency_unit_label = "\\mathrm{mHz}"
frequency_ax.set_xlabel("$\\nu-\\nu_a\\,$" + f"$({frequency_unit_label})$")

WF_ax.set_xlabel("$r\\,(R_\\oplus$)")
WF_ax.set_ylabel("$r\\,R(r)\\,(R_\\oplus^{-1/2})$")
# WF_ax.legend(ncol=2, bbox_to_anchor=(1.0, 1.0))

WF_ax.set_xlim(r_lims[0].to_value(unit.R_earth), r_lims[1].to_value(unit.R_earth))

# Show the wavefunction radius in kilometres on its upper x-axis.
wavefunction_km_ax = WF_ax.twiny()
wavefunction_x_min, wavefunction_x_max = WF_ax.get_xlim()
wavefunction_km_ax.set_xlim(
    (wavefunction_x_min * unit.R_earth).to_value(unit.km),
    (wavefunction_x_max * unit.R_earth).to_value(unit.km),
)
wavefunction_km_ax.set_xlabel("$\\mathrm{Radius}\\, (\\mathrm{km})$")

# put figure index
letters = ["(a)", "(b)", "(c)", "(d)", "(e)", "(f)", "(g)", "(h)", "(i)"]
for i, ax in enumerate([state_ax, WF_ax]):
    # xleft, xright = ax.get_xlim()
    # ybottom, ytop = ax.get_ylim()
    ax.text(
        -0.07,
        1.02,
        s=letters[i],
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        color="k",
    )
# ha = 'left' or 'right'
# va = 'top' or 'bottom'

# fig.savefig(output_path, facecolor="white", transparent=False)
fig.savefig(
    "tex/figures/EH_ALP-state_amplitude-and-radial_wavefunctions-7states.pdf",
    # dpi=300,
    # bbox_inches="tight",
)
fig.savefig(
    "tex/figures/EH_ALP-state_amplitude-and-radial_wavefunctions-7states.png",
    # dpi=300,
    # bbox_inches="tight",
)
# fig.tight_layout()
plt.show()
