import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager

font_dir = "fonts"  # adjust if needed

# Add all .ttf or .TTF files
for file in os.listdir(font_dir):
    if file.lower().endswith(".ttf"):
        font_path = os.path.join(font_dir, file)
        font_manager.fontManager.addfont(font_path)

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["mathtext.fontset"] = "cm"  # optional, depends if you want math in Computer Modern

x = np.linspace(0, 10, 100)
y = np.sin(x)

# Set default font
plt.rcParams["font.serif"] = ["Times New Roman"]
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["mathtext.fontset"] = "cm"

plt.plot(x, y)
plt.title("Sine wave")
plt.savefig("figures/example-plot.png")
# plt.show()