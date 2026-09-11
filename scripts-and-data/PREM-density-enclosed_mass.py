from src.dependency import *
from axionbloch.EarthBoundAxionHalo import (
    PREM_density_profile,
    getCumulativeMass,
)


radius_m, density_kg_m3 = PREM_density_profile()
density_r = radius_m * unit.meter
density_rho = density_kg_m3 * (unit.kg / unit.meter**3)
density_unit = unit.g / unit.cm**3

# cumulative mass
mass_r, mass_M_r = getCumulativeMass()

# Acceleration magnitude, with the regular central limit g(0)=0.
gravity = np.zeros(mass_r.shape) * unit.m / unit.s**2
nonzero_radius = mass_r > 0 * unit.m
gravity[nonzero_radius] = (
    const.G * mass_M_r[nonzero_radius] / mass_r[nonzero_radius]**2
)
surface_g = const.G * mass_M_r[-1] / mass_r[-1]**2
uniform_g = surface_g * mass_r / mass_r[-1]
assert np.all(np.isfinite(gravity)) and np.all(gravity >= 0 * unit.m / unit.s**2)
assert gravity.max() > surface_g
print(f'Surface g: {surface_g.to(unit.m / unit.s**2):.4f}; '
      f'maximum g: {gravity.max():.4f} at {mass_r[gravity.argmax()].to(unit.km):.1f}')

# use units for plotting:
r_unit = unit.R_earth
gravity_unit = unit.m / unit.s**2

# ------------- Plot ---------------------

cm = 1 / 2.54  # convert cm to inch

fig = plt.figure(figsize=(13. * cm, 10.5 * cm), dpi=300)  # initialize a figure

gs = gridspec.GridSpec(nrows=3, ncols=1)

# fix the margins
left = 0.235
bottom = 0.11
right = 0.817
top = 0.90
wspace = 0.2
hspace = 0.1
fig.subplots_adjust(
    left=left, top=top, right=right, bottom=bottom, wspace=wspace, hspace=hspace
)

density_ax = fig.add_subplot(gs[0, 0])
mass_ax = fig.add_subplot(gs[1, 0])
gravity_ax = fig.add_subplot(gs[2, 0])

# density profile
density_ax.plot(
    density_r.to_value(r_unit),
    density_rho.to_value(density_unit),
    label="Density Profile",
    color="darkblue",
)
density_ax.set_ylabel("$\\rho_\\oplus \\,(\\mathrm{g}\\,\\mathrm{cm}^{-3})$")

# cumulative mass
mass_ax.plot(
    mass_r.to_value(r_unit),
    mass_M_r.to_value(unit.kg) / 1e24,
    label="Mass Profile",
    color="darkgreen",
)
mass_ax.set_ylabel("$M_\\mathrm{enclosed}(10^{24}\\,\\mathrm{kg})$")
mass_ax.ticklabel_format(useOffset=False)


gravity_ax.plot(mass_r.to_value(r_unit), gravity.to_value(gravity_unit), color="darkred", label="PREM")
gravity_ax.plot(mass_r.to_value(r_unit), uniform_g.to_value(gravity_unit), "--", color="0.5", label="Uniform density")
gravity_ax.set_ylabel("$g\\, (\\mathrm{m}\,\\mathrm{s}^{-2})$")
gravity_ax.set_xlabel("Radius ($R_\\oplus$)")
gravity_ax.set_ylim(-0.4, 12)
gravity_ax.legend(loc="lower right", frameon=False, fontsize=7)


# density
density_ax.set_ylim(-0.5, 15.5)


xlimits = (-.05, 1.05)
density_ax.set_xlim(xlimits)
mass_ax.set_xlim(xlimits)
gravity_ax.set_xlim(xlimits)
density_ax.set_xticklabels([])
mass_ax.set_xticklabels([])

# Show radius in km at the top of the density panel.
density_km_ax = density_ax.twiny()
density_km_ax.set_xlim(
    xlimits[0] * (1 * unit.R_earth).to_value(unit.km),
    xlimits[1] * (1 * unit.R_earth).to_value(unit.km),
)
density_km_ax.set_xlabel("Radius (km)")
# density_km_ax.tick_params(direction="in", pad=2)

fig.align_ylabels([density_ax, mass_ax, gravity_ax])
# fig.tight_layout()
plt.savefig("tex/figures/PREM-density-enclosed_mass.pdf", transparent=False)
plt.savefig("tex/figures/PREM-density-enclosed_mass.png", transparent=False)

plt.show()
