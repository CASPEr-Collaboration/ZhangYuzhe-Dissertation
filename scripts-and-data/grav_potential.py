from src.dependency import *
from src.constants import *
from src.utils import check
m_a = 1 * unit.ueV / const.c**2
earth_pot = -const.G * unit.earthMass / unit.earthRad
check(m_a.to(unit.kg))
check(unit.earthMass.to(unit.kg))
check(unit.earthRad.to(unit.km))
check(earth_pot.to(unit.MJ / unit.kg))
check(np.abs(earth_pot * 10 * unit.eV / const.c**2).to(unit.eV))
