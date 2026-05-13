# $env:PYTHONPATH = "C:\Users\zhenf\D\Yu0702\Axionbloch-paper;$env:PYTHONPATH”
# This file is for plotting the free decay of the spin system under a RF pulse.
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import font_manager

from src.utils import high_contrast_extended

data = np.load("figures/RF_pulse_simu.npz")
size = len(data["timeStamp_s"])
timeStamp_s = data["timeStamp_s"][:size//2]  # timeStamp_s.shape (5050,)
B_vec = data["B_vec"][0][:size//2]  # data["B_vec"].shape : tuple((1, 5050, 3)) [len=3]
M = data["trjry"][0][:size//2]  # data["trjry"].shape : tuple((1, 5051, 3)) [len=3]


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
left = 0.173
bottom = 0.17
right = 0.717
top = 0.916
wspace = 0.2
hspace = 0.14
fig.subplots_adjust(
    left=left, top=top, right=right, bottom=bottom, wspace=wspace, hspace=hspace
)
# #############################################################################
pulse_ax = fig.add_subplot(gs[0, 0])
M_ax = fig.add_subplot(gs[1, 0])

pulse_ax.plot(
    timeStamp_s,
    B_vec[:, 0] * 1e9,
    label="$B_{x}$",
    color=high_contrast_extended[0],
)
pulse_ax.plot(
    timeStamp_s,
    B_vec[:, 1] * 1e9,
    label="$B_{y}$",
    color=high_contrast_extended[1],
)
pulse_ax.set_xlabel("")
pulse_ax.set_ylabel("$B$ (nT)")
pulse_ax.set_xticklabels([])  # hide x-axis tick labels for the upper plot
# pulse_ax.legend(loc="upper right", ncol=2, frameon=False)

M_ax.plot(
    timeStamp_s,
    M[:, 0],
    label="$M_{x}$",
    color=high_contrast_extended[2],
)
M_ax.plot(
    timeStamp_s,
    M[:, 1],
    label="$M_{y}$",
    color=high_contrast_extended[3],
)
# M_ax.plot(
#     timeStamp_s,
#     (M[:-1, 0] ** 2 + M[:-1, 1] ** 2) ** 0.5,
#     label="$(M_{x}^2 + M_{y}^2)^{1/2}$",
#     linestyle="dashed",
#     color=high_contrast_extended[5],
# )
decay_envelope = np.exp(-(timeStamp_s+0.02) / 1)
M_ax.plot(
    timeStamp_s,
    decay_envelope,
    label=f"$e^{{-t/T_2^*}}$",
    linestyle="dashed",
    color=high_contrast_extended[4],
)
M_ax.set_xlabel("Time (s)")
M_ax.set_ylabel("Normalized $\\mathbf{M}$")
# M_ax.set_ylim(-1.1, 1.25)
# M_ax.set_xlim(right= 5)

pulse_ax.legend(
    # loc="upper right",
    bbox_to_anchor=(1.0, 1.0),
    frameon=False,
)
M_ax.legend(
    # loc="upper right",
    bbox_to_anchor=(1.0, 1.0),
    frameon=False,
)
# M_ax.legend(loc="upper right", ncol=2, frameon=False)

# put figure index
letters = ["(a)", "(b)", "(c)", "(d)", "(e)", "(f)", "(g)", "(h)", "(i)"]
for i, ax in enumerate([pulse_ax]):
    xleft, xright = ax.get_xlim()
    ybottom, ytop = ax.get_ylim()
    ax.text(-0.3, 1.09, letters[i], transform=ax.transAxes)
# ha = 'left' or 'right'
# va = 'top' or 'bottom'
# plt.tight_layout()
plt.savefig("figures/free_decay.pdf")
plt.show()
