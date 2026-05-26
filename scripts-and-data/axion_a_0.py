from src.dependency import *
from src.constants import *

rho_E_DM = 0.4 * unit.GeV / (unit.cm**3)
m_a = 1 * unit.ueV / const.c**2
a_0_KimballOverview: Quantity = np.sqrt(
    rho_E_DM * 2 * const.hbar**3 / (const.c * m_a**2)
)
a_0_Gramolin: Quantity = const.hbar * np.sqrt(rho_E_DM * 2) / (const.c * m_a)

print(a_0_KimballOverview.si)
print(a_0_Gramolin.si)
