from src.dependency import *
from axionbloch.EarthBoundAxionHalo import (
    PREM_density_profile,
    getCumulativeMass,
    earth_grav_potential_infty,
    earth_grav_potential_infty2,
)


radius_m, density_kg_m3 = PREM_density_profile()
density_r = radius_m * unit.meter
density_rho = density_kg_m3 * (unit.kg / unit.meter**3)
density_unit = unit.g / unit.cm**3

# cumulative mass
mass_r, mass_M_r = getCumulativeMass()

# Compare both potential conventions in the bottom panel.
Phi_func, r_unit, Phi_unit = earth_grav_potential_infty()
Phi_integral_func, integral_r_unit, integral_Phi_unit = (
    earth_grav_potential_infty2()
)
# extend to radii beyond Earth's surface
r_extended = np.linspace(0, 3, 1000) * unit.R_earth
Phi_extended = Phi_func(r_extended.to_value(r_unit)) * (Phi_unit)

Phi_integral_extended = (
    Phi_integral_func(r_extended.to_value(integral_r_unit)) * integral_Phi_unit
)

# use units for plotting:
r_unit = unit.R_earth
Phi_unit = unit.megajoule / unit.kilogram

# ------------- Plot ---------------------

cm = 1 / 2.54  # convert cm to inch

fig = plt.figure(figsize=(13.5 * cm, 6.5 * cm), dpi=300)  # initialize a figure

gs = gridspec.GridSpec(nrows=2, ncols=1)

# fix the margins
left = 0.336
bottom = 0.165
right = 0.686
top = 0.845
wspace = 0.2
hspace = 0.1
fig.subplots_adjust(
    left=left, top=top, right=right, bottom=bottom, wspace=wspace, hspace=hspace
)

density_ax = fig.add_subplot(gs[0, 0])
mass_ax = fig.add_subplot(gs[1, 0])

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


mass_ax.set_xlabel("Radius ($R_\\oplus$)")


# density
density_ax.set_ylim(-0.5, 15.5)


xlimits = (-.05, 1.05)
density_ax.set_xlim(xlimits)
mass_ax.set_xlim(xlimits)
density_ax.set_xticklabels([])
# mass_ax.set_xticklabels([])

# Show radius in km at the top of the density panel.
density_km_ax = density_ax.twiny()
density_km_ax.set_xlim(
    xlimits[0] * (1 * unit.R_earth).to_value(unit.km),
    xlimits[1] * (1 * unit.R_earth).to_value(unit.km),
)
density_km_ax.set_xlabel("Radius (km)")
# density_km_ax.tick_params(direction="in", pad=2)

fig.align_ylabels([density_ax, mass_ax])
# fig.tight_layout()
plt.savefig("tex/figures/PREM-density-enclosed_mass.pdf", transparent=False)
plt.savefig("tex/figures/PREM-density-enclosed_mass.png", transparent=False)
plt.show()
