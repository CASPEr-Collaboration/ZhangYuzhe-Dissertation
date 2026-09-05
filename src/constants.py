"""
Physical constants and unit conversion factors used throughout the axionbloch package.

Provides:
- Nuclear magneton helper ``mu_N``
- Proton and Xe-129 gyromagnetic ratios / magnetic moments
- ``AtomicUnits``: a namespace of conversion factors from SI to Hartree atomic units

All constants with units are astropy Quantity objects.
"""
from astropy import units as unit
from astropy.constants import codata2018 as const
from astropy.constants import Constant

def mu_N(m):
    """Return the nuclear magneton e*hbar / (2*m) for a nucleus of mass m."""
    return (const.e * const.hbar) / (2 * m)


# Magnetic dipole moment of proton
g_p = 5.585694713
I_p = 0.5 * const.hbar
mu_p = g_p * mu_N(const.m_p) * I_p / const.hbar

# Gyromagnetic ratio of proton
gamma_p = Constant(
    "gamma_p",
    "Proton gyromagnetic ratio",
    2.6752218708e8,
    "rad Hz / T",
    0.0000000011e8,
    reference="CODATA",
)


# Magnetic dipole moment of Xe nucleus
mu_Xe129 = -0.777969 * mu_N(const.m_p)

# Gyromagnetic ratio of Xe129
gamma_Xe129 = Constant(
    "gamma_Xe129",
    "Xe-129 gyromagnetic ratio",
    -7.451956e7,
    "rad Hz / T",
    0.000075e7,
    reference="https://doi.org/10.3390/magnetochemistry6040065",
)
