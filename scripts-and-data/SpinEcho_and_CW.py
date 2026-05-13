# $env:PYTHONPATH = "C:\Users\zhenf\D\Yu0702\Axionbloch-paper;$env:PYTHONPATH”
# This file is for plotting the free decay of the spin system under a RF pulse.
from tkinter import font

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import font_manager

from src.utils import high_contrast_extended
data_dir = "scripts-and-data/"
echo_data = np.load(data_dir + "SpinEcho_CPMG_simu.npz")
echo_Tdelta = echo_data["Tdelta_s"]
echo_T2 = echo_data["T2_s"]
echo_T2star = (echo_T2 ** (-1) + echo_Tdelta ** (-1)) ** (-1)
size = len(echo_data["timeStamp_s"]) - 1
echo_timeStamp_s = echo_data["timeStamp_s"][:size]  # timeStamp_s.shape (5050,)
echo_B_vec = echo_data["B_vec"][0][
    :size
]  # data["B_vec"].shape : tuple((1, 5050, 3)) [len=3]
echo_M = echo_data["trjry"][0][
    :size
]  # data["trjry"].shape : tuple((1, 5051, 3)) [len=3]

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
    figsize=(2 * 8.5 * cm, 5 * cm), dpi=300
)  # initialize a figure following APS journal requirements
# #############################################################################
# to specify heights and widths of subfigures
width_ratios = [1, 1]
height_ratios = [0.5, 1]
gs = gridspec.GridSpec(
    nrows=2, ncols=2, width_ratios=width_ratios, height_ratios=height_ratios
)  # create grid for multiple figures
# #############################################################################
# fix the margins
left = 0.11
bottom = 0.238
right = 0.88
top = 0.888
wspace = 0.32
hspace = 0.14
fig.subplots_adjust(
    left=left, top=top, right=right, bottom=bottom, wspace=wspace, hspace=hspace
)
# #############################################################################
echo_pulse_ax = fig.add_subplot(gs[0, 0])
echo_M_ax = fig.add_subplot(gs[1, 0])

CW_pulse_ax = fig.add_subplot(gs[0, 1])
CW_M_ax = fig.add_subplot(gs[1, 1])
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
    echo_timeStamp_s[: len(echo_timeStamp_s) // 4],
    T2star_envelope[: len(echo_timeStamp_s) // 4],
    # label="$e^{{-t/T_2^*}}$",
    linestyle="dashed",
    color="k",
    linewidth=linewidth,
)
echo_M_ax.text(
    2.1,
    0.18,
    # "$e^{\\frac{-t}{T_2^*}}$",
    "$e^{-t/T_2^*}$",
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
    "$e^{-t/T_2}$",
    color=high_contrast_extended[5],
    fontsize=10,
    ha="left",
)

echo_M_ax.set_xlabel("Time (s)")
echo_M_ax.set_ylabel("$M / M_\\mathrm{eqb}$")
echo_M_ax.set_ylim(-1.1, 1.1)
# echo_M_ax.set_xlim(right= 5)

echo_pulse_ax.set_xticklabels([])  # hide x-axis tick labels for the upper plot

# echo_pulse_ax.legend(
#     loc="upper left",
#     bbox_to_anchor=(1.0, 1.0),
#     frameon=False,
# )
# echo_M_ax.legend(
#     loc="upper left",
#     bbox_to_anchor=(1.0, 1.0),
#     frameon=False,
# )
# echo_M_ax.legend(loc="upper right", ncol=2, frameon=False)


CW_data = np.load(data_dir + "RF_CW_simu.npz")
CW_Tdelta = CW_data["Tdelta_s"]
CW_T2 = CW_data["T2_s"]
CW_T2star = (CW_T2 ** (-1) + CW_Tdelta ** (-1)) ** (-1)

size = len(CW_data["timeStamp_s"]) - 1
CW_timeStamp_s = CW_data["timeStamp_s"][:size]  # timeStamp_s.shape (5050,)
CW_B_vec = CW_data["B_vec"][0][
    :size
]  # data["B_vec"].shape : tuple((1, 5050, 3)) [len=3]
CW_M = CW_data["trjry"][0][:size]  # data["trjry"].shape : tuple((1, 5051, 3)) [len=3]


CW_pulse_ax.plot(
    CW_timeStamp_s,
    CW_B_vec[:, 0] * 1e9,
    label="$B_{x}$",
    color=high_contrast_extended[0],
    linewidth=linewidth,
)
CW_pulse_ax.plot(
    CW_timeStamp_s,
    CW_B_vec[:, 1] * 1e9,
    label="$B_{y}$",
    color=high_contrast_extended[1],
    linewidth=linewidth,
)
CW_pulse_ax.set_xlabel("")
# CW_pulse_ax.set_ylabel("$B\\,(\\mathrm{p T})$")
# pulse_ax.legend(loc="upper right", ncol=2, frameon=False)

CW_M_ax.plot(
    CW_timeStamp_s,
    CW_M[:, 0],
    label="$M_{x}$",
    color=high_contrast_extended[2],
    linewidth=linewidth,
)
CW_M_ax.plot(
    CW_timeStamp_s,
    CW_M[:, 1],
    label="$M_{y}$",
    color=high_contrast_extended[3],
    linewidth=linewidth,
)
# M_ax.plot(
#     timeStamp_s,
#     (M[:, 0] ** 2 + M[:, 1] ** 2) ** 0.5,
#     label="$(M_{x}^2 + M_{y}^2)^{1/2}$",
#     linestyle="dashed",
#     color=high_contrast_extended[5],
# )
gamma = 2 * np.pi * 42.57747892e6  # gyromagnetic ratio of proton in Hz/T
B1_T = 0.5 * 1e-11  # magnetic field strength in Tesla
T2star_envelope = (1 - np.exp(-(CW_timeStamp_s) / CW_T2star)) * B1_T * gamma * CW_T2star
CW_M_ax.plot(
    CW_timeStamp_s[: len(CW_timeStamp_s) // 1],
    T2star_envelope[: len(CW_timeStamp_s) // 1],
    # label="$\\gamma B T_2^*\\times$\n$(1-e^{-t/T_2^*})$",
    linestyle="dashed",
    color="#393b79",
    linewidth=linewidth,
)
CW_M_ax.text(
    3.5,
    0.0016,
    # "$\\gamma B T_2^* (1-e^{\\frac{-t}{T_2^*}})$",
    "$\\gamma B T_2^* (1-e^{-t/T_2^*})$",
    # transform=M_ax.transAxes,
    # fontsize=8,
    color="#393b79",
    ha="left",
)

# T2_envelope = np.exp(-(timeStamp_s + 0.02) / T2)
# M_ax.plot(
#     timeStamp_s,
#     T2_envelope,
#     label=f"$e^{{-t/T_2}}$",
#     linestyle="dashed",
#     color=high_contrast_extended[5],
#     linewidth = linewidth ,
# )
CW_M_ax.set_xlabel("Time (s)")
# CW_M_ax.set_ylabel("Normalized $\\mathbf{M}$")

CW_pulse_ax.set_ylim(-7e-3, 7e-3)
CW_M_ax.set_ylim(-0.0015, 0.00236)
# M_ax.set_xlim(right= 5)

CW_pulse_ax.set_xticklabels([])  # hide x-axis tick labels for the upper plot

CW_pulse_ax.legend(
    loc="upper left",
    bbox_to_anchor=(1.0, 1.0),
    frameon=False,
)
CW_M_ax.legend(
    loc="upper left",
    bbox_to_anchor=(1.0, 1.0),
    frameon=False,
)
# M_ax.legend(loc="upper right", ncol=2, frameon=False)


# put figure index
letters = ["(a)", "(b)", "(c)", "(d)", "(e)", "(f)", "(g)", "(h)", "(i)"]
for i, ax in enumerate([echo_pulse_ax, CW_pulse_ax]):
    xleft, xright = ax.get_xlim()
    ybottom, ytop = ax.get_ylim()
    ax.text(-0.25, 1.2, letters[i], transform=ax.transAxes)
# ha = 'left' or 'right'
# va = 'top' or 'bottom'
# plt.tight_layout()
plt.savefig("tex/figures/SpinEcho_and_CW.pdf")
plt.show()
