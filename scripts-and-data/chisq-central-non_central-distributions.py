from src.dependency import *
from scipy.stats import norm, chi2, ncx2

# parameters for chi-sq distribution
df = 2  # degree of freedom
sigma = np.sqrt(2.0 * df)  # standard deviation

# find p value > 5 sigma in normal distribution
pvalueNorm5sigma = norm.sf(5.0, loc=0, scale=1.0)

# find what p=2.87e-7 corresponds to in terms of signal significance
# in normal and chi2 (d.o.f.=2) distribution
print(norm.isf(pvalueNorm5sigma))
print(chi2.isf(pvalueNorm5sigma, df=2) / sigma)  # this value is 15.064998393988729

# assign the nc value with isf
nc = chi2.isf(pvalueNorm5sigma, df=2)

# find the 95% rescan threshold
rescan_thres = ncx2.ppf(0.05, df, nc)
print(f"rescan_thres = {rescan_thres}")


fig = plt.figure(figsize=(13 / 2.54, 5.2 / 2.54), dpi=300)  # initialize a figure
gs = gridspec.GridSpec(nrows=1, ncols=1)  # create grid for multiple figures
# fix the margins
left = 0.235
bottom = 0.22
right = 0.618
top = 0.958
wspace = 0.24
hspace = 0.114
fig.subplots_adjust(
    left=left, top=top, right=right, bottom=bottom, wspace=wspace, hspace=hspace
)
# left=
# bottom=
# right=
# top=
# wspace=
# hspace=


ax = fig.add_subplot(gs[0, 0])

x = np.linspace(0.0, 50.0, 1000)
x_sn95 = np.linspace(rescan_thres, np.amax(x), 1000)


# ax00.fill_between(
#     x_sn_95,
#     pdf_sn_95,
#     alpha=1,
#     color="lightgrey",
#     label=f"$>3.355\\,\\sigma$ range\n$P=${norm.sf(3.355146373048527*sigma, mu_sn, sigma):.2g}",
# )

# ax00.fill_between(
#     x_n_sn95,
#     pdf_n_sn95,
#     facecolor="lightgrey",
#     hatch="//",
#     label=f"False alarm rate\n$P=${norm.sf(3.355146373048527*sigma, mu_noise, sigma):.4f}",
# )

nc = 0.0
# mean, var, skew, kurt = ncx2.stats(df, nc, moments='mvsk')
noise_pdf = ncx2.pdf(x, df, nc)
noise_pdf_sn95 = ncx2.pdf(x_sn95, df, nc)


nc = 2 * 15.064998393988729
# mean, var, skew, kurt = ncx2.stats(df, nc, moments='mvsk')
signal_pdf = ncx2.pdf(x, df, nc)
signal_pdf_sn95 = ncx2.pdf(x_sn95, df, nc)

ax.plot(x / sigma, noise_pdf, label="Noise")
ax.plot(
    x / sigma,
    signal_pdf,
    label="Signal + Noise",
)


ax.fill_between(
    x_sn95 / sigma,
    signal_pdf_sn95,
    alpha=1,
    color="lightgrey",
    label="$>7.809\\,\\sigma$ range\n"
    + f"$P=${ncx2.sf(rescan_thres, df, 2 * 15.064998393988729):.2f}",
)

ax.fill_between(
    x_sn95 / sigma,
    noise_pdf_sn95,
    facecolor="lightgrey",
    hatch="//",
    label="$>7.809\\,\\sigma$ range\n" + f"$P=${ncx2.sf(rescan_thres, df, 0.0):.1g}",
)

# ax.set_xlim([x[0], x[-1]])
# ax.legend(loc='best', frameon=False)
ax.set_yscale("log")

# Add labels and legend
ax.set_xlabel("$x\\,(\\sigma$)")
ax.set_ylabel("PDF")
ax.legend(bbox_to_anchor=(1.0, 1.0))

ax.set_ylim(bottom=np.amin(ncx2.pdf(x, df, nc)))

# Show the plot
# fig.tight_layout()

plt.savefig(
    "tex/figures/chisq-central-non_central-distributions.png", transparent=False
)
plt.savefig(
    "tex/figures/chisq-central-non_central-distributions.pdf", transparent=False
)

plt.show()
