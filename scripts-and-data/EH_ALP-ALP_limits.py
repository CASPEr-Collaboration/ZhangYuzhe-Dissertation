"""Plot the 2022-12-14 Earth halo axion exclusion limits.

Run from any directory; use --no-show for noninteractive figure generation.

% AXION_RABI_FREQUENCY = 2 * PI * 2 * unit.mHz
-> % AXION_RABI_FREQUENCY = 2 * PI * .1 * unit.mHz
-> a factor of 20 increase in the limit


"""

from pathlib import Path

from src.dependency import *

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = Path(__file__).with_name(
    "20221214_Earth_halo_axion_exclusion_20260729_1801.txt"
)

# limits in data assumed Omega_a = 2 pi * 2 mHz for gaNN = 1e-9 GeV^-1
data = np.loadtxt(DATA_PATH, comments="#", ndmin=2)

# This factor is applied to the limits to account for the change in Omega_a assumption
# for example, the original data assumed Omega_a = 2 pi * 2 mHz, but we want to plot
# the limits assuming Omega_a = 2 pi * 0.1 mHz, which is a factor of 20 smaller, so the limits are a factor of 20 larger.
gaNN_correction = 20

# Columns: frequency offset (Hz), frequency (Hz), limit (GeV^-1),
# valid mask, candidate mask. Candidate bins retain their supplied limits.
frequency_minus_offset, frequency, limit, valid_mask, _ = data.T
valid = (
    np.isfinite(frequency_minus_offset)
    & np.isfinite(frequency)
    & np.isfinite(limit)
    & (valid_mask == 1)
    & (limit > 0)
)
if not np.any(valid):
    raise ValueError("No valid, finite, positive limits to plot.")
# reference_hz = 1.348568e6
reference_hz = 1.348575e6


fig, ax = plt.subplots(figsize=(13 / 2.54, 5.2 / 2.54), dpi=300)
fig.subplots_adjust(left=0.227, bottom=0.21, right=0.812, top=0.95)

# Mask rather than remove invalid rows, preserving gaps in the curve.
order = np.argsort(frequency, kind="stable")
ax.plot(
    np.ma.masked_where(~valid[order], frequency[order]) - reference_hz,
    np.ma.masked_where(~valid[order], limit[order]) * gaNN_correction,
    color="tab:green",
)
ax.set_yscale("log")
ax.set_xlabel("$\\mathrm{Frequency} - 1\\,348\\,575\\,(\\mathrm{Hz})$")
ax.set_ylabel("$|g_{\\mathrm{ap}}|$ limit ($\\mathrm{GeV}^{-1}$)")

ax.set_xlim(-55, 55)
ax.set_ylim(6e-11, 1.8e-7)

ax.set_xticks([-50, -25, 0, 25, 50])
ax.set_xticklabels(["-50", "-25", "0", "25", "50"])

ax.fill_between(
    np.ma.masked_where(~valid[order], frequency[order]) - reference_hz,
    np.ma.masked_where(~valid[order], limit[order]) * gaNN_correction,
    ax.get_ylim()[1] * 1e2,
    color="tab:green",
    alpha=0.5,
)

ax.grid(visible=True, which="major", axis="both", color="0.8", linestyle="--")
ax.margins(x=0.02, y=0.1)

# OUTPUT.parent.mkdir(parents=True, exist_ok=True)
# for suffix in (".png", ".pdf"):
#     fig.savefig(OUTPUT.with_suffix(suffix), transparent=False)
# print(f"Plotted {valid.sum()} of {len(data)} rows; excluded {(~valid).sum()}.")
# print(f"Saved {OUTPUT.with_suffix('.png')} and .pdf")
# if not args.no_show:
fig.savefig(
    "tex/figures/EH_ALP-ALP_limits.pdf",
    # dpi=300,
    # bbox_inches="tight",
)
fig.savefig(
    "tex/figures/EH_ALP-ALP_limits.png",
    # dpi=300,
    # bbox_inches="tight",
)

plt.show()
