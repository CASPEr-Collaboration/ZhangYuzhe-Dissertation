from src.dependency import *
from src.constants import *

m_a = 1 * unit.ueV / const.c**2
earth_pot = -const.G * unit.earthMass / unit.earthRad
earth_pot_10eV = np.abs(earth_pot * 10 * unit.eV / const.c**2).to(unit.eV)

print("ALP mass m_a (1 ueV):", m_a.to(unit.kg))
print("Earth mass M_E:", unit.earthMass.to(unit.kg))
print("Earth radius R_E:", unit.earthRad.to(unit.km))
print("Gravitational potential at surface G*M_E/R_E:", earth_pot.to(unit.MJ / unit.kg))
print("Gravitational binding energy for 10 eV/c^2 ALP:", earth_pot_10eV)

# escape velocity at Earth's surface: v_esc = sqrt(2 G M_E / R_E)
v_esc = np.sqrt(2 * const.G * unit.earthMass / unit.earthRad)
print("Escape velocity v_esc = sqrt(2 G M_E / R_E):", v_esc.to(unit.km / unit.s))

# maximum kinetic energy for a bound ALP: E_k = (1/2) m_a v_esc^2 = G M_E m_a / R_E
E_k_max = 0.5 * m_a * v_esc**2
print("Max kinetic energy of bound ALP (m_a = 1 ueV/c^2):", E_k_max.to(unit.eV))

v_a = (2 * earth_pot_10eV) / m_a
