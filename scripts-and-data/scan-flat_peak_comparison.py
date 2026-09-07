from src.dependency import np, plt, gridspec
from matplotlib.patches import Ellipse
from scipy.stats import norm

from src.utils import get_FWHMin, check, Exclusion


def Lorentzian(x, center, FWHM, area, offset):
    """
    Return the value of the Lorentzian function
        offset + 0.5*FWHM*area / (np.pi * ( (x-center)**2 + (0.5*FWHM)**2 )      )

                           FWHM A
        offset + ───────────────────────
                  2π ((x-c)^2+(FWHM/2)^2 )

    Parameters
    ----------

    x : scalar or array_like
        argument of the Lorentzian function
    center : scalar
        the position of the Lorentzian peak
    FWHM : scalar
        full width of half maximum (FWHM) / linewidth of the Lorentzian peak
    area : scalar
        area under the Lorentzian curve (without taking offset into consideration)
    offset : scalar
        offset for the curve


    Returns
    -------
    the value of the Lorentzian function : ndarray or scalar

    Examples
    --------
    >>>

    Reference
    ----------
    Null

    """
    return offset + 0.5 * FWHM * area / (
        np.pi * ((x - center) ** 2 + (0.5 * FWHM) ** 2)
    )


# data
freqstamp = np.linspace(1.0e6 - 200, 1.0e6 + 200, num=600)
freqstamp_list = []

gainFWHM = 20
# Lorzlin = Lorentzian(x=freqstamp, center=np.mean(freqstamp), FWHM=FWHM, area=1e-3, offset=1e-6)
gain = Lorentzian(
    x=freqstamp, center=np.mean(freqstamp), FWHM=gainFWHM, area=1, offset=1e-8
)
noise_flat_envo = Lorentzian(
    x=freqstamp, center=np.mean(freqstamp), FWHM=10 * gainFWHM, area=3e1, offset=1e-2
)
noise_peak_envo = Lorentzian(
    x=freqstamp, center=np.mean(freqstamp), FWHM=1 * gainFWHM, area=1e1, offset=1e-2
)
rand_noise0 = norm.rvs(loc=0, scale=1.0, size=len(freqstamp), random_state=None)
rand_noise1 = norm.rvs(loc=0, scale=1.0, size=len(freqstamp), random_state=None)
# PSD_noise = norm.rvs(loc=0, scale=1e-1*np.sqrt(np.amax(Lorzlin)), size=len(freqstamp), random_state=None) ** 2
# NMR_decayspectrum = Lorzlin + PSD_noise
# Axion_sensitivity = 1e-12 * 1. / np.sqrt(NMR_decayspectrum)

cm = 1 / 2.56  # convert cm to inch
fig = plt.figure(
    figsize=(2 * 6.5 * cm, 2 * 6.5 * cm / 6.0 * 3.5), dpi=300
)  # initialize a figure following APS journal requirements
# fig = plt.figure(figsize=(6., 4.), dpi=300)  # initialize a figure
# fig = plt.figure(figsize=(6., 3.5), dpi=300)  # initialize a figure

# gs = gridspec.GridSpec(nrows=3, ncols=2)  # create grid for multiple figures

# to specify heights and widths of subfigures
width_ratios = [1, 1]
height_ratios = [0.7, 1, 1]
gs = gridspec.GridSpec(
    nrows=3, ncols=2, width_ratios=width_ratios, height_ratios=height_ratios
)  # create grid for multiple figures

# fix the margins
left = 0.105
bottom = 0.159
right = 0.921
top = 0.93
wspace = 0.175
hspace = 0.36
fig.subplots_adjust(
    left=left, top=top, right=right, bottom=bottom, wspace=wspace, hspace=hspace
)

# ax00 = fig.add_subplot(gs[0,0])  # Gain
# ax10 = fig.add_subplot(gs[1,0], sharex=ax00)  # Noise
# ax20 = fig.add_subplot(gs[2,0], sharex=ax00)  # sensitivity
# ax01 = fig.add_subplot(gs[0,1], sharex=ax00, sharey=ax00)  # Gain
# ax11 = fig.add_subplot(gs[1,1], sharex=ax01)  # Noise
# ax21 = fig.add_subplot(gs[2,1], sharex=ax01)  # sensitivity

ax00 = fig.add_subplot(gs[0, 0])  # Gain
ax10 = fig.add_subplot(gs[1, 0])  # Noise
ax20 = fig.add_subplot(gs[2, 0])  # sensitivity
ax01 = fig.add_subplot(gs[0, 1], sharey=ax00)  # Gain
ax11 = fig.add_subplot(gs[1, 1])  # Noise
ax21 = fig.add_subplot(gs[2, 1])  # sensitivity

# # Add a solid black line between columns
# line = Line2D([0.525, 0.525], [0.02, 0.97], transform=fig.transFigure, color="black", linewidth=2)
# fig.add_artist(line)

# Create a line with varying width
# n_points = 10000
# x = np.linspace(0.525, 0.525, n_points)
# y = np.linspace(0.02, 0.97, n_points)
# linewidths = 1 * np.sin(np.pi * y)**2 + 1  # Line width varies like a bell curve
# segments = [[[x[i], y[i]], [x[i+1], y[i+1]]] for i in range(n_points - 1)]
# lc = LineCollection(segments, linewidths=linewidths, color="black", transform=fig.transFigure)
# fig.add_artist(lc)

# Add an ellipse between the left and right columns
ellipse = Ellipse(
    (0.514, 0.5),  # (x, y) position in figure coordinates
    width=0.0031,  # Width of the ellipse
    height=0.95,  # Height of the ellipse
    edgecolor="black",
    facecolor="black",
    linewidth=0.01,
    alpha=1,
)

# Add the ellipse to the figure
ellipse.set_transform(fig.transFigure)
fig.add_artist(ellipse)


def plotOneColumn(
    axGain, axNoise, axSensi, freq, center, gainFWHM, noiseFWHM, noise_mean
):
    # plot gain
    gain = Lorentzian(x=freq, center=center, FWHM=gainFWHM, area=1, offset=1e-8)
    axGain.plot(
        freq,
        gain,
        label="Signal gain",
        linewidth=0.9,
        color="tab:blue",
        alpha=1,
        linestyle="-",
    )
    axGain.set_xticks([])
    axGain.set_yticks([])

    # plot noise
    noise_envo = Lorentzian(
        x=freq, center=center, FWHM=noiseFWHM, area=1e1, offset=1e-2
    )

    # axNoise.fill_between(freq, noise_envo+noise_mean, -noise_envo+noise_mean, \
    #             color = 'k', alpha=0.2, zorder=6)
    noise = np.abs(norm.rvs(loc=0, scale=1.0, size=len(freq), random_state=None)) ** 2
    axNoise.plot(
        freq,
        noise_envo * noise + noise_mean,
        label="Noise",
        color="k",
        alpha=1,
        linestyle="-",
        linewidth=0.7,
    )
    # axNoise.set_ylim(top=2.5*np.amax(noise_cruv_envo), bottom=-2.5*np.amax(noise_cruv_envo))
    axNoise.set_xticks([])
    axNoise.set_yticks([])

    # plot sensitivity
    SNR = gain / noise_envo
    sensi = np.sqrt(SNR)
    exclusion = 1.0 / sensi
    # check(get_FWHMin(freq, exclusion))
    # check(get_FWHMin(freq, SNR))
    sensiBW = get_FWHMin(freq, exclusion)
    # sensiBW = get_FWHMin(freq, SNR)

    def SNR_function(freq, gainFWHM, noiseFWHM):
        center = np.mean(freq)
        # Gain and noise envelope Lorentzian calculations
        gain = Lorentzian(x=freq, center=center, FWHM=gainFWHM, area=1, offset=1e-8)
        noise_envo = Lorentzian(
            x=freq, center=center, FWHM=noiseFWHM, area=1e1, offset=1e-2
        )
        # SNR calculation
        return gain / noise_envo

    meas_dict = {"SNR": SNR_function}
    # exclusion.addMeas(meas_dict)

    axSensi.plot(
        freq,
        exclusion,
        label="Exclusion",
        color="tab:green",
        alpha=1,
        linestyle="-",
        linewidth=0.9,
        zorder=6,
    )
    top = 3.1 * np.amin(exclusion)
    axSensi.fill_between(freq, exclusion, top, color="tab:green", alpha=0.2, zorder=6)
    # axSensi.quiver([np.mean(freq), np.mean(freq)], \
    #                [2. * np.amin(exclusion), 2. * np.amin(exclusion)], \
    #                 [0.5*sensiBW, -0.5*sensiBW], [0, 0], \
    #         angles='xy', scale_units='xy', scale=1, color='black', \
    #             width=0.005)
    # axSensi.hlines(y=2. * np.amin(exclusion), xmin=np.amin(freq), xmax=np.amax(freq))
    # check(np.amin(exclusion))
    # axSensi.set_yscale('log')
    # axSensi.set_yticks([1. * np.amin(exclusion), 2. * np.amin(exclusion)])
    axSensi.set_yticks([])

    axSensi.set_ylim(top=top)
    # axSensi.set_xticks([])
    # axSensi.set_yticks([])
    axSensi.set_xlabel("Frequency")

    return sensiBW, np.amin(exclusion), SNR


def plotExclusion(axSensi, freq, exclusion):
    axSensi.plot(
        freq,
        exclusion,
        label="Exclusion",
        color="tab:red",
        alpha=1,
        linestyle="-",
        linewidth=0.9,
        zorder=10,
    )
    top = 3.1 * np.amin(exclusion)
    axSensi.fill_between(freq, exclusion, top, color="tab:green", alpha=0.2, zorder=6)
    # axSensi.quiver([np.mean(freq), np.mean(freq)], \
    #                [2. * np.amin(exclusion), 2. * np.amin(exclusion)], \
    #                 [0.5*sensiBW, -0.5*sensiBW], [0, 0], \
    #         angles='xy', scale_units='xy', scale=1, color='black', \
    #             width=0.005)
    # axSensi.hlines(y=2. * np.amin(exclusion), xmin=np.amin(freq), xmax=np.amax(freq))
    # check(np.amin(exclusion))
    # axSensi.set_yscale('log')
    # axSensi.set_yticks([1. * np.amin(exclusion), 2. * np.amin(exclusion)])
    axSensi.set_yticks([])
    # ax.set_title('')
    # ax.set_xscale('log')

    # ax.set_xlim(left=, right=)
    # axSensi.set_ylim(top=top)
    # axSensi.set_xticks([])
    # axSensi.set_yticks([])
    # axSensi.set_xlabel('Frequency')


# plot flat-noise scenario
freqstamp_flat = np.linspace(1.0e6 - 50, 1.0e6 + 50, num=200) - 108
sensiBW_flat, exc_flat_min, SNR = plotOneColumn(
    ax00,
    ax10,
    ax20,
    freqstamp_flat,
    np.mean(freqstamp_flat),
    gainFWHM,
    10 * gainFWHM,
    0,
)
check(sensiBW_flat)
numofflatspec = 12  # number of flat spectra

exclusion_flat = Exclusion(
    nu_start=freqstamp[0], nu_end=freqstamp_flat[-1] + (numofflatspec) * sensiBW_flat
)
exclusion_flat.updateExc_SNR(
    freq_arr=freqstamp_flat,
    SNR=SNR,
)
for i in range(numofflatspec):
    freq = freqstamp_flat + (i + 1) * sensiBW_flat / 1
    a, b, SNR = plotOneColumn(
        ax00, ax10, ax20, freq, np.mean(freq), gainFWHM, 10 * gainFWHM, -(i + 1) / 2
    )
    exclusion_flat.updateExc_SNR(
        freq_arr=freq,
        SNR=SNR,
    )


# plot peak-noise scenario
freqstamp_peak = np.linspace(1.0e6 - 150, 1.0e6 + 200, num=600)


sensiBW_peak, exc_peak_min, SNR = plotOneColumn(
    ax01, ax11, ax21, freqstamp_peak, 1.0e6, gainFWHM, 1 * gainFWHM, 0
)
# check(sensiBW_peak)
freqstamp_peak_1 = np.linspace(
    1.0e6 + sensiBW_peak - 200, 1.0e6 + sensiBW_peak + 150, num=600
)

exclusion_peak = Exclusion(nu_start=freqstamp_peak[0], nu_end=freqstamp_peak_1[-1])
exclusion_peak.updateExc_SNR(
    freq_arr=freqstamp_peak,
    SNR=SNR,
)
a, b, SNR = plotOneColumn(
    ax01, ax11, ax21, freqstamp_peak_1, 1.0e6 + sensiBW_peak, gainFWHM, 1 * gainFWHM, -4
)
exclusion_peak.updateExc_SNR(
    freq_arr=freqstamp_peak_1,
    SNR=SNR,
)

plotExclusion(ax20, exclusion_flat.frequencies, exclusion_flat.gaNNexc)
plotExclusion(ax21, exclusion_peak.frequencies, exclusion_peak.gaNNexc)

# set same x lim for two columns
ax21.set_xlim(
    np.amin(freqstamp_peak), 1.0e6 + sensiBW_peak + abs(1.0e6 - np.amin(freqstamp_peak))
)
xlim_left, xlim_right = ax21.get_xlim()
ax20.set_xlim(xlim_left, xlim_right)

#  set x axis labels
for ax in [ax00, ax01, ax10, ax11]:
    ax.set_xlim(xlim_left, xlim_right)
    ax.set_xticks([xlim_left, xlim_right])
    ax.set_xticklabels(("", ""))

#  set x axis labels
for ax in [ax20, ax21]:
    ax.set_xlim(xlim_left, xlim_right)
    ax.set_xticks([xlim_left, xlim_right])
    ax.set_xticklabels(("$\\nu_{0}$", "$\\nu_{1}$"))


ax10.set_ylim(top=1)

# set y lim for ax21
ylim_bottom, ylim_up = ax21.get_ylim()
ax21.set_ylim(bottom=ylim_bottom * 0.5)

# # set y tick labels
# ax20.set_yticklabels(('$\\mathrm{g}_{\\mathrm{min}}^{\\mathrm{flat}}$', '$2\,\\mathrm{g}_{\\mathrm{min}}^{\\mathrm{flat}}$'))
# ax21.set_yticklabels(('$\\mathrm{g}_{\\mathrm{min}}^{\\mathrm{peak}}$', '$2\,\\mathrm{g}_{\\mathrm{min}}^{\\mathrm{peak}}$'))

# draw two horizontal lines
# ax20.hlines(
#     y=[1.0 * exc_flat_min],
#     xmin=xlim_left,
#     xmax=xlim_right,
#     color="b",
#     linestyles="dotted",
#     linewidth=1,
# )
# ax20.hlines(
#     y=[2.0 * exc_flat_min],
#     xmin=xlim_left,
#     xmax=xlim_right,
#     color="k",
#     linestyles="dashed",
#     linewidth=1,
# )

# ax21.hlines(
#     y=[1.0 * exc_peak_min],
#     xmin=xlim_left,
#     xmax=xlim_right,
#     color="b",
#     linestyles="dotted",
#     linewidth=1,
# )
# ax21.hlines(
#     y=[2.0 * exc_peak_min],
#     xmin=xlim_left,
#     xmax=xlim_right,
#     color="k",
#     linestyles="dashed",
#     linewidth=1,
# )

# title
# fig.suptitle('Flat v.s. peak noise & sensitivity', wrap=True)


# put figure index
letters = ["(a)", "(b)", "(c)", "(d)", "(e)", "(f)", "(g)", "(h)", "(i)"]
for i, ax in enumerate([ax00, ax10, ax20, ax01, ax11, ax21]):
    xleft, xright = ax.get_xlim()
    ybottom, ytop = ax.get_ylim()
    ax.text(x=xleft, y=1.03 * ytop, s=letters[i], ha="left", va="bottom", color="k")

# set y labels
# ax00.set_ylabel('Transfer                    \nfunction                    ', rotation=0, color='tab:blue')
# ax10.set_ylabel('Noise        ', rotation=0, color='k')
# ax20.set_ylabel('$|g_{\\mathrm{a}}|$              \nsensitivity               ', rotation=0, color='tab:green')

# ax00.set_ylabel('Transfer\nfunction', color='tab:blue')
ax00.set_ylabel("$\\eta^2(\\nu)$", color="k")
ax10.set_ylabel("Noise", color="k")
ax20.set_ylabel("$|g_{\\mathrm{a}}|$ sensitivity", color="k")
# labels = ['Transfer function', 'Noise', '$|g_{\\mathrm{a}}|$\nsensitivity']
# for i, ax in enumerate([ax00, ax10, ax20]):
#     xleft, xright = ax.get_xlim()
#     ybottom, ytop = ax.get_ylim()
#     ax.text(x=xleft, y=ytop/2, s = labels[i], ha='right', va = 'center', color='k')

# plt.tight_layout()
plt.savefig("tex/figures/scan-flat_peak_sensi.png", transparent=False)
plt.savefig("tex/figures/scan-flat_peak_sensi.pdf", transparent=False)
plt.show()

# colors from Piet Cornelies Mondrian
# RGB
# red 212 1 0
# orange 242 141 2
# light grey 233 226 228
# mid grey 173 189 201
# black 0 0 0
# blue 20 17 93
# yellow 252 215 7
# purple 56 63 131
# dark blue 0 13 47

# dark color list
# 'Dark2'
#
