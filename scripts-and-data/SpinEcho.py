# $env:PYTHONPATH = "C:\Users\zhenf\D\Yu0702\Axionbloch-paper;$env:PYTHONPATH”
# This file is for plotting the free decay of the spin system under a RF pulse.
from tkinter import font

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import font_manager

from src.utils import high_contrast_extended

echo_data = np.load("figures/SpinEcho_CPMG_simu.npz")
echo_Tdelta = echo_data["Tdelta_s"]
echo_T2 = echo_data["T2_s"]
echo_T2star = (echo_T2 ** (-1) + echo_Tdelta ** (-1)) ** (-1)
size = len(echo_data["timeStamp_s"]) - 1
echo_timeStamp_s = echo_data["timeStamp_s"][:size]  # timeStamp_s.shape (5050,)
echo_B_vec = echo_data["B_vec"][0][:size]  # data["B_vec"].shape : tuple((1, 5050, 3)) [len=3]
echo_M = echo_data["trjry"][0][:size]  # data["trjry"].shape : tuple((1, 5051, 3)) [len=3]

linewidth = 1

plt.rc("font", size=10)  # font size for all figures
# plt.rcParams['font.family'] = 'serif'
# plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams["font.family"] = "Times New Roman"
# plt.rcParams['mathtext.fontset'] = 'dejavuserif'

# Make math text match Times New Roman
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["mathtext.rm"] = "Times New Roman"
cm = 1 / 2.56  # convert cm to inch
fig = plt.figure(
    figsize=(8.5 * cm, 5 * cm), dpi=300
)  # initialize a figure following APS journal requirements
# #############################################################################
# to specify heights and widths of subfigures
width_ratios = [1]
height_ratios = [0.5, 1]
gs = gridspec.GridSpec(
    nrows=2, ncols=1, width_ratios=width_ratios, height_ratios=height_ratios
)  # create grid for multiple figures
# #############################################################################
# fix the margins
left = 0.22
bottom = 0.238
right = 0.767
top = 0.888
wspace = 0.2
hspace = 0.14
fig.subplots_adjust(
    left=left, top=top, right=right, bottom=bottom, wspace=wspace, hspace=hspace
)
# #############################################################################
echo_pulse_ax = fig.add_subplot(gs[0, 0])
echo_M_ax = fig.add_subplot(gs[1, 0])

echo_pulse_ax.plot(
    echo_timeStamp_s,
    echo_B_vec[:, 0] * 1e9,
    label="$B_{x}$",
    color=high_contrast_extended[0],
    linewidth=linewidth,
)
echo_pulse_ax.plot(
    echo_timeStamp_s,
    echo_B_vec[:, 1] * 1e9,
    label="$B_{y}$",
    color=high_contrast_extended[1],
    linewidth=linewidth,
)
echo_pulse_ax.set_xlabel("")
echo_pulse_ax.set_ylabel("$B\\,(\\mathrm{n T})$")
# echo_pulse_ax.legend(loc="upper right", ncol=2, frameon=False)

echo_M_ax.plot(
    echo_timeStamp_s,
    echo_M[:, 0],
    label="$M_{x}$",
    color=high_contrast_extended[2],
    linewidth=linewidth,
)
echo_M_ax.plot(
    echo_timeStamp_s,
    echo_M[:, 1],
    label="$M_{y}$",
    color=high_contrast_extended[3],
    linewidth=linewidth,
)
# echo_M_ax.plot(
#     timeStamp_s,
#     (M[:-1, 0] ** 2 + M[:-1, 1] ** 2) ** 0.5,
#     label="$(M_{x}^2 + M_{y}^2)^{1/2}$",
#     linestyle="dashed",
#     color=high_contrast_extended[5],
# )
T2star_envelope = np.exp(-(echo_timeStamp_s + 0.02) / echo_T2star)
echo_M_ax.plot(
    echo_timeStamp_s[: len(echo_timeStamp_s) // 2],
    T2star_envelope[: len(echo_timeStamp_s) // 2],
    # label="$e^{{-t/T_2^*}}$",
    linestyle="dashed",
    color="k",
    linewidth=linewidth,
)
echo_M_ax.text(
    2.1,
    0.18,
    "$e^{\\frac{-t}{T_2^*}}$",
    color="k",
    fontsize=10,
    ha="left",
)
T2_envelope = np.exp(-(echo_timeStamp_s + 0.02) / echo_T2)
echo_M_ax.plot(
    echo_timeStamp_s,
    T2_envelope,
    # label="$e^{{-t/T_2}}$",
    linestyle="dashed",
    color=high_contrast_extended[5],
    linewidth=linewidth,
)
echo_M_ax.text(
    11.3,
    0.4,
    "$e^{\\frac{-t}{T_2}}$",
    color=high_contrast_extended[5],
    fontsize=10,
    ha="left",
)

echo_M_ax.set_xlabel("Time (s)")
echo_M_ax.set_ylabel("Normalized $\\mathbf{M}$")
echo_M_ax.set_ylim(-1.1, 1.1)
# echo_M_ax.set_xlim(right= 5)

echo_pulse_ax.set_xticklabels([])  # hide x-axis tick labels for the upper plot

echo_pulse_ax.legend(
    loc="upper left",
    bbox_to_anchor=(1.0, 1.0),
    frameon=False,
)
echo_M_ax.legend(
    loc="upper left",
    bbox_to_anchor=(1.0, 1.0),
    frameon=False,
)
# echo_M_ax.legend(loc="upper right", ncol=2, frameon=False)

# put figure index
letters = ["(a)", "(b)", "(c)", "(d)", "(e)", "(f)", "(g)", "(h)", "(i)"]
for i, ax in enumerate([echo_pulse_ax]):
    xleft, xright = ax.get_xlim()
    ybottom, ytop = ax.get_ylim()
    ax.text(-0.4, 1.2, letters[0], transform=ax.transAxes)
# ha = 'left' or 'right'
# va = 'top' or 'bottom'
# plt.tight_layout()
plt.savefig("figures/SpinEcho.pdf")
plt.show()
