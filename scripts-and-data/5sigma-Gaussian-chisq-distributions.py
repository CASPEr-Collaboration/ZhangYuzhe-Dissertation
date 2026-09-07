from src.dependency import *
from scipy.stats import norm, chi2

fig = plt.figure(figsize=(13 / 2.54, 5.5 / 2.54), dpi=300)  # initialize a figure
gs = gridspec.GridSpec(nrows=1, ncols=2)  # create grid for multiple figures

Gaussian_ax = fig.add_subplot(gs[0, 0])
chisq_ax = fig.add_subplot(gs[0, 1])

# fix the margins
left = 0.105
bottom = 0.206
right = 0.964
top = 0.88
wspace = 0.327
hspace = 0.237
fig.subplots_adjust(
    left=left, top=top, right=right, bottom=bottom, wspace=wspace, hspace=hspace
)

# ------------------------------------------


# Define the mean and standard deviation
mu = 0
sigma = 1

# Generate x values
x = np.linspace(mu - 6 * sigma, mu + 6 * sigma, 1000)

# print(f">10-sigma range: Probability={norm.sf(10*sigma, mu, sigma):.2e}")
# Calculate the PDF
Gaussian_pdf = norm.pdf(x, mu, sigma)


x_5sigma = np.linspace(mu + 5 * sigma, np.amax(x), 1000)

Gaussian_pdf_5sigma = norm.pdf(x_5sigma, mu, sigma)

Gaussian_ax.plot(x, Gaussian_pdf)

Gaussian_ax.fill_between(
    x_5sigma,
    Gaussian_pdf_5sigma,
    alpha=0.2,
    color="red",
    label="$>5\\,\\sigma$ range\n$P=2.87\\times 10^{-7}$",
)

# Add labels and legend
Gaussian_ax.set_xlabel("$x\\,(\\sigma)$")
Gaussian_ax.set_ylabel("PDF")
Gaussian_ax.legend()
Gaussian_ax.set_xlim(np.amin(x), np.amax(x))

Gaussian_ax.set_yscale("log")
Gaussian_ax.set_title("(a) Gaussian distribution")

# ------------------------------------------


sigma = np.sqrt(2 * 2)

# Generate x values
x = np.linspace(0, 35, 1000)

# Calculate the PDF
chisq_pdf = chi2.pdf(x, df=2)


x_5sigma = np.linspace(5 * sigma, np.amax(x), 1000)
x_15sigma = np.linspace(15.064998393988729 * sigma, np.amax(x), 1000)


chisq_pdf_5sigma = chi2.pdf(x_5sigma, df=2)
chisq_pdf_15sigma = chi2.pdf(x_15sigma, df=2)

pvalueNorm5sigma = norm.sf(5, 0, 1)
print(norm.isf(pvalueNorm5sigma) / 1.0)
print(chi2.isf(pvalueNorm5sigma, df=2) / sigma)

chisq_ax.plot(x / sigma, chisq_pdf)

chisq_ax.fill_between(
    x_5sigma / sigma,
    chisq_pdf_5sigma,
    alpha=0.2,
    color="red",
    label="$>5\\,\\sigma$ range\n$P=6.74\\times 10^{-3}$",
)
chisq_ax.fill_between(
    x_15sigma / sigma,
    chisq_pdf_15sigma,
    alpha=1,
    color="tab:green",
    label="$>15.06\\,\\sigma$ range\n$P=2.87\\times 10^{-7}$",
)

# Add labels and legend
chisq_ax.set_xlabel("$x \\, (\\sigma)$")
chisq_ax.set_ylabel("PDF")
chisq_ax.legend()

chisq_ax.set_yscale("log")

chisq_ax.set_xlim(np.amin(x) / sigma, np.amax(x) / sigma)
chisq_ax.set_title("(b) $\\chi^2_2$ distribution")

# plt.tight_layout()

plt.savefig("tex/figures/5sigma-Gaussian-chisq-distributions.png", transparent=False)
plt.savefig("tex/figures/5sigma-Gaussian-chisq-distributions.pdf", transparent=False)

# Show the plot
plt.show()
