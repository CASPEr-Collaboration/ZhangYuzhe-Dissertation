# $env:PYTHONPATH = "C:\Users\zhenf\D\Yu0702\Axionbloch-paper;$env:PYTHONPATH”
# This file is for plotting the Milky Way axion-induced magnetic field and the resulting spin dynamics.
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import font_manager

from src.utils import high_contrast_extended, linestyles

# np.savez(
#     "C:\\Users\\zhenf\\D\\Yu0702\\CASPEr-Collaboration\\AxionBloch-paper/figures/Axion-Xe_NMR-simulations.npz",
#     timeStamp_s=timeStamp_s,
#     B_vec_mean=simu.excField.B_vec_mean,
#     B_vec_std=simu.excField.B_vec_std,
#     M_mean=simu.M_mean,
#     M_std=simu.M_std,
#     Mxy_mrs=simu.Mxy_mrs,
#     Mxy_srs=simu.Mxy_srs,
#     T2_s=sample.T2.value_in("s"),
#     Tdelta_s=simu_all.pool[i].simu.Tdelta_s,
#     T_1_s=sample.T1.value_in("s"),
#     pol=sample.pol,
# )
MW_data = np.load("figures/Axion-Xe_NMR-simulations-1.npz")
MW_Tdelta = MW_data["Tdelta_s"]
MW_T2 = MW_data["T2_s"]
MW_T2star = (MW_T2 ** (-1.0) + MW_Tdelta ** (-1.0)) ** (-1.0)
MW_T1 = MW_data["T_1_s"]


size = len(MW_data["timeStamp_s"]) - 1
MW_timeStamp_s = MW_data["timeStamp_s"][:size]  # timeStamp_s.shape (5050,)
MW_B_vec_mean = MW_data["B_vec_mean"][:size]
MW_B_vec_std = MW_data["B_vec_std"][:size]
MW_M_mean = MW_data["M_mean"][:size]
MW_M_std = MW_data["M_std"][:size]

MW_Mxy_mean = MW_data["Mxy_mrs"][:size]
MW_Mxy_std = MW_data["Mxy_srs"][:size]

linewidth = 2
err_alpha = 0.5
plt.rc("font", size=10)  # font size for all figures
plt.rcParams["font.family"] = "Times New Roman"

# Make math text match Times New Roman
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["mathtext.rm"] = "Times New Roman"
cm = 1 / 2.56  # convert cm to inch
fig = plt.figure(
    figsize=(8.5 * cm, 7.5 * cm), dpi=300
)  # initialize a figure following APS journal requirements
# #############################################################################
# to specify heights and widths of subfigures
width_ratios = [1]
height_ratios = [1, 1, 2.5]
gs = gridspec.GridSpec(
    nrows=3, ncols=1, width_ratios=width_ratios, height_ratios=height_ratios
)  # create grid for multiple figures
# #############################################################################
# fix the margins
left = 0.193
bottom = 0.15
right = 0.955
top = 0.967
wspace = 0.15
hspace = 0.264
fig.subplots_adjust(
    left=left, top=top, right=right, bottom=bottom, wspace=wspace, hspace=hspace
)
# #############################################################################
MW_Bx_ax = fig.add_subplot(gs[0, 0])
MW_By_ax = fig.add_subplot(gs[1, 0], sharey=MW_Bx_ax)
MW_M_ax = fig.add_subplot(gs[2, 0])
xyz = ["x", "y", "z"]
B_unit = "pT"
B_scale = 1e18  # convert T to pT
for i, ax in enumerate([MW_Bx_ax, MW_By_ax]):
    ax.plot(
        MW_timeStamp_s,
        MW_B_vec_mean[:, i] * B_scale,
        label="$B_" + xyz[i] + "$ mean $\pm 1 \sigma$",
        color=high_contrast_extended[i],
        # linestyle=linestyles[i],
        alpha=1,
        zorder=3,
    )

M_start = 1

MW_M_ax.plot(
    MW_timeStamp_s[M_start:],
    MW_Mxy_mean[M_start:],
    label="$ M_{xy} / M_\\mathrm{eqb}$ mean $\pm 1 \sigma$",
    color=high_contrast_extended[5],
    linewidth=linewidth,
)


MW_M_ax.set_xlabel("Time (s)")

MW_M_ax.set_yscale("log")


# hide x-axis tick labels for the upper plot
MW_Bx_ax.set_xticklabels([]) 
MW_By_ax.set_xticklabels([]) 

MW_Bx_ax.set_yticks([-30, 0, 30])
# MW_Bx_ax.set_yticks([-30, 0, 30])
MW_M_ax.set_yticks([1, 1e1, 1e2, 1e3])

xleft, xright = MW_Bx_ax.get_xlim()
MW_By_ax.set_xlim(xleft, xright)
MW_M_ax.set_xlim(xleft, xright)

MW_Bx_ax.set_ylim(-35, 35)
MW_M_ax.set_ylim(0.9, 1.2e3)

MW_Bx_ax.set_ylabel("$B_x\\,(\\mathrm{a T})$")
MW_By_ax.set_ylabel("$B_y\\,(\\mathrm{a T})$")
MW_M_ax.set_ylabel("$M_{xy} / M_\\mathrm{eqb}$")


plt.savefig("figures/MilkyWayAxionHalo-1.pdf")
plt.show()
