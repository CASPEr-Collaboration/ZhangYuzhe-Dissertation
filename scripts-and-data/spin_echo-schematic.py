# import os
# import sys
# from turtle import color
# print(os.path.abspath(os.curdir))
# sys.path.insert(0, os.path.abspath(os.curdir))
# # os.chdir("..")  # if you want to go to parent folder
# # os.chdir("..")
# # print(os.path.abspath(os.curdir))
# # sys.path.insert(0, os.path.abspath(os.curdir))

# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.gridspec as gridspec
# import time
# from NMRKineticSimu import Xe129, Methanol, TestSample10MHzT, Mainz, TestStation, MagVec, AxionWind
# from NMRKineticSimu import *
# from DataAnalysis import LIASignal, SQUID, Exclusion
# from DataAnalysis import *
from src.dependency import *
from src.utils import check, Lorentzian, Init_3020sphere, Init_0090sphere, Add_vector, sph2orth1d


def addrotation(
    ax
):
    timestamp = np.linspace(start=0, stop=0.899, num=1000)
    magx = 0.3 * np.cos(2 * np.pi * timestamp)
    magy = 0.3 * np.sin(2 * np.pi * timestamp)
    magz = 0.0 * np.ones(magx.shape)
    ax.plot(xs=magx, ys=magy, \
        zs=magz, zdir='z', color='k', lw=1.4, linestyle='-')
    ax.plot(xs=[magx[-1], magx[-1]-0.15*np.cos(10*np.pi/180)], \
        ys=[magy[-1], magy[-1]-0.15*np.sin(10*np.pi/180)], 
        zs=[0,0],
            lw=1.4, color='k', alpha=1.)
    ax.plot(xs=[magx[-1], magx[-1]-0.15*np.cos(70*np.pi/180)], \
        ys=[magy[-1], magy[-1]-0.15*np.sin(70*np.pi/180)], 
        zs=[0,0],
            lw=1.4, color='k', alpha=1.)
    # magnum = -2
    # Add_vector(ax20,
    #         start=[magx[-1]-0.001*np.cos(35*np.pi/180), magy[-1]-0.001*np.sin(35*np.pi/180), magz[-1]], end=[magx[-1], magy[-1], magz[-1]],
    #         mutation_scale=15, lw=1.4, color='k', alpha=.8, zorder=5)

T2 = 1.0
T2star = 0.1

Delta_t = 0.1
pulsedur = 0.001

omega0 = 2 * np.pi / (0.2+0.02)
omega1 = 0.86 * 2 * np.pi / (0.2+0.02)
omega2 = 0.74 * 2 * np.pi / (0.2+0.02)
omega3 = 0.62 * 2 * np.pi / (0.2+0.02)
omega_list = [omega0, omega1, omega2, omega3]
color_list = ['tab:red', 'tab:orange', 'tab:brown', 'tab:purple']

plt.rc('font', size=12)
plt.rcParams["font.family"] = "Times New Roman"
# plt.rcParams["font.family"] = "serif"
# plt.rcParams["font.serif"] = ["Times New Roman"]
plt.rcParams["mathtext.fontset"] = 'cm'  # 'dejavuserif'
fig = plt.figure(figsize=(8, 4.5),dpi=150)
gs = gridspec.GridSpec(nrows=4, ncols=6, height_ratios=[1.5, 2.0, 2.0, 1.5])
fig.subplots_adjust(top=0.97,
bottom=0.00,
left=0.04,
right=0.98,
hspace=0.0,
wspace=0.)

nu = 2

ax = fig.add_subplot(gs[0,:])
extimestamp = np.linspace(start=16, stop=19, num=500)
# ax.plot(extimestamp, 3 * np.sin(2 * np.pi * nu * extimestamp), label='', color='blue', alpha=1, lw=1.2)
ax.plot([0, 0, 1, 1], [0, 0.5, .5, 0], label='', color='blue', alpha=1, lw=1.2)
ax.plot([20, 20, 21, 21], [0, 1, 1, 0], label='', color='blue', alpha=1, lw=1.2)

ax.quiver([0], \
    [0], [60], [0], \
    angles='xy', scale_units='xy', scale=1, color='black', \
        width=0.004)
ax.set_xlim(0, 60)
ax.set_ylim(-1, 1.2)

ax.text(x=0, y=.7,s='$\\pi/2$ pulse', color='blue')
ax.text(x=20, y=1.1,s='$\\pi$ pulse', color='blue')

ax.text(x=2.9, y=0.2,s='(1)', color='k')
ax.text(x=16.5, y=0.2,s='(2)', color='k')
ax.text(x=22.5, y=0.2,s='(3)', color='k')


ax.quiver([2.8], \
    [0.32], [-1.2], [-0.28], \
    angles='xy', scale_units='xy', scale=1, color='black', \
        width=0.002)
ax.quiver([18.5], \
    [0.32], [1.2], [-0.28], \
    angles='xy', scale_units='xy', scale=1, color='black', \
        width=0.002)
ax.quiver([22.5], \
    [0.32], [-1.2], [-0.28], \
    angles='xy', scale_units='xy', scale=1, color='black', \
        width=0.002)

ax.text(x=1, y=-0.485,s='in excitation coil')
ax.text(x=58, y=-.5,s='time')
ax.axis('off')
# ax.grid()


ax2 = fig.add_subplot(gs[-1,:])
# ax2.arrow(x=0, y=0., dx=60, dy=0, width=0.005, head_width=1, head_length=1.4, color='black', \
#             edgecolor='none', length_includes_head=True, shape='full', )
ax2.quiver([0], \
    [0], [60], [0], \
    angles='xy', scale_units='xy', scale=1, color='black', \
        width=0.004)
pktimestamp = np.linspace(start=21, stop=59, num=1500)

pksignal = np.exp(-abs(pktimestamp - 40)) * np.cos(2 * np.pi * nu * (pktimestamp-pktimestamp[0]))
ax2.plot(pktimestamp, pksignal, label='', color='tab:blue', alpha=1, lw=1.2)

# ax2.plot(pktimestamp, 2.4 * np.exp(-(pktimestamp-pktimestamp[0])/8), label='', color='tab:red', alpha=1, lw=1.2)
ax2.set_xlim(0, 60)
ax2.set_ylim(-2.6, 2.6)

ax2.text(x=22.5, y=0.4,s='(3)', color='k')
ax2.text(x=33.5, y=.6,s='(4)', color='k')
ax2.text(x=41.5, y=1.3,s='(5) $t_c$', color='k')
ax2.text(x=48.5, y=0.4,s='(6)', color='k')

ax2.quiver([22.5], \
    [0.6], [-1.3], [-0.4], \
    angles='xy', scale_units='xy', scale=1, color='black', \
        width=0.002)
ax2.quiver([35.3], \
    [0.7], [1.5], [-0.5], \
    angles='xy', scale_units='xy', scale=1, color='black', \
        width=0.002)

ax2.quiver([41.3], \
    [1.65], [-1.3], [-0.45], \
    angles='xy', scale_units='xy', scale=1, color='black', \
        width=0.002)
ax2.quiver([48.2], \
    [0.5], [-1.5], [-0.4], \
    angles='xy', scale_units='xy', scale=1, color='black', \
        width=0.002)

ax2.text(x=1, y=-1.019,s='in pickup coil')
# ax2.text(x=40, y=-.8,s='$e^{-t/T_2} e^{-|t-t_c|/T_{\\delta}}$', ha='center', va ='top')
# ax2.text(x=30, y=-2.4,s='$M_{xy} = M_{xy0} e^{-t/T_2} e^{-|t-t_c|/T_{\\delta}}\\cos(\\omega t + \\varphi_0)$', fontsize=14)
#
ax2.text(x=58, y=-1.13,s='time')

ax2.axis('off')
# ax2.grid()


ax10 = fig.add_subplot(gs[1,0], projection='3d', azim=30, elev=20)
Init_3020sphere(
    ax10,
    verbose=False
    )


#
ax11 = fig.add_subplot(gs[1,1], projection='3d', azim=30, elev=20)
Init_3020sphere(
    ax11,
    verbose=False
    )


ax12 = fig.add_subplot(gs[1,2], projection='3d', azim=30, elev=20)
Init_3020sphere(
    ax12,
    verbose=False
    )

ax13 = fig.add_subplot(gs[1,3], projection='3d', azim=30, elev=20)
Init_3020sphere(
    ax13,
    verbose=False
    )

ax14 = fig.add_subplot(gs[1,4], projection='3d', azim=30, elev=20)
Init_3020sphere(
    ax14,
    verbose=False
    )


ax15 = fig.add_subplot(gs[1,5], projection='3d', azim=30, elev=20)
Init_3020sphere(
    ax15,
    verbose=False
    )

# after 90 deg pulse
ax20 = fig.add_subplot(gs[2, 0], projection='3d', azim=0, elev=90)
Init_0090sphere(
    ax20,
    verbose=False
    )
for i, omega in enumerate(omega_list) :
    vec = sph2orth1d([np.exp(-0 * Delta_t/T2), np.pi/2, 0 * Delta_t])
    Add_vector(ax10,
        start=[0,0,0], end=vec,
        lw=0.6*(4.0-i), color=color_list[i], verbose=False
    )
    Add_vector(ax20,
        start=[0,0,0], end=vec,
        lw=0.6*(4.0-i), color=color_list[i], verbose=False
    )
ax20.text(-1.4, -0.25, 0, '(1)', color='black')
addrotation(ax20)


# relaxation after 90 deg pulse
ax21 = fig.add_subplot(gs[2, 1], projection='3d', azim=0, elev=90)
Init_0090sphere(
    ax21,
    verbose=False
    )
for i, omega in enumerate(omega_list) :
    vec = sph2orth1d([np.exp(-Delta_t/T2), np.pi/2, omega * Delta_t])
    Add_vector(ax11,
        start=[0,0,0], end=vec,
        lw=1.0, color=color_list[i], verbose=False
    )
    Add_vector(ax21,
        start=[0,0,0], end=vec,
        lw=1.0, color=color_list[i], verbose=False
    )
ax21.text(-1.4, -0.25, 0, '(2)', color='black')
addrotation(ax21)


# Delta_t + 180 deg pulse
ax22 = fig.add_subplot(gs[2, 2], projection='3d', azim=0, elev=90)
Init_0090sphere(
    ax22,
    verbose=False
    )
for i, omega in enumerate(omega_list) :
    vec = sph2orth1d([np.exp(-(1. * Delta_t + pulsedur)/T2), np.pi/2, omega * Delta_t])
    Add_vector(ax12,
        start=[0,0,0], end=vec,
        lw=1.0, color=color_list[i], alpha=.5
    )
    Add_vector(ax22,
        start=[0,0,0], end=vec,
        lw=1.0, color=color_list[i], alpha=.5
    )
timestamp = np.linspace(start=0, stop=pulsedur*0.9, num=1000)
magz = 0.5 * np.sin(np.pi * timestamp / pulsedur)
magx = -0.5 * np.cos(np.pi * timestamp / pulsedur)
magy = 0.5 * np.ones(magx.shape)
ax12.plot(xs=magx, ys=magy, \
    zs=magz, zdir='z', color='blue', lw=1.4, linestyle='--')
Add_vector(ax12,
        start=[magx[-2], magy[-2], magz[-2]], end=[magx[-1], magy[-1], magz[-1]],
        mutation_scale=15, lw=1.4, color='blue', alpha=1, zorder=0)

for i, omega in enumerate(omega_list):
    vec0 = sph2orth1d([np.exp(-(1. * Delta_t + pulsedur)/T2), np.pi/2, omega * Delta_t])
    vec = sph2orth1d([np.exp(-Delta_t/T2), np.pi/2, np.pi - omega * Delta_t])
    Add_vector(ax12,
        start=[0,0,0], end=vec,
        lw=1.0, color=color_list[i], verbose=False
    )
    Add_vector(ax22,
        start=[0,0,0], end=vec,
        lw=1.0, color=color_list[i], verbose=False
    )
    Add_vector(ax22,
        start=vec0, end=vec,
        mutation_scale=15, lw=0.99, color='blue', \
            alpha=0.5, zorder=0, linestyle='--')

ax22.text(-1.4, -0.25, 0, '(3)', color='black')
addrotation(ax22)


# 90 PULSE + Delta_t + 180 deg pulse + 0.8 * Delta_t
ax23 = fig.add_subplot(gs[2, 3], projection='3d', azim=0, elev=90)
Init_0090sphere(
    ax23,
    verbose=False
    )
for i, omega in enumerate(omega_list) :
    vec = sph2orth1d([np.exp(-(1.7 * Delta_t + pulsedur)/T2), np.pi/2, np.pi - omega * Delta_t * 0.3])
    Add_vector(ax13,
        start=[0,0,0], end=vec,
        lw=1.0, color=color_list[i], verbose=False
    )
    Add_vector(ax23,
        start=[0,0,0], end=vec,
        lw=1.0, color=color_list[i], verbose=False
    )
ax23.text(-1.4, -0.25, 0, '(4)', color='black')
addrotation(ax23)


# 90 PULSE + Delta_t + 180 deg pulse + Delta_t
ax24 = fig.add_subplot(gs[2, 4], projection='3d', azim=0, elev=90)
Init_0090sphere(
    ax24,
    verbose=False
    )

for i, omega in enumerate(omega_list) :
    vec = sph2orth1d([np.exp(-(2 * Delta_t + pulsedur)/T2), np.pi/2, np.pi])
    Add_vector(ax14,
        start=[0,0,0], end=vec,
        lw=0.6*(4.0-i), color=color_list[i], verbose=False
    )
    Add_vector(ax24,
        start=[0,0,0], end=vec,
        lw=0.6*(4.0-i), color=color_list[i], verbose=False
    )
ax24.text(-1.4, -0.25, 0, '(5)', color='black')
addrotation(ax24)


ax25 = fig.add_subplot(gs[2, 5], projection='3d', azim=0, elev=90)
Init_0090sphere(
    ax25,
    verbose=False
    )
for i, omega in enumerate(omega_list) :
    vec = sph2orth1d([np.exp(-(2.7 * Delta_t + pulsedur)/T2), np.pi/2, np.pi + omega * Delta_t * 0.7])
    Add_vector(ax15,
        start=[0,0,0], end=vec,
        lw=1.0, color=color_list[i], verbose=False
    )
    Add_vector(ax25,
        start=[0,0,0], end=vec,
        lw=1.0, color=color_list[i], verbose=False
    )
ax25.text(-1.4, -0.25, 0, '(6)', color='black')
addrotation(ax25)

# plt.tight_layout()
plt.savefig("tex/figures/spin_echo-schematic.pdf")
plt.savefig("tex/figures/spin_echo-schematic.png")
plt.show()
