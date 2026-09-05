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

from src.dependency import *
# from src.utils import check, Lorentzian, Init_3020sphere, Init_0090sphere, Add_vector, sph2orth1d

T2 = 20.0
T2star = 0.1
Tdelta = 1.5

Delta_t = 0.1
pulsedur = .5
pulse_period = 5

nu = 4

# omega0 = 2 * np.pi / (0.2+0.02)
# omega1 = 0.86 * 2 * np.pi / (0.2+0.02)
# omega2 = 0.74 * 2 * np.pi / (0.2+0.02)
# omega3 = 0.62 * 2 * np.pi / (0.2+0.02)
# omega_list = [omega0, omega1, omega2, omega3]
# color_list = ['tab:red', 'tab:orange', 'tab:brown', 'tab:purple']

# plt.rc('font', size=12)
# plt.rcParams["font.family"] = "Times New Roman"
# # plt.rcParams["font.family"] = "serif"
# # plt.rcParams["font.serif"] = ["Times New Roman"]
# plt.rcParams["mathtext.fontset"] = 'cm'  # 'dejavuserif'

fig = plt.figure(figsize=(13 / 2.54, 13 / 2.54 * 3.5 / 8), dpi=300)
gs = gridspec.GridSpec(nrows=3, ncols=1, height_ratios=[1, 1, 4])
fig.subplots_adjust(top=0.97,
bottom=0.035,
left=0.035,
right=0.98,
hspace=0.0,
wspace=0.0)


ax = fig.add_subplot(gs[0,0])
extimestamp = np.linspace(start=16, stop=19, num=500)
# ax.plot(extimestamp, 3 * np.sin(2 * np.pi * nu * extimestamp), label='', color='blue', alpha=1, lw=1.2)
for i in np.arange(1, 12):
    ax.plot([pulse_period * i, pulse_period * i, pulse_period * i + pulsedur, pulse_period * i + pulsedur], \
        [0, 1, 1, 0], label='', color='blue', alpha=1, lw=1.2)
ax.plot([0, 0, pulsedur, pulsedur], [0, 0.5, .5, 0], label='', color='blue', alpha=1, lw=1.2)


ax.quiver([0], [0], [60], [0], \
    angles='xy', scale_units='xy', scale=1, color='black', \
        width=0.004)
ax.set_xlim(-1, 60)
ax.set_ylim(-1, 1.2)
ax.text(x=-1.5, y=.7,s='$\\pi/2$', color='blue')
ax.text(x=4.8, y=1.1,s='$\\pi$', color='blue')
ax.text(x=0, y=-0.7,s='Excitation coil')
ax.text(x=58, y=-.9,s='time')
ax.axis('off')
# ax.grid()


ax2 = fig.add_subplot(gs[1,0])
# ax2.arrow(x=0, y=0., dx=60, dy=0, width=0.005, head_width=1, head_length=1.4, color='black', \
#             edgecolor='none', length_includes_head=True, shape='full', )
ax2.quiver([0], \
    [0], [60], [0], \
    angles='xy', scale_units='xy', scale=1, color='black', \
        width=0.004)

tc_list = []
peakval_list = []
for i in np.arange(1, 12):
    ax.plot([pulse_period * i, pulse_period * i, pulse_period * i + pulsedur, pulse_period * i + pulsedur], \
        [0, 1, 1, 0], label='', color='blue', alpha=1, lw=1.2)
    
    pktimestamp = np.linspace(start=pulse_period * i + pulsedur+1, stop= pulse_period * i + pulse_period-1, num=1500)
    tc = np.mean(pktimestamp)
    pksignal = 3*np.exp(-(pktimestamp)/T2) * np.exp(-abs(pktimestamp - tc)/Tdelta) * np.cos(2 * np.pi * nu * (pktimestamp-tc))
    ax2.plot(pktimestamp, pksignal, label='', color='tab:blue', alpha=1, lw=1.2)
    ax2.scatter(tc, np.amax(pksignal) , color='tab:orange', marker='x', s=30,  alpha=1, zorder = 4)
    tc_list.append(tc)
    peakval_list.append(np.amax(pksignal))

# ax2.plot(pktimestamp, 2.4 * np.exp(-(pktimestamp-pktimestamp[0])/8), label='', color='tab:red', alpha=1, lw=1.2)
ax2.set_xlim(-1, 60)
ax2.set_ylim(-2.6, 2.6)
ax2.text(x=0, y=-1.6,s='Pickup coil')
# ax2.text(x=30, y=-2.4,s='$M_{xy} \\sim e^{-t/T_2} e^{-|t-t_c|/T_{\\delta}}\\cos(\\omega t + \\phi_0)$')
ax2.text(x=58, y=-1.99,s='time')
ax2.axis('off')
# ax2.grid()

T2_ax = fig.add_subplot(gs[2,0])
T2_ax.plot(tc_list, peakval_list , color='tab:orange', label='', alpha=1)
T2_ax.scatter(tc_list, peakval_list , color='tab:orange', marker='x', s=30,  alpha=1)
T2_ax.set_xlabel('Time')
T2_ax.set_ylabel('Peak value')

# T2_ax.set_xscale('log')
# T2_ax.set_yscale('log')
T2_ax.set_xlim(-1, 60)
T2_ax.set_ylim(-0.2, peakval_list[0]*1.2)
# T2_ax.set_xticks([])
# T2_ax.set_yticks([])
# T2_ax.grid()
# T2_ax.legend(bbox_to_anchor=(1.0, 1.0), loc='upper left')
T2_ax.axis('off')
T2_ax.quiver([0], [0], [0], [peakval_list[0]*1.12], \
    angles='xy', scale_units='xy', scale=1, color='black', \
        width=0.004)

T2_ax.quiver([0], [0], [60], [0], \
    angles='xy', scale_units='xy', scale=1, color='black', \
        width=0.004)
T2_ax.text(x=-2, y=peakval_list[0]/4, s='echo amplitude', rotation=90)
T2_ax.text(x=58, y=-.2,s='time')
T2_ax.text(x=30, y=peakval_list[0]/2, s='$\\sim e^{-t/T_2}$', rotation=0, color='tab:orange')
# plt.tight_layout()
plt.show()
