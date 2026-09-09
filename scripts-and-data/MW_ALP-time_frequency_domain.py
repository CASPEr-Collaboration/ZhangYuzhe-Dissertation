"""
Script to generate the time-domain and frequency-domain plots of the axion field, including stochastic variations in amplitude and phase. The script uses an inverse FFT method to simulate the time-series of the axion field based on a given lineshape and random variations.
The runtime of the script is approximately 1 minute, depending on the system performance and the number of samples used in the simulation.
Large RAM is recommended for efficient execution. 
"""
from src.dependency import *
from src.utils import axion_lineshape

from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset
from scipy.stats import uniform, expon
from scipy.interpolate import interp1d

plot_sin = True

total_dur = 20.0
samprate = 50
totalLen = int(total_dur * samprate)


nu_a = 1e6
# axion linewidth = 1
# coherence time = 1
tau_a = 1 / np.pi
frequencies = np.linspace(-25, 25, totalLen, endpoint=True)
lineshape = axion_lineshape(
    v_0=220e3,
    v_lab=233e3,
    nu_a=nu_a,
    nu=frequencies + nu_a,
    case="non-grad",
    alpha=0.0,
)
# for i in [0]:
# print(f'seed {i}')
rng = np.random.default_rng(seed=5)
rvs_amp = expon.rvs(loc=0.0, scale=1.0, size=totalLen, random_state=rng)
rvs_phase = np.exp(
    1j * uniform.rvs(loc=0, scale=2 * np.pi, size=totalLen, random_state=rng)
)

stoch_lineshape = lineshape * rvs_amp


# inverse FFT method
ax_FFT = stoch_lineshape * rvs_phase
# length = len(ax_FFT)
ax_FFT_pos_neg = connected = np.concatenate(
    [ax_FFT[totalLen // 2 :], ax_FFT[: totalLen // 2]]
)
# del length

axion_ts_complex = np.fft.ifft(ax_FFT_pos_neg)
axion_ts_envelope = np.abs(axion_ts_complex)
timeStamp = np.linspace(0, total_dur, num=totalLen)

newSampRate = np.ptp(timeStamp)
newTimeStamp = np.linspace(
    np.amin(timeStamp), np.amax(timeStamp), num=int(np.ptp(timeStamp) * 10 * nu_a)
)

f = interp1d(timeStamp, axion_ts_envelope, kind="linear", fill_value="interpolate")

axion_ts = f(newTimeStamp) * np.sin(2 * np.pi * nu_a * newTimeStamp)


cm = 1 / 2.56  # convert cm to inch
fig = plt.figure(
    figsize=(2 * 6.5 * cm, 5.0 * cm), dpi=300
)  # initialize a figure following APS journal requirements


gs = gridspec.GridSpec(nrows=1, ncols=2)  # create grid for multiple figures


# fix the margins
left = 0.05
bottom = 0.23
right = 0.977
top = 0.915
wspace = 0.15
hspace = 0.2
fig.subplots_adjust(
    left=left, top=top, right=right, bottom=bottom, wspace=wspace, hspace=hspace
)


ax00 = fig.add_subplot(gs[0, 0])
# ax00.plot(timestamp, np.real(ax_ts), label='signal real')
# ax00.plot(timestamp, np.imag(ax_ts), label='signal imaginary')
if not plot_sin:
    ax00.plot(timeStamp, np.abs(axion_ts_envelope))
if plot_sin:
    ax00.plot(newTimeStamp, axion_ts, label="")
ax00.set_xlabel("Time ($\\tau_a$)")
# ax00.set_xlabel("time ($\\Delta \\nu_a^{-1}$)")
ax00.set_ylabel("$a(t)\\, (\\mathrm{arb.\\,units})$")
# ax00.set_title('ALP time-series')
ybottom, ytop = ax00.get_ylim()
ax00.set_ylim(top=1.8 * ytop)
ax00.set_xticks(np.arange(0, 21, 5, dtype=int))
ax00.set_yticks([])
ax00.set_xticklabels(list(map(str, np.arange(0, 21, 5, dtype=int))))

if plot_sin:
    ax00_zoomin: Axes = inset_axes(
        ax00,  # parent axis
        bbox_to_anchor=(0.0, 0.0, 0.5, 1),  # (x0, y0, width, height)
        width="50%",
        height="30%",  # the dimensions of the inset plot
        loc="upper right",  # location in the bounding box
        # position x0, y0) and size (width, height) of the bounding box
        bbox_transform=ax00.transAxes,
        borderpad=0.5,  # padding (safe distance) around the inset plot
    )
    ax00_zoomin.plot(
        newTimeStamp[0 : int(1e-5 * 10 * nu_a)], axion_ts[0 : int(1e-5 * 10 * nu_a)]
    )
    ax00_zoomin.set_xticks([0, 1e-5])
    ax00_zoomin.set_yticks([])
    ax00_zoomin.set_xticklabels(["0", "$10^{-5}$"])
    # Draw rectangle and connecting lines
    mark_inset(ax00, ax00_zoomin, loc1=2, loc2=4, fc="none", ec="0.0", linewidth=0.5)
    # ax_inset.plot(timeStamp[0 : int(samprate * 1)], np.real(ts[0 : int(samprate * 1)]))
    # ax_inset.plot(timeStamp[0 : int(samprate * 1)], np.imag(ts[0 : int(samprate * 1)]))

# ax00.set_xlim(-0.5, 10.5)
# ax00.set_ylim(min(np.amin(np.real(ax_ts)), np.amin(np.imag(ax_ts))), 0.017)
# ax00.legend(loc="upper left")

ax01 = fig.add_subplot(gs[0, 1])

ax01.plot(frequencies, stoch_lineshape, color="tab:green", label="Stochastic lineshape")
ax01.plot(frequencies, lineshape, "--", color="tab:red", label="Average lineshape")
ax01.set_xlabel("Frequency$\\,-\\,\\nu_a$ ($\\Delta \\nu_a$)")
ax01.set_ylabel("$\\left|\\mathrm{FT}[a(t)]\\right|^2\\, (\\mathrm{arb.\\,units})$")
# ax01.set_title('Pulsed-NMR Signal Amplitude')
ax01.set_xlim(-0.5, 3.5)
ax01.set_yticks([])
ax01.set_xticks(np.arange(0, 4, 1, dtype=int))
ax01.set_xticklabels(list(map(str, np.arange(0, 4, 1, dtype=int))))
ax01.legend(loc="upper right", frameon=False)

for i, ax in enumerate([ax00, ax01]):
    # ax.tick_params(axis='y', which='both', pad=3)  # For y-axis ticks
    ax.tick_params(axis="x", which="both", pad=3)  # For x-axis ticks

if plot_sin:
    ax00_zoomin.tick_params(axis="x", which="both", pad=3)  # For x-axis ticks

# put figure index
letters = ["(a)", "(b)", "(c)", "(d)", "(e)", "(f)", "(g)", "(h)", "(i)"]
for i, ax in enumerate([ax00, ax01]):
    # xleft, xright = ax.get_xlim()
    # ybottom, ytop = ax.get_ylim()
    ax.text(
        -0.013,
        1.02,
        s=letters[i],
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        color="k",
    )
# ha = 'left' or 'right'
# va = 'top' or 'bottom'

# fig.tight_layout()
plt.savefig("tex/figures/MW_ALP-time_frequency_domain.png")
plt.savefig("tex/figures/MW_ALP-time_frequency_domain.pdf")
# plt.show()
