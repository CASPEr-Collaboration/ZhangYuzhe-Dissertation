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

# use units for plotting:
r_unit = unit.R_earth
Phi_unit = unit.megajoule / unit.kilogram

# extend to radii beyond Earth's surface
r_extended = np.linspace(0, 20, 4000) * unit.R_earth
Phi_extended = Phi_func(r_extended.to_value(r_unit)) * (Phi_unit)

Phi_integral_extended = (
    Phi_integral_func(r_extended.to_value(integral_r_unit)) * integral_Phi_unit
)


# ------------- Plot ---------------------

cm = 1 / 2.54  # convert cm to inch

fig = plt.figure(figsize=(13.5 * cm, 5. * cm), dpi=300)  # initialize a figure

gs = gridspec.GridSpec(nrows=1, ncols=1)

# fix the margins
left = 0.15
bottom = 0.213
right = 0.865
top = 0.798
wspace = 0.2
hspace = 0.1
fig.subplots_adjust(
    left=left, top=top, right=right, bottom=bottom, wspace=wspace, hspace=hspace
)

pot_ax = fig.add_subplot(gs[0, 0])

# gravitational potential
(infinity_line,) = pot_ax.plot(
    r_extended.to_value(r_unit),
    Phi_extended.to_value(Phi_unit),
    # label="",
    color="darkorange",
    linestyle="-",
    # zorder=8,
)

pot_ax.set_xlabel("Radius ($R_\\oplus$)")
# pot_ax.set_ylabel("Grav. Pot. (MJ/kg) ref. to $\\infty$")
pot_ax.set_ylabel(
    "$\\Phi_\\oplus\\, (\\mathrm{MJ}\\,\\mathrm{kg}^{-1}$)"
)

# potential
ylimits = (-130, 5)
pot_ax.set_ylim(ylimits)


xlimits = (-0.1, 10.1)
pot_ax.set_xlim(xlimits)

# Show radius in km at the top of the density panel.
pot_km_ax = pot_ax.twiny()
pot_km_ax.set_xlim(
    xlimits[0] * (1 * r_unit).to_value(unit.km),
    xlimits[1] * (1 * r_unit).to_value(unit.km),
)
pot_km_ax.set_xlabel("Radius (km)")

# show potential as km^2/s^2 on the right y-axis
Phi_unit2 = 1e6 * unit.m**2 / unit.s**2
print("1 MJ/kg = ", (1 * Phi_unit).to(Phi_unit2))
pot_kms2_ax = pot_ax.twinx()
pot_kms2_ax.set_ylim(
    ylimits[0] * (1 * Phi_unit).to_value(Phi_unit2),
    ylimits[1] * (1 * Phi_unit).to_value(Phi_unit2),
)
pot_kms2_ax.set_ylabel("$\\Phi_\\oplus\\,(10^6\\mathrm{m}^2/\\mathrm{s}^2$)")
pot_ax.set_yticks([-125, -100, -75, -50, -25, 0])

plt.savefig("tex/figures/PREM-Earth_grav_potential.pdf", transparent=False)
plt.savefig("tex/figures/PREM-Earth_grav_potential.png", transparent=False)

plt.show()
