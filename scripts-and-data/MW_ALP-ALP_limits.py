"""Plot the 2022-12-23 MW axion exclusion limits.

Run from any directory; use --no-show for noninteractive figure generation.
"""

import argparse
from pathlib import Path

from src.dependency import *


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = Path(__file__).with_name(
    "20221223_MW_axion_exclusion_20260907_203500.txt"
)
OUTPUT = ROOT / "tex" / "figures" / "MW_ALP-ALP_limits"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-show", action="store_true")
    args = parser.parse_args()
    if args.no_show:
        plt.switch_backend("Agg")

    data = np.loadtxt(DATA_PATH, comments="#", ndmin=2)
    # Columns: frequency offset (Hz), frequency (Hz), limit (GeV^-1),
    # valid mask, candidate mask. Candidate bins retain their supplied limits.
    offset, frequency, limit, valid_mask, _ = data.T
    valid = (
        np.isfinite(offset)
        & np.isfinite(frequency)
        & np.isfinite(limit)
        & (valid_mask == 1)
        & (limit > 0)
    )
    if not np.any(valid):
        raise ValueError("No valid, finite, positive limits to plot.")
    reference_hz = 1.348570e6

    # Match 5sigma-2-Gaussian_distributions.py and src/dependency.py.
    # plt.rcParams.update({
    #     "font.size": 8,
    #     "font.family": "Times New Roman",
    #     "mathtext.fontset": "cm",
    #     "mathtext.rm": "Times New Roman",
    #     "lines.linewidth": 1.0,
    #     "lines.markersize": 0.5,
    #     "figure.dpi": 300,
    #     "savefig.dpi": 300,
    # })
    fig, ax = plt.subplots(figsize=(13 / 2.54, 5.2 / 2.54), dpi=300)
    fig.subplots_adjust(left=0.227, bottom=0.21, right=0.812, top=0.95)

    # Mask rather than remove invalid rows, preserving gaps in the curve.
    order = np.argsort(frequency, kind="stable")
    ax.plot(
        np.ma.masked_where(~valid[order], offset[order]),
        np.ma.masked_where(~valid[order], limit[order]),
        color="tab:blue",
    )
    ax.set_yscale("log")
    ax.set_xlabel("$\\mathrm{Frequency} - 1\\,348\\,570\\,(\\mathrm{Hz})$")
    ax.set_ylabel("$|g_{\\mathrm{ap}}|$ limit ($\\mathrm{GeV}^{-1}$)")

    ax.set_xlim(-158, 158)
    ax.set_ylim(5.8e-3, 2.7e-2)

    ax.set_xticks([-120, -60, 0, 60, 120])
    ax.set_xticklabels(["-120", "-60", "0", "60", "120"])

    ax.fill_between(
        offset[order],
        np.ma.masked_where(~valid[order], limit[order]),
        ax.get_ylim()[1],
        color="tab:blue",
        alpha=0.5,
    )

    ax.grid(visible=True, which="major", axis="both", color="0.8", linestyle="--")
    ax.margins(x=0.02, y=0.1)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    for suffix in (".png", ".pdf"):
        fig.savefig(OUTPUT.with_suffix(suffix), transparent=False)
    print(f"Plotted {valid.sum()} of {len(data)} rows; excluded {(~valid).sum()}.")
    print(f"Saved {OUTPUT.with_suffix('.png')} and .pdf")
    if not args.no_show:
        plt.show()
    plt.close(fig)


if __name__ == "__main__":
    main()
