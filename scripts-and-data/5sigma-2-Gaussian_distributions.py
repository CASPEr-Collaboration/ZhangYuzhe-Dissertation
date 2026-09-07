from src.dependency import *
from src.constants import *

from scipy.stats import norm

# Define the mean and standard deviation
mu_noise = 0.0
sigma = 1.0
mu_sn = 5.0 * sigma

# Generate x values
x_noise = np.linspace(mu_noise - 6 * sigma, mu_noise + 6 * sigma, 1000)
x_sn = np.linspace(mu_sn - 6 * sigma, mu_sn + 6 * sigma, 1000)

# Calculate the PDF
pdf_noise = norm.pdf(x_noise, mu_noise, sigma)
pdf_sn = norm.pdf(x_sn, mu_sn, sigma)

print(norm.ppf(0.05, loc=5 * sigma, scale=sigma))


x_n_sn95 = np.linspace(mu_noise + 3.355146373048527 * sigma, np.amax(x_noise), 1000)
x_sn_95 = np.linspace(mu_noise + 3.355146373048527 * sigma, np.amax(x_sn), 1000)

pdf_n_sn95 = norm.pdf(x_n_sn95, mu_noise, sigma)
pdf_sn_95 = norm.pdf(x_sn_95, mu_sn, sigma)

fig = plt.figure(
    figsize=(13 / 2.54, 5.5 / 2.54), dpi=300
)  # initialize a figure
gs = gridspec.GridSpec(nrows=1, ncols=1)  # create grid for multiple figures
# fix the margins
left=0.222
bottom=0.202
right=0.624
top=0.983
wspace=0.24
hspace=0.114
fig.subplots_adjust(left=left, top=top, right=right,
                    bottom=bottom, wspace=wspace, hspace=hspace)
# left=
# bottom=
# right=
# top=
# wspace=
# hspace=

ax00 = fig.add_subplot(gs[0, 0])
ax00.plot(x_noise, pdf_noise, label="Noise")
ax00.plot(x_sn, pdf_sn, label="Signal + Noise")


ax00.fill_between(
    x_sn_95,
    pdf_sn_95,
    alpha=1,
    color="lightgrey",
    label=f"$>3.355\\,\\sigma$ range\n$P=${norm.sf(3.355146373048527*sigma, mu_sn, sigma):.2g}",
)

ax00.fill_between(
    x_n_sn95,
    pdf_n_sn95,
    facecolor="lightgrey",
    hatch="//",
    label=f"False alarm rate\n$P=${norm.sf(3.355146373048527*sigma, mu_noise, sigma):.4f}",
)

# Add labels and legend
ax00.set_xlabel("$x\\,(\\sigma$)")
ax00.set_ylabel("PDF")
ax00.legend(bbox_to_anchor=(1.0, 1.0))
ax00.set_xlim(np.amin(x_noise), np.amax(x_sn))
ax00.set_ylim(bottom=np.amin(pdf_sn))
ax00.set_yscale("log")
ax00.set_xticks(range(-6, 12, 2))
ax00.set_xticklabels([f"{x:d}" for x in range(-6, 12, 2)])
# fig.suptitle("Normal Distribution Probability Density")
ax00.set_ylim(top=2)

# fig.tight_layout()
# 5sigma-2-Gaussian_distributions.py
plt.savefig("tex/figures/5sigma-2-Gaussian_distributions.png", transparent=False)
plt.savefig("tex/figures/5sigma-2-Gaussian_distributions.pdf", transparent=False)

plt.show()
