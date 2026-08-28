# import os
# import sys
# from turtle import color
# print(os.path.abspath(os.curdir))
# sys.path.insert(0, os.path.abspath(os.curdir))
# os.chdir("..")  # if you want to go to parent folder
# os.chdir("..")
# print(os.path.abspath(os.curdir))
# sys.path.insert(0, os.path.abspath(os.curdir))

# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.gridspec as gridspec
# import time
# from NMRKineticSimu import Xe129, Methanol, TestSample10MHzT, Mainz, TestStation, MagVec, AxionWind
# from NMRKineticSimu import *
# from DataAnalysis import LIASignal, SQUID, Exclusion
# from DataAnalysis import *
# from functioncache import check, Lorentzian
from src.dependency import *

# plt.rc("font", size=12)
# plt.rcParams["font.family"] = "Times New Roman"
# # plt.rcParams["font.family"] = "serif"
# # plt.rcParams["font.serif"] = ["Times New Roman"]
# plt.rcParams["mathtext.fontset"] = "cm"  # 'dejavuserif'
fig = plt.figure(figsize=(13/2.54, 6.5/2.54), dpi=300)
gs = gridspec.GridSpec(nrows=3, ncols=5, height_ratios=[1.5, 2.0, 1.0])
fig.subplots_adjust(
    top=0.97, bottom=0.03, left=0.025, right=0.975, hspace=0.11, wspace=0.0
)
lw = 1.0
nu = 2

ax = fig.add_subplot(gs[0, :])
extimestamp = np.linspace(start=16, stop=19, num=500)
ax.plot(
    extimestamp,
    3 * np.sin(2 * np.pi * nu * extimestamp),
    label="",
    color="blue",
    alpha=1,
    lw=lw,
)
# ax.plot(GammaandSAmp_arr, GammaandSAmp_arr, label='', color='tab:blue', alpha=1, linestyle='-')
# ax.scatter(GammaandSAmp_arr, GammaandSAmp_arr, marker='x', s=30, color='tab:blue', alpha=1)
# ax.arrow(x=0, y=0, dx=60, dy=0, width=0.005, head_width=1.0, head_length=1.4, color='black', \
#             edgecolor='none', length_includes_head=True, shape='full', )
ax.quiver(
    [0],
    [0],
    [60],
    [0],
    angles="xy",
    scale_units="xy",
    scale=1,
    color="black",
    width=0.004,
)
ax.set_xlim(0, 60)
ax.set_ylim(-3.2, 3.2)
ax.text(x=1, y=0.25, s="in excitation coil")
ax.text(x=58, y=-1.5, s="time")
ax.axis("off")
# ax.grid()


ax2 = fig.add_subplot(gs[2, :])

# ax2.arrow(x=0, y=0., dx=60, dy=0, width=0.005, head_width=1, head_length=1.4, color='black', \
#             edgecolor='none', length_includes_head=True, shape='full', )
ax2.quiver(
    [0],
    [0],
    [60],
    [0],
    angles="xy",
    scale_units="xy",
    scale=1,
    color="black",
    width=0.004,
)
pktimestamp = np.linspace(start=28, stop=55, num=1500)
ax2.plot(
    pktimestamp,
    2.4
    * np.exp(-(pktimestamp - pktimestamp[0]) / 8)
    * np.cos(2 * np.pi * nu * (pktimestamp - pktimestamp[0])),
    label="",
    color="tab:blue",
    alpha=1,
    lw=lw,
)
ax2.plot(
    pktimestamp,
    2.4 * np.exp(-(pktimestamp - pktimestamp[0]) / 8),
    label="",
    color="tab:red",
    alpha=1,
    lw=lw,
)
ax2.set_xlim(0, 60)
ax2.set_ylim(-2.6, 2.6)
ax2.text(x=1, y=0.45, s="in pickup coil")
# ax2.text(
#     x=35, y=1.4, s="$M_{xy} \\sim e^{-t/T_2^*}\\cos(\\omega t + \\phi_0)$"
# )
ax2.text(x=35, y=1.4, s="$M_{xy} \\sim e^{-t/T_2^*}$", color="tab:red")
ax2.text(x=58, y=-1.5, s="time")
ax2.axis("off")
# ax2.grid()

ax13 = fig.add_subplot(gs[1, 3])

ax13.plot([2, 2], [90, 50], color="black", label="", alpha=1, lw=lw)
ax13.plot([31, 31], [90, 50], color="black", label="", alpha=1, lw=lw)
coil_radius = 20
coil_period = 1
timestamp = np.linspace(start=0, stop=5 - 0.5 * coil_period, num=1500)
centerstamp = coil_radius + 2 + 2 * timestamp
xstamp = (
    -coil_radius * 0.5000
    + centerstamp
    + 0.5 * coil_radius * np.sin(2 * np.pi / coil_period * timestamp + np.pi * 3 / 2)
)
ystamp = 50 + coil_radius * np.sin(2 * np.pi / coil_period * timestamp + np.pi * 2 / 2)
ax13.plot(xstamp, ystamp, label="", color="black", alpha=1, lw=lw)
ax13.set_xlim(0, 100)
ax13.set_ylim(0, 100)
ax13.text(x=35, y=50, s="Excitation / Pickup coil")
# ax2.text(x=58, y=-1.5,s='time')
ax13.axis("off")

ax10 = fig.add_subplot(gs[1, 0], projection="3d", azim=30, elev=20)
plt.gca().invert_yaxis()
ax10.grid(False)
ax10.xaxis.set_pane_color((1, 1, 1, 0.0))
ax10.yaxis.set_pane_color((1, 1, 1, 0.0))
ax10.zaxis.set_pane_color((1, 1, 1, 0.0))
# draw the cooridnates
ax10.quiver(
    0,
    0,
    0,  # <-- starting point of vector
    1,
    0,
    0,  # <-- directions of vector
    color="black",
    alpha=1,
    lw=lw,
    length=2.0,
    normalize=False,
    arrow_length_ratio=0.10,
)
ax10.quiver(
    0,
    0,
    0,  # <-- starting point of vector
    0,
    1,
    0,  # <-- directions of vector
    color="black",
    alpha=1,
    lw=lw,
    length=1.4,
    normalize=False,
    arrow_length_ratio=0.10,
)
ax10.quiver(
    0,
    0,
    0,  # <-- starting point of vector
    0,
    0,
    1,  # <-- directions of vector
    color="black",
    alpha=1,
    lw=lw,
    length=1.4,
    normalize=False,
    arrow_length_ratio=0.10,
)
ax10.text(0.8, 1.55, 0, "y", color="black")
ax10.text(2.4, 0.35, 0, "x", color="black")
ax10.text(0, 0.05, 1.25, "z", color="black")
# draw the sphere
r = 1
u, v = np.mgrid[0 : 2 * np.pi : 20j, 0 : np.pi : 20j]
x = np.cos(u) * np.sin(v)
y = np.sin(u) * np.sin(v)
z = np.cos(v)
ax10.plot_surface(x, y, z, cmap=plt.cm.YlGnBu_r, alpha=0.2)
# draw B0
ax10.quiver(
    0,
    -0.95,
    0.75,  # <-- starting point of vector
    0,
    0,
    0.5,  # <-- directions of vector
    color="black",
    alpha=1,
    lw=lw,
    length=1.4,
    normalize=False,
    arrow_length_ratio=0.45,
)
ax10.text(0, -0.85, 1.25, "$\\mathbf{B}_0$", color="black")
ax10.text(1, 0.85, 1.25, "$\\mathbf{M}$", color="g")

# draw magnetization vectors
timestamp = np.linspace(start=0, stop=1, num=1000)
magz = np.cos(2 * np.pi * nu / 10 * timestamp)
magx = np.sqrt(1 - magz**2) * np.cos(2 * np.pi * nu * 1 * timestamp)
magy = np.sqrt(1 - magz**2) * np.sin(2 * np.pi * nu * 1 * timestamp)
ax10.quiver(
    0,
    0,
    0,  # <-- starting point of vector
    magx[0],
    magy[0],
    magz[0],  # <-- directions of vector
    color="g",
    alpha=1,
    lw=lw,
    length=1,
    normalize=False,
    arrow_length_ratio=0.25,
    label="$\\vec{M}$",
)
try:
    ax10.set_aspect("equal")
except NotImplementedError:
    pass

XYZlim = [-0.9, 0.9]
ax10.set_xlim3d(XYZlim)
ax10.set_ylim3d(XYZlim)
ax10.set_zlim3d(XYZlim)
ax10.set_xlabel("x")
ax10.set_ylabel("y")
ax10.set_zlabel("z")
ax10.axis("off")
# ax10.legend(loc='upper right')
ax10.set_box_aspect((1, 1, 1))

# in excitation
ax11 = fig.add_subplot(gs[1, 1], projection="3d", azim=30, elev=20)
plt.gca().invert_yaxis()
ax11.grid(False)
ax11.xaxis.set_pane_color((1, 1, 1, 0.0))
ax11.yaxis.set_pane_color((1, 1, 1, 0.0))
ax11.zaxis.set_pane_color((1, 1, 1, 0.0))
# draw the cooridnates
ax11.quiver(
    0,
    0,
    0,  # <-- starting point of vector
    1,
    0,
    0,  # <-- directions of vector
    color="black",
    alpha=1,
    lw=lw,
    length=2.0,
    normalize=False,
    arrow_length_ratio=0.10,
)
ax11.quiver(
    0,
    0,
    0,  # <-- starting point of vector
    0,
    1,
    0,  # <-- directions of vector
    color="black",
    alpha=1,
    lw=lw,
    length=1.4,
    normalize=False,
    arrow_length_ratio=0.10,
)
ax11.quiver(
    0,
    0,
    0,  # <-- starting point of vector
    0,
    0,
    1,  # <-- directions of vector
    color="black",
    alpha=1,
    lw=lw,
    length=1.4,
    normalize=False,
    arrow_length_ratio=0.10,
)
ax11.text(0.8, 1.55, 0, "y", color="black")
ax11.text(2.4, 0.35, 0, "x", color="black")
ax11.text(0, 0.05, 1.25, "z", color="black")
# draw the sphere
r = 1
u, v = np.mgrid[0 : 2 * np.pi : 20j, 0 : np.pi : 20j]
x = np.cos(u) * np.sin(v)
y = np.sin(u) * np.sin(v)
z = np.cos(v)
ax11.plot_surface(x, y, z, cmap=plt.cm.YlGnBu_r, alpha=0.2)
# draw B0
ax11.quiver(
    0,
    -0.95,
    0.75,  # <-- starting point of vector
    0,
    0,
    0.5,  # <-- directions of vector
    color="black",
    alpha=1,
    lw=lw,
    length=1.4,
    normalize=False,
    arrow_length_ratio=0.45,
)
ax11.text(0, -0.85, 1.25, "$\\mathbf{B}_0$", color="black")

# draw magnetization vectors
timestamp = np.linspace(start=0, stop=1, num=1000)
magz = np.cos(2 * np.pi * 1 / 4 * timestamp)
magx = np.sqrt(1 - magz**2) * np.cos(2 * np.pi * nu * 1 * timestamp)
magy = np.sqrt(1 - magz**2) * np.sin(2 * np.pi * nu * 1 * timestamp)
ax11.plot(xs=magx, ys=magy, zs=magz, zdir="z", color="tab:green", linewidth=0.50)
ax11.quiver(
    0,
    0,
    0,  # <-- starting point of vector
    magx[-1],
    magy[-1],
    magz[-1],  # <-- directions of vector
    color="g",
    alpha=1,
    lw=lw,
    length=1,
    normalize=False,
    arrow_length_ratio=0.25,
    label="$\\vec{M}$",
)
try:
    ax11.set_aspect("equal")
except NotImplementedError:
    pass

XYZlim = [-0.9, 0.9]
ax11.set_xlim3d(XYZlim)
ax11.set_ylim3d(XYZlim)
ax11.set_zlim3d(XYZlim)
ax11.set_xlabel("x")
ax11.set_ylabel("y")
ax11.set_zlabel("z")
ax11.axis("off")
# ax11.legend(loc='upper right')
ax11.set_box_aspect((1, 1, 1))


# free decay
ax12 = fig.add_subplot(gs[1, 2], projection="3d", azim=30, elev=20)
plt.gca().invert_yaxis()
ax12.grid(False)
ax12.xaxis.set_pane_color((1, 1, 1, 0.0))
ax12.yaxis.set_pane_color((1, 1, 1, 0.0))
ax12.zaxis.set_pane_color((1, 1, 1, 0.0))
# draw the cooridnates
ax12.quiver(
    0,
    0,
    0,  # <-- starting point of vector
    1,
    0,
    0,  # <-- directions of vector
    color="black",
    alpha=1,
    lw=lw,
    length=2.0,
    normalize=False,
    arrow_length_ratio=0.10,
)
ax12.quiver(
    0,
    0,
    0,  # <-- starting point of vector
    0,
    1,
    0,  # <-- directions of vector
    color="black",
    alpha=1,
    lw=lw,
    length=1.4,
    normalize=False,
    arrow_length_ratio=0.10,
)
ax12.quiver(
    0,
    0,
    0,  # <-- starting point of vector
    0,
    0,
    1,  # <-- directions of vector
    color="black",
    alpha=1,
    lw=lw,
    length=1.4,
    normalize=False,
    arrow_length_ratio=0.10,
)
ax12.text(0.8, 1.55, 0, "y", color="black")
ax12.text(2.4, 0.35, 0, "x", color="black")
ax12.text(0, 0.05, 1.25, "z", color="black")
# draw the sphere
r = 1
u, v = np.mgrid[0 : 2 * np.pi : 20j, 0 : np.pi : 20j]
x = np.cos(u) * np.sin(v)
y = np.sin(u) * np.sin(v)
z = np.cos(v)
ax12.plot_surface(x, y, z, cmap=plt.cm.YlGnBu_r, alpha=0.2)
# draw B0
ax12.quiver(
    0,
    -0.95,
    0.75,  # <-- starting point of vector
    0,
    0,
    0.5,  # <-- directions of vector
    color="black",
    alpha=1,
    lw=lw,
    length=1.4,
    normalize=False,
    arrow_length_ratio=0.45,
)
ax12.text(0, -0.85, 1.25, "$\\mathbf{B}_0$", color="black")

# draw magnetization vectors
trans_nu = 1 / 10
timestamp = np.linspace(start=1 / trans_nu / 4, stop=-6 / trans_nu / 4, num=2000)
magz = 1 - np.exp(
    -(1 / trans_nu / 4 - timestamp) / 4
)  # np.exp(-(1/trans_nu/4 - timestamp)/2)*
magx = (
    np.exp(-(1 / trans_nu / 4 - timestamp) / 2)
    * np.sqrt(1 - magz**2)
    * np.cos(2 * np.pi * nu * 1 * timestamp)
)
magy = (
    np.exp(-(1 / trans_nu / 4 - timestamp) / 2)
    * np.sqrt(1 - magz**2)
    * np.sin(2 * np.pi * nu * 1 * timestamp)
)
ax12.plot(xs=magx, ys=magy, zs=magz, zdir="z", color="tab:green", linewidth=0.50)
ax12.quiver(
    0,
    0,
    0,  # <-- starting point of vector
    magx[-1],
    magy[-1],
    magz[-1],  # <-- directions of vector
    color="g",
    alpha=1,
    lw=lw,
    length=1,
    normalize=False,
    arrow_length_ratio=0.25,
    label="$\\vec{M}$",
)
try:
    ax12.set_aspect("equal")
except NotImplementedError:
    pass

XYZlim = [-0.9, 0.9]
ax12.set_xlim3d(XYZlim)
ax12.set_ylim3d(XYZlim)
ax12.set_zlim3d(XYZlim)
ax12.set_xlabel("x")
ax12.set_ylabel("y")
ax12.set_zlabel("z")
ax12.axis("off")
# ax12.legend(loc='upper right')
ax12.set_box_aspect((1, 1, 1))


# plt.tight_layout()
plt.show()
