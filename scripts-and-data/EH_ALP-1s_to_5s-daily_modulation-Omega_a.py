"""Plot daily Omega_a modulation at Mainz.

The column includes the Rabi frequencies Omega_a with the first-order Lorentz boost.
"""

from datetime import datetime
from zoneinfo import ZoneInfo

from src.dependency import *
from src.utils import markers, linestyles
from axionbloch.EarthBoundAxionHalo import EarthBoundAxionHalo
from axionbloch.Station import Mainz

colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]

states_to_check = ["1s", "2s", "3s", "2p", "4s", "3d", "5s"]
state_notations = {
    "1s": r"$|1,\,0,\, 0\rangle$",
    "2s": r"$|2,\,0,\, 0\rangle$",
    "2p": r"$|2,\,1,\, 0\rangle$",
    "3s": r"$|3,\,0,\, 0\rangle$",
    "3p": r"$|3,\,1,\, 0\rangle$",
    "3d": r"$|3,\,2,\, 0\rangle$",
    "4s": r"$|4,\,0,\, 0\rangle$",
    "4p": r"$|4,\,1,\, 0\rangle$",
    "4d": r"$|4,\,2,\, 0\rangle$",
    "4f": r"$|4,\,3,\, 0\rangle$",
    "5s": r"$|5,\,0,\, 0\rangle$",
    "5p": r"$|5,\,1,\, 0\rangle$",
}

# states_to_check = ["1s", "2s", "2p"]
halo = EarthBoundAxionHalo(
    nu_a=1.348500 * unit.MHz,
    N=int(2**12),
    extent=128.0 * unit.R_earth,
    g_aNN=1e-9 * unit.GeV**-1,
    verbose=True,
)

halo.showValueAndUnits()
halo.solve_TISE_3D(
    l_vals=[0, 1, 2],
    max_n_r=64,
    verbose=False,
)

t0 = Time(datetime(2022, 12, 13, 7, 0, tzinfo=ZoneInfo("Europe/Berlin")))
t_hours = np.linspace(0, 72, 216) * unit.hour
meas_times = t0 + t_hours


components = [
    (
        "grad_r",
        "\\partial_r \\psi",
        "\\Omega_a^r / (2\\pi)",
    ),
    (
        "grad_theta",
        "\\frac{1}{r}\\partial_\\theta \\psi",
        "\\Omega_a^\\theta / (2\\pi)",
    ),
    (
        "grad_phi",
        "\\frac{1}{r\\sin\\theta}\\partial_\\varphi\\psi",
        "\\Omega_a^\\phi / (2\\pi)",
    ),
]

Omega_factor = (
    const.c * halo.g_aNN * np.sqrt(halo.N_a * const.hbar**3 * const.c / (2 * halo.m_a))
)

fig, axes = plt.subplots(
    3,
    1,
    figsize=(13.0 / 2.54, 10.8 / 2.54),
    dpi=300,
    sharex="col",
    sharey="col",
)

left = 0.22
bottom = 0.11
right = 0.764
top = 0.95
wspace = 0.428
hspace = 0.123
fig.subplots_adjust(
    left=left, top=top, right=right, bottom=bottom, wspace=wspace, hspace=hspace
)

Omega_axes = axes

for idx, state in enumerate(states_to_check):
    for Omega_ax, component in zip(Omega_axes, components):
        gradient_key, gradient_label, Omega_label = component

        gradient_result_with_boost = halo.findGradientsOverTime(
            stateCoefficients={state: 1.0},
            station=Mainz,
            meas_times=meas_times,
            truncRadius=3 * unit.R_earth,
            include_lorentz_boost=True,
            verbose=True,
        )

        gradient_with_boost = gradient_result_with_boost[gradient_key]
        # convert to mHz
        # using the dimensionless_angles equivalency because polar and azimuthal components have units of 1/rad

        Omega_with_boost = (Omega_factor * np.abs(gradient_with_boost)).to(
            unit.mHz, equivalencies=unit.dimensionless_angles()
        )

        Omega_ax.plot(
            t_hours,
            Omega_with_boost / (2 * np.pi),
            color=colors[idx % len(colors)],
            label=state_notations[state],
            linestyle="-",
            # linewidth=0.5,
            marker=markers[idx],
            markevery=0.1,
            markersize=2,
        )

        Omega_ax.set_ylabel(
            f"${Omega_label}$\n$\\left(\\mathrm{{mHz}}\\right)$",
            color="black",
        )
        Omega_ax.tick_params(axis="y", colors="black")

# Omega_axes[0].set_title("$\\Omega_a$")
# Omega_axes[1].legend(
#     # loc="lower center",
#     bbox_to_anchor=(1.05, 1.05),
#     ncol=1,
#     # frameon=False,
#     # fontsize=7,
# )
Omega_axes[1].legend(
    loc="center left",
    bbox_to_anchor=(1.02, 0.5),
    # frameon=False,
)

# from 2022-12-13 07:00 CET
Omega_axes[-1].set_xlabel("Time (hour)")

for ax in Omega_axes:
    ax.set_ylim(-0.06, 1.06)

# fig.tight_layout()

plt.savefig(
    "tex/figures/EH_ALP-1s_to_5s-daily_modulation-Omega_a.pdf",
    transparent=False,
)
plt.savefig(
    "tex/figures/EH_ALP-1s_to_5s-daily_modulation-Omega_a.png",
    transparent=False,
)

plt.show()
