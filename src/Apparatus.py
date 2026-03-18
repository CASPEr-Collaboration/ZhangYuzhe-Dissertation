# $env:PYTHONPATH = "C:\Users\zhenf\D\Yu0702\CASPEr-Collaboration\ZhangYuzhe-Dissertation\src;$env:PYTHONPATH”
# src/Apparatus.py
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from functools import partial

from typing import Optional, Callable

from scipy.integrate import quad

from src.enphylope import PhysicalQuantity as PQ
from src.constants import (
    gamma_p,
    gamma_Xe129,
    mol_to_num,
    mu_p,
    mu_Xe129,
    hbar,
    c,
    mu_0,
    kB,
)

from src.utils import PhysicalObject, Lorentzian, check
from src.Sample import Sample, liquid_Xe129, methanol, ethanol


class Magnet(PhysicalObject):

    def __init__(
        self,
        name=None,
        B0: Optional[PQ] = None,
        FWHM: Optional[PQ] = None,
        numPt: float = 1,
        nFWHM: float = 10.0,
        verbose: bool = False,
    ):
        """
        name : str
            name of the SQUID. default to 'PhiC6L1W'. 'PhiC73L1' is the other option
        """
        super().__init__()

        self.name = name
        assert nFWHM >= 0
        self.nFWHM = nFWHM
        self.B0 = B0
        self.FWHM = FWHM
        self.B0_nW = self.nFWHM * self.FWHM * self.B0
        self.numPt = numPt
        self.FWHM_T = (self.B0 * self.FWHM).value_in("T")
        # Specify all physical quantities with units
        self.physicalQuantities = {"B0": "T", "FWHM": "", "B0_nW": "T"}
        # Specify general quantities
        self.generalQuantities = {"numPt": "float", "nFWHM": "float", "FWHM_T": "float"}
        # make sure that we use common units for quantities
        self.useCommonUnits()
        self.setHomogeneity()

    def setHomogeneity(
        self,
        # lineshape:str = "Lorentizan",
        numPt: int | float = None,
        showplt: bool = False,
        verbose: bool = False,
    ):
        """
        set the homogeneity sampling using ...some complicated methods
        """
        # update self.numPt if
        if numPt is not None:
            self.numPt = max(1, int(numPt))
        elif self.numPt is None:
            self.numPt = 1

        # FWHM_T = (self.B0 * self.FWHM).value_in("T")
        if self.numPt == 1 or self.FWHM_T == 0.0 or self.nFWHM == 0:
            self.B_vals_T = np.array([self.B0.value_in("T")])
            self.ratios = np.array([1.0])
        else:
            pdf = partial(
                Lorentzian,
                center=self.B0.value_in("T"),
                FWHM=self.FWHM_T,
                area=1,
                offset=0,
            )

            u = np.linspace(start=-1, stop=1, num=self.numPt, endpoint=True)
            self.B_vals_T = (
                self.nFWHM * np.sign(u) * np.abs(u) ** 2
            ) * self.FWHM_T + self.B0.value_in(
                "T"
            )  # exponent < 1 increases central density
            if showplt:
                fig = plt.figure(figsize=(6.0, 4.0), dpi=150)  # initialize a figure
                gs = gridspec.GridSpec(
                    nrows=1, ncols=1
                )  # create grid for multiple figures
                ax00 = fig.add_subplot(gs[0, 0])
                hist, bin_edges = np.histogram(self.B_vals_T)
                # for i, count in enumerate(hist):
                #     if count > 0:
                #         ax00.scatter(bin_edges[i+1], count, color='goldenrod', edgecolors='darkgoldenrod', linewidths=0.8, marker='o', s=2, zorder=6)
                ax00.plot(
                    (bin_edges[1:] - self.B0.value_in("T")) / self.FWHM_T,
                    hist,
                    label="",
                )
                ax00.set_xlabel("Magnetic field - B0 (FWHM)")
                ax00.set_ylabel("Number of data points")
                plt.tight_layout()
                # plt.savefig('example figure - one-column.png', transparent=False)
                plt.show()

            # Define interval edges (midpoints between adjacent x's)
            edges = np.zeros(len(self.B_vals_T) + 1)
            edges[1:-1] = (self.B_vals_T[:-1] + self.B_vals_T[1:]) / 2
            edges[0] = -np.inf
            edges[-1] = np.inf

            self.ratios = np.zeros_like(self.B_vals_T)
            for i in range(len(self.B_vals_T)):
                a, b = edges[i], edges[i + 1]
                self.ratios[i], _ = quad(pdf, a, b)

            if showplt:
                fig = plt.figure(figsize=(6.0, 4.0), dpi=150)  # initialize a figure
                gs = gridspec.GridSpec(
                    nrows=1, ncols=1
                )  # create grid for multiple figures
                ax00 = fig.add_subplot(gs[0, 0])

                ax00.plot(self.B_vals_T, self.ratios, label="")
                ax00.set_xlabel("")
                ax00.set_ylabel("")
                # ax00.set_xscale('log')
                # ax00.set_yscale('log')
                ax00.legend()
                plt.tight_layout()
                # plt.savefig('example figure - one-column.png', transparent=False)
                plt.show()

            self.ratios /= np.sum(self.ratios)


class Gradiometer(PhysicalObject):

    def __init__(
        self,
        name=None,
        R: Optional[PQ] = None,
        H_side: Optional[PQ] = None,
        H_center: Optional[PQ] = None,
        H_gap: Optional[PQ] = None,
        verbose: bool = False,
    ):
        """
        name : str
            name of the SQUID. default to 'PhiC6L1W'. 'PhiC73L1' is the other option
        """
        super().__init__()

        self.name = name
        self.R = R
        self.H_side = H_side
        self.H_center = H_center
        self.H_gap = H_gap

        # Specify all physical quantities with units
        self.physicalQuantities = {
            "R": "mm",
            "H_side": "mm",
            "H_center": "mm",
            "H_gap": "mm",
        }
        # Specify general quantities
        self.generalQuantities = {}
        # make sure that we use common units for quantities
        self.useCommonUnits()


class CylinderSampleHolder(PhysicalObject):

    def __init__(
        self,
        name=None,
        R: Optional[PQ] = None,
        H: Optional[PQ] = None,
        verbose: bool = False,
    ):
        """
        name : str
            name of the SQUID. default to 'PhiC6L1W'. 'PhiC73L1' is the other option
        """
        super().__init__()

        self.name = name
        self.R = R
        self.H = H

        # Specify all physical quantities with units
        self.physicalQuantities = {
            "R": "mm",
            "H": "mm",
        }
        # Specify general quantities
        self.generalQuantities = {}
        # make sure that we use common units for quantities
        self.useCommonUnits()
        self.getVolume()

    def getVolume(
        self,
    ):
        self.vol = (np.pi * self.R**2 * self.H).to("cm**3")
        return self.vol


class SphereSampleHolder(PhysicalObject):

    def __init__(
        self,
        name=None,
        R: Optional[PQ] = None,
        verbose: bool = False,
    ):
        """
        name : str
            name of the SQUID. default to 'PhiC6L1W'. 'PhiC73L1' is the other option
        """
        super().__init__()

        self.name = name
        self.R = R
        # Specify all physical quantities with units
        self.physicalQuantities = {
            "R": "mm",
        }
        # Specify general quantities
        self.generalQuantities = {}
        # make sure that we use common units for quantities
        self.useCommonUnits()
        self.getVolume()

    def getVolume(
        self,
    ):
        self.vol = (4.0 / 3.0 * np.pi * self.R**3).to("cm**3")
        return self.vol


gradiometer14mm = Gradiometer(
    name="gradiometer14mm",
    R=PQ(14, "mm"),
    H_side=PQ(12, "mm"),
    H_center=PQ(24, "mm"),
    H_gap=PQ(2, "mm"),
)

cylinder = CylinderSampleHolder(
    name="cylindrical sample holder", R=PQ(4, "mm"), H=PQ(24, "mm")
)

sphere = SphereSampleHolder(
    name="spherical sample holder",
    R=PQ(4, "mm"),
)


class SQUID(PhysicalObject):

    def __init__(
        self,
        name=None,
        R: Optional[PQ] = None,
        verbose: bool = False,
    ):
        """
        name : str
            name of the SQUID. default to 'PhiC6L1W'. 'PhiC73L1' is the other option
        """
        super().__init__()

        self.name = name


# the system of CASPEr-G lowfield setup
class CASPErGLF:
    def __init__(
        self,
        name="CASPEr-G Lowfield system",
        sample: Sample = None,
        sampleHolder:CylinderSampleHolder|SphereSampleHolder=None,
        pickup: Gradiometer = None,
        squid: SQUID = None,
        B0_max=PQ(0.1, "tesla"),
        rho_E_DM=PQ(0.3, "GeV / cm**3"),
        va=PQ(220, "km / s"),
    ):
        self.name = name
        self.sample = sample
        self.sampleHolder=sampleHolder
        self.pickup = pickup
        self.squid = squid
        #
        self.B0_max = B0_max
        self.rho_E_DM = rho_E_DM
        self.rho_M_DM = rho_E_DM  # / c**2
        self.Q_a = PQ(10**6, "")
        self.nu_lowlimit = PQ(1, "kHz")
        self.va = va

    def sampleMethanol(
        self,
    ):
        # Methanol properites
        rho_M_Methanol = PQ(0.792, "g / cm**3 ")
        molmassMethanol = PQ(32.04, "g / mol")
        rho_N_MethanolProton = (
            PQ(4.0, "") * rho_M_Methanol / molmassMethanol * mol_to_num
        )

        self.sample = "Methanol"

        self.ns = rho_N_MethanolProton.convert_to("1 / cm**3")
        self.ns_SPN = PQ((self.ns.value) ** 0.5, " 1 / cm**3 ")
        # check(ns)
        # self.T2 = PQ(1, 's')
        self.gamma = gamma_p
        self.nu_uplimit = self.gamma * self.B0_max / (2 * np.pi)
        self.mu = mu_p

    def sampleLXe129(self, abundance: PQ = PQ(100, "%")):
        # Xe properites
        rho_M_LXe = PQ(3.1, "g / cm**3 ")
        molmassLXe = PQ(131.29, "g / mol")
        rho_N_LXe129 = abundance * 1 * rho_M_LXe / molmassLXe * mol_to_num
        # check(abundance.convert_to('%'))
        # print(rhoN_MethanolProton.convert_to("1 / cm ** 3"))

        self.sample = "LXe129"
        self.ns = rho_N_LXe129.convert_to(" 1 / cm**3 ")
        self.ns_SPN = PQ(np.sqrt(self.ns.value), " 1 / cm**3 ")
        # check(ns)
        self.gamma = ((gamma_Xe129) ** 2) ** (1 / 2)
        # check(self.gamma)
        self.nu_uplimit = self.gamma * self.B0_max / (2 * np.pi)
        self.mu = mu_Xe129
        self.T2 = PQ(1000, "s")

    def sampleLXe129_approx(self, abundance: PQ = PQ(100, "%")):
        # Xe properites
        # rho_M_LXe = PQ(3.1, "g / cm**3 ")
        # molmassLXe = PQ(131.29, "g / mol")
        # rho_N_LXe129 = abundance * 1 * rho_M_LXe / molmassLXe * mol_to_num
        # check(abundance.convert_to('%'))
        # print(rhoN_MethanolProton.convert_to("1 / cm ** 3"))

        self.sample = "LXe129"
        self.ns = PQ(1e22, " 1 / cm**3 ")
        self.ns_SPN = PQ(np.sqrt(self.ns.value), " 1 / cm**3 ")
        # check(ns)
        self.gamma = ((gamma_Xe129) ** 2) ** (1 / 2)
        # check(self.gamma)
        self.nu_uplimit = self.gamma * self.B0_max / (2 * np.pi)
        self.mu = mu_Xe129
        self.T2 = PQ(1000, "s")

    def GetT2(
        self,
        nu: PQ,
    ):
        nu = nu.convert_to("Hz")
        if self.sample == "Methanol":
            return PQ(1, "s")
        elif self.sample == "LXe129":
            return PQ(1000, "s")

    def NMR_lw_Hz(
        self,
        NMR_lw_ppm: PQ,
        nu: PQ,
    ):
        return (nu * NMR_lw_ppm).convert_to("Hz")

    def GetTdelta(
        self,
        NMR_lw_ppm: PQ,
        nu: PQ,
    ):
        return (1 / (np.pi * self.NMR_lw_Hz(NMR_lw_ppm, nu))).convert_to("s")

    def GetT2star(
        self,
        NMR_lw_ppm: PQ,
        nu: PQ,
    ):
        T2star = (self.GetT2(nu) ** (-1) + self.GetTdelta(NMR_lw_ppm, nu) ** (-1)) ** (
            -1
        )
        return T2star.convert_to("s")

    def getThermalPol(
        self,
        # nu_L:PQ,
        B_pol: PQ,
        Temp: PQ,
    ):
        pol = hbar * self.gamma * B_pol / (2 * kB * Temp)
        # pol = hbar * (2 * np.pi * nu_L) / ( 2 * k * Temp)
        # self.p = p.convert_to('')
        pol = pol.convert_to("")
        # check(pol)
        return pol

    def getM0(
        self,
        pol,
        ns,
    ):
        """
        compute magnetization M0
        """
        M0 = (self.mu * pol * ns).convert_to("A/m")
        # self.M0_SPN = (mu_p * ns_SPN).convert_to("A/m")
        return M0

    def getPhi_pick(
        self,
        M0: PQ,
        gV: PQ = PQ(
            37.0, "1/m"
        ),  # estimated from a  cylindrical sample (R=4 mm, H=22.53 mm) coupling to the gradiometer
        Vol: PQ = PQ(np.pi * 4.0**2 * 24, "mm**3"),
    ):
        """
        get the flux in the np.pickup coil (gradiometer)
        """
        Phi_pick = gV * mu_0 * M0 * Vol
        Phi_pick = Phi_pick.convert_to("Phi_0")
        return Phi_pick

    def getM2Pick(
        self,
        gV: PQ = PQ(
            37.0, "1/m"
        ),  # estimated from a  cylindrical sample (R=4 mm, H=22.53 mm) coupling to the gradiometer
        Vol: PQ = PQ(np.pi * 4.0**2 * 24, "mm**3"),
    ):
        """ """
        return gV

    def getPick2In(
        self,
        # defaults are properties of SQUID C649_G12 for DM measurement 2022.12.14 and 12.23
        Lin=PQ(400, "nH"),
        Lpick=PQ(553, "nH"),
        Min=PQ(1 / 0.5194, "Phi_0/microA"),
    ):
        """
        input coupling
        considering np.pickup-SQUID coupling
        """
        # check(Mf.convert_to('Phi_0 / mA'))
        # check(Min.convert_to('nH'))

        # coupling between Phi_pick and Phi_in
        np.pick2in = Min / (Lpick + Lin)
        np.pick2in = np.pick2in.convert_to("")
        # check(np.pick2in)
        return np.pick2in

    def getIn2Vf(
        self,
        # defaults are properties of SQUID C649_G12 for DM measurement 2022.12.14 and 12.23
        Lin=PQ(400, "nH"),
        Lpick=PQ(553, "nH"),
        Mf=PQ(1 / 43.803, "Phi_0 / microA"),
        Min=PQ(1 / 0.5194, "Phi_0/microA"),
        Rf=PQ(3, "kiloohm"),
    ):
        """
        input coupling
        considering np.pickup-SQUID coupling
        """
        # check(Mf.convert_to('Phi_0 / mA'))
        # check(Min.convert_to('nH'))

        # coupling between V_f and Phi_in
        in2Vf = Rf / Mf * Min / (Lpick + Lin)
        in2Vf = in2Vf.convert_to("V/Phi_0")

        return in2Vf

    # def useLF_Magnet(
    #     self,
    # ):
    #     self.B0_max = PQ(0.1, "tesla")

    # def useHF_Magnet(
    #     self,
    # ):
    #     self.B0_max = PQ(14.1, "tesla")

    def useShims(
        self,
        NMR_lw_ppm: PQ,
    ):
        self.NMR_lw_ppm = NMR_lw_ppm

    def getOmega_a(self, alpha=PQ(np.pi / 2, "rad")):
        """
        ALP field Rabi frequency Omega_a at gaNN = self.gaNN_base
        """

        alpha = alpha.convert_to("rad")
        # self.gaNN_base = PQ(1, "GeV**(-1)")
        self.gaNN_base = PQ(1.1e-13, "eV**(-1)")

        Omega_a = (
            1
            / 2.0
            * self.gaNN_base
            * (2.0 * hbar * c * self.rho_E_DM) ** (1 / 2)
            * self.va
            * np.sin(alpha.value)
        )
        Omega_a = Omega_a.convert_to("Hz")
        # check(gaNN)
        # check(sin(alpha.value))
        # check(Omega_a / (2 * np.pi))
        return Omega_a

    def getTipAngle(
        self,
        Omega_a: PQ,
        T2: PQ,
        tau_a: PQ,
    ):
        angle = Omega_a * T2 * (tau_a / (T2 + tau_a)) ** 0.5
        angle = angle.convert_to("rad")
        # check(sin(angle.value))
        return angle

    def getSpecFac(
        self,
        nu_L: PQ,
        nu_a: PQ,
        T2: PQ,
        Tdelta: PQ,
        tau_a: PQ,
    ):
        Delta2 = (tau_a) ** (-1)
        Delta3 = (T2) ** (-1) + (Tdelta) ** (-1)
        # u = (
        #     Delta2
        #     / Delta3
        #     * (PQ(1, "") + (nu_L - nu_a) ** 2 / (Delta3 / 2) ** 2) ** (-1)
        # )
        u = Delta2 / Delta3
        u = u.convert_to("")
        return u

    def getPSDnoise_SQUID(self, nu: PQ):
        noise = PQ(1e-12, "Phi_0 ** 2 / Hz")
        return noise

    def getPower_sig(
        self,
        gin: PQ,
        M0: PQ,
        vol: PQ,
        u: PQ,
        tipAngle: PQ,
    ) -> PQ:
        Phi_in_pito2 = gin * mu_0 * M0 * vol
        power_sig = 1.0 / 2 * (u * Phi_in_pito2) ** 2.0 * tipAngle**2
        power_sig = power_sig.convert_to("Phi_0**2")
        return power_sig

    def getPower_SPN(
        self,
        gin: PQ,
        M_SPN: PQ,
        vol: PQ,
    ) -> PQ:
        Phi_in_SPN = gin * mu_0 * M_SPN * vol
        power_SPN = 1.0 / 2 * (Phi_in_SPN) ** 2.0
        power_SPN = power_SPN.convert_to("Phi_0**2")
        return power_SPN.convert_to("Phi_0**2")

    def getPSD_SPN(self, power: PQ, Delta: PQ) -> PQ:
        PSD_SPN = power / Delta
        PSD_SPN = PSD_SPN.convert_to("Phi_0**2 / Hz")
        return PSD_SPN

    def getPowerNoise_MF(
        self,
        PSDnoise_SQUID: PQ,
        power_SPN: PQ,
        # nu:PQ,
        ALP_lw_Hz: PQ,
        Tmeas: PQ,
        T2star: PQ,
        verbose: bool = False,
    ) -> PQ:
        """
        Noise in the spectrum after matched filtering
        """
        # assume long measurement time
        assert (Tmeas - 1 / ALP_lw_Hz).convert_to("s").value >= 0
        PSDnoise_SPN = self.getPSD_SPN(power=power_SPN, Delta=1 / (np.pi * T2star))
        PSDnoise = (PSDnoise_SQUID**2 + PSDnoise_SPN**2) ** 0.5
        Navg = (ALP_lw_Hz * Tmeas).convert_to("")
        RBW = 1 / Tmeas
        if (Tmeas - T2star).value < 0:
            # measurement time is shorter than T2star
            # RBW boarder than
            powerNoise_MF = RBW * (PSDnoise_SQUID**2 + (power_SPN / RBW) ** 2) ** 0.5
        elif Navg.value < 1:
            # measurement time is longer than T2star
            # but shorter than 1 / ALP_lw_Hz
            # matched filtering cannot be applied
            powerNoise_MF = RBW * PSDnoise
        else:
            # measurement time is longer than 1 / ALP_lw_Hz
            # matched filtering can be applied
            powerNoise_MF = PSDnoise * PQ(1, "Hz") / Navg**0.5

        powerNoise_MF = powerNoise_MF.convert_to("Phi_0**2")

        if verbose:
            check((Tmeas - T2star).convert_to("s"))
            check(Navg)
            check(powerNoise_MF)

        return powerNoise_MF

    def getEfficPow(
        self,
        # nu:PQ,
        RBW_Hz: PQ,  # resolution bandwidth
        ALP_lw_Hz: PQ,
        SG_effic=PQ(100, "%"),
    ):
        """
        analysis efficiency for signal power
        """
        assert RBW_Hz.value > 0
        assert RBW_Hz.value > 0
        assert SG_effic.value > 0
        # ALP_lw_Hz = ALP_lw_Hz.convert_to("Hz")
        # RBW_Hz = RBW_Hz.convert_to("Hz")
        # check(ALP_lw_Hz.value)
        # check(RBW_Hz.value)
        effici = PQ(100, "%")
        effici *= SG_effic
        if (RBW_Hz - ALP_lw_Hz).value > 0:
            effici *= PQ(1, "") - 0.5 * ALP_lw_Hz / RBW_Hz

        effici = effici.convert_to("")
        return effici

    def getThermMethanol_Sensi(
        self,
        freq_list: list[PQ],  # frequencies [Hz]
        Tmeas_list: list[PQ],
        verbose: bool = False,
    ) -> list[PQ]:
        """
        gaNN sensitivity with a thermally-polarized methanol sample

        compute SNR for gaNN = 1 GeV^-1, so as to estimate the gaNN limit
        """
        # if np.amin(freq)<1e3 or np.amax(freq) > 4.3

        # get self.sample, self.ns, self.ns_SPN
        self.sampleMethanol()  #

        # set inhomogeneity
        self.useShims(PQ(10, "ppm"))

        # temperature
        temp = PQ(273.15 - 90, "K")

        # sensitivity at nu_a
        def sensi(
            nu_a: PQ,  # frequency [Hz]
            Tmeas: PQ,  # frequencies [Hz]
            # eta:PQ
        ) -> PQ:
            ALP_lw_Hz = nu_a / self.Q_a
            # check(ALP_lw_Hz)
            tau_a = (1 / (np.pi * ALP_lw_Hz)).convert_to("s")

            nu_a = nu_a.convert_to("Hz")
            self.nu_uplimit = self.nu_uplimit.convert_to("Hz")
            nu_L = nu_a if (nu_a - self.nu_uplimit).value <= 0 else self.nu_uplimit

            T2 = self.GetT2(nu_L)
            # check(T2)
            Tdelta = self.GetTdelta(NMR_lw_ppm=self.NMR_lw_ppm, nu=nu_L)
            # check(Tdelta)
            T2star = ((T2) ** (-1) + (Tdelta) ** (-1)) ** (-1)

            # Phi np.pi/2

            gin = self.getPick2In() * self.getM2Pick()
            pol = self.getThermalPol(B_pol=2 * np.pi * nu_L / self.gamma, Temp=temp)
            u = self.getSpecFac(
                nu_L=nu_a, nu_a=nu_a, T2=self.GetT2(nu_L), Tdelta=Tdelta, tau_a=tau_a
            )
            tipAngle = self.getTipAngle(Omega_a=self.getOmega_a(), T2=T2, tau_a=tau_a)
            vol = PQ(1.2, "cm**3")
            power_sig = self.getPower_sig(
                gin=gin,
                M0=self.getM0(pol, ns=self.ns),
                vol=vol,
                u=u,
                tipAngle=self.getTipAngle(
                    Omega_a=self.getOmega_a(), T2=T2, tau_a=tau_a
                ),
            )
            check(power_sig)

            power_SPN = self.getPower_SPN(
                gin=gin,
                M_SPN=self.getM0(pol=PQ(1, ""), ns=self.ns_SPN),
                vol=vol,
            )
            PSD_SPN = self.getPSD_SPN(power=power_SPN, Delta=1 / (np.pi * T2star))
            # check(nu_L)
            # check((SPN_PSDnoise**0.5).convert_to('microPhi_0 / Hz**0.5'))

            eta = self.getEfficPow(RBW_Hz=1 / Tmeas, ALP_lw_Hz=ALP_lw_Hz)

            # check(ALP_lw_Hz)
            powerNoise_MF = self.getPowerNoise_MF(
                # PSDnoise_SQUID=self.getPSDnoise_SQUID(nu=nu_a),
                PSDnoise_SQUID=PQ(4e-11, "Phi_0**2/Hz"),
                power_SPN=power_SPN,
                ALP_lw_Hz=ALP_lw_Hz,
                Tmeas=Tmeas,
                T2star=T2star,
                verbose=True,
            )

            glim = (5 * powerNoise_MF / (eta * power_sig)) ** 0.5 * self.gaNN_base
            # check((powerNoise_MF))
            # check(eta)
            # check(P_perp)
            glim = glim.convert_to("GeV**(-1)")
            if verbose:
                print("**************************")
                check(nu_a)
                check(tau_a)
                check(T2)
                check(T2star)
                check(Tmeas)
                check(gin)
                check(self.getPick2In())
                check(self.getM2Pick())
                check(pol)
                check(u)
                check(tipAngle)
                check(eta)
                check(powerNoise_MF)
                check(glim)
            return glim

        glim_list = []
        for i, freq in enumerate(freq_list):
            glim_list.append(sensi(freq, Tmeas_list[i]))

        return glim_list

    def plotThermMethanol_Sensi(
        self,
        ax: plt.Axes,
        freq_list: list[PQ],  # frequencies [Hz]
        Tmeas_list: list[PQ],
        verbose: bool = False,
    ):
        """
        gaNN sensitivity with a thermally-polarized methanol

        compute SNR for gaNN = 1 GeV^-1, so as to estimate the gaNN limit
        """
        glim_list = self.getThermMethanol_Sensi(freq_list, Tmeas_list, verbose=verbose)
        glim_vals = []
        freq_vals = []
        for glim in glim_list:
            # assert isinstance(glim, PQ), "glim is not a PQ"
            glim = glim.convert_to("GeV**(-1)")
            glim_vals.append(glim.value)
        for freq in freq_list:
            # assert isinstance(glim, PQ), "glim is not a PQ"
            freq = freq.convert_to("Hz")
            freq_vals.append(freq.value)

        glim_vals = np.array(glim_vals)
        freq_vals = np.array(freq_vals)

        # check(np.amin(freq))  # 1348562.406998
        # freq0 = 1348560
        top = 1e-0
        ax.fill_between(
            x=freq_vals,
            y1=glim_vals,
            y2=top,
            color="tab:green",
            edgecolor="k",
            linewidth=0.5,
            alpha=0.5,
            zorder=2,
        )

        # ax.set_xlim(0, 53)
        # ax.set_ylim(1e-10, 1e-2)

        ax.set_xscale("log")
        # ax.set_yscale('linear')
        # ax.set_xscale('log')
        ax.set_yscale("log")

        ax.set_xticks([1e3, 1e4, 1e5, 1e6, 4.3e6])
        # xticklabels = []
        # for freq in freq_vals:
        #     xticklabels.append(f'{}')
        ax.set_xticklabels(["1 kHz", "10 kHz", "100 kHz", "1 MHz", "4.3 MHz"])
        # ax.set_yticks([1e-2, 1e-4, 1e-6, 1e-8, 1e-10])
        # ax.set_yticklabels([1, 10, 100, 1000])
        # ax.set_ylim(bottom=0.1)
        # ax.legend(loc='upper right')
        ax.grid(True)

        ax.set_xlabel(f"Frequency")
        ax.set_ylabel("$|g_\\mathrm{aNN}| [\\mathrm{GeV}^{-1}]$ ", color="k")

        return

    def getXe129_Sensi_Phase1(
        self,
        freq_list: list[PQ],  # frequencies [Hz]
        Tmeas_list: list[PQ],
        verbose: bool = False,
    ) -> list[PQ]:
        """
        gaNN sensitivity with a thermally-polarized methanol

        compute SNR for gaNN = 1 GeV^-1, so as to estimate the gaNN limit
        """
        # if np.amin(freq)<1e3 or np.amax(freq) > 4.3

        # get self.sample, self.ns, self.ns_SPN
        self.sampleLXe129()  #
        vol = PQ(1.2, "cm**3")

        # set inhomogeneity
        self.useShims(PQ(2, "ppm"))

        # temperature
        # temp = PQ(273.15 - 90, "K")

        # sensitivity at nu_a
        def sensi(
            nu_a: PQ,  # frequency [Hz]
            Tmeas: PQ,  # frequencies [Hz]
            # eta:PQ
        ) -> PQ:
            ALP_lw_Hz = nu_a / self.Q_a
            # check(ALP_lw_Hz)
            tau_a = 1 / (np.pi * ALP_lw_Hz)

            # nu_a = nu_a.convert_to("Hz")
            # self.freq_uplimit = self.freq_uplimit.convert_to("Hz")
            nu_L = nu_a if (nu_a - self.nu_uplimit).value <= 0 else self.nu_uplimit

            T2 = self.GetT2(nu_L)
            Tdelta = self.GetTdelta(NMR_lw_ppm=self.NMR_lw_ppm, nu=nu_L)
            T2star = (T2 ** (-1) + Tdelta ** (-1)) ** (-1)
            # print("**************************")
            # check(nu_a)
            # check(T2)
            # check(T2star)
            # check(Tmeas)
            # Phi np.pi/2

            gin = self.getPick2In() * self.getM2Pick()
            pol = PQ(1, "")
            u = self.getSpecFac(
                nu_L=nu_a, nu_a=nu_a, T2=self.GetT2(nu_L), Tdelta=Tdelta, tau_a=tau_a
            )

            power_sig = self.getPower_sig(
                gin=gin,
                M0=self.getM0(pol, ns=self.ns),
                vol=vol,
                u=u,
                tipAngle=self.getTipAngle(
                    Omega_a=self.getOmega_a(), T2=T2, tau_a=tau_a
                ),
            )

            power_SPN = self.getPower_SPN(
                gin=gin,
                M_SPN=self.getM0(pol=PQ(1, ""), ns=self.ns_SPN),
                vol=vol,
            )
            PSD_SPN = self.getPSD_SPN(power=power_SPN, Delta=1 / (np.pi * T2star))
            # check((SPN_PSDnoise**0.5).convert_to('microPhi_0 / Hz**0.5'))

            eta = self.getEfficPow(RBW_Hz=1 / Tmeas, ALP_lw_Hz=ALP_lw_Hz)
            # check(ALP_lw_Hz)
            powerNoise_MF = self.getPowerNoise_MF(
                PSDnoise_SQUID=self.getPSDnoise_SQUID(nu=nu_a),
                power_SPN=power_SPN,
                ALP_lw_Hz=ALP_lw_Hz,
                Tmeas=Tmeas,
                T2star=T2star,
            )

            glim = (5 * powerNoise_MF / (eta * power_sig)) ** 0.5 * self.gaNN_base
            # check((powerNoise_MF))
            # check(eta)
            # check(P_perp)
            glim = glim.convert_to("GeV**(-1)")
            if verbose:
                check(glim)
            return glim

        glim_list = []
        for i, freq in enumerate(freq_list):
            glim_list.append(sensi(freq, Tmeas_list[i]))

        return glim_list

    def plotXe129_Sensi_Phase1(
        self,
        ax: plt.Axes,
        freq_list: list[PQ],  # frequencies [Hz]
        Tmeas_list: list[PQ],
        verbose: bool = False,
    ):
        """
        gaNN sensitivity with a thermally-polarized methanol

        compute SNR for gaNN = 1 GeV^-1, so as to estimate the gaNN limit
        """
        glim_list = self.getXe129_Sensi_Phase1(freq_list, Tmeas_list, verbose=verbose)
        glim_vals = []
        freq_vals = []
        for glim in glim_list:
            # assert isinstance(glim, PQ), "glim is not a PQ"
            glim = glim.convert_to("GeV**(-1)")
            glim_vals.append(glim.value)
        for freq in freq_list:
            # assert isinstance(glim, PQ), "glim is not a PQ"
            freq = freq.convert_to("Hz")
            freq_vals.append(freq.value)

        glim_vals = np.array(glim_vals)
        freq_vals = np.array(freq_vals)

        # ax01 = fig.add_subplot(gs[0, 1])  #
        # ax10 = fig.add_subplot(gs[1, 0])  #
        # ax11 = fig.add_subplot(gs[1, 1])  #
        # check(np.amin(freq))  # 1348562.406998
        # freq0 = 1348560
        ax.plot(
            freq_vals,
            glim_vals,
            linestyle="--",
            color="tab:green",
            label="updated CASPEr-G-LF limit",
        )
        top = 1e-0
        ax.fill_between(
            x=freq_vals,
            y1=glim_vals,
            y2=top,
            color="tab:green",
            # edgecolor="tab:green",
            # linestyle='--',
            # linewidth=2,
            alpha=0.5,
            # label='updated CASPEr-G-LF limit',
            zorder=2,
        )
        # ax.set_xlim(0, 53)
        # ax.set_ylim(1e-10, 1e-2)

        ax.set_xscale("log")
        # ax.set_yscale('linear')
        # ax.set_xscale('log')
        ax.set_yscale("log")

        # ax.set_xticks(freq_vals[[0, 1, 2, 4]])
        # ax.set_xticklabels(["1 kHz", "10 kHz", "100 kHz", "1.2 MHz"])
        # ax.set_yticks([1e-2, 1e-4, 1e-6, 1e-8, 1e-10])
        # ax.set_yticklabels([1, 10, 100, 1000])
        # ax.set_ylim(bottom=0.1)
        # ax.legend(loc='upper right')
        ax.grid(True)

        ax.set_xlabel(f"Frequency")
        ax.set_ylabel("$|g_\\mathrm{aNN}| [\\mathrm{GeV}^{-1}]$ ", color="k")

    def getXe129_Sensi_Phase2(
        self,
        freq_list: list[PQ],  # frequencies [Hz]
        Tmeas_list: list[PQ],
        verbose: bool = False,
    ) -> list[PQ]:
        """
        gaNN sensitivity with a thermally-polarized methanol

        compute SNR for gaNN = 1 GeV^-1, so as to estimate the gaNN limit
        """
        # if np.amin(freq)<1e3 or np.amax(freq) > 4.3
        # self.useLF_Magnet()

        # get self.sample, self.ns, self.ns_SPN
        self.sampleLXe129_approx()  #
        vol = PQ(10, "cm**3")
        pol = PQ(0.05, "")

        # set inhomogeneity
        self.useShims(PQ(2, "ppm"))

        # sensitivity at nu_a
        def sensi(
            nu_a: PQ,  # frequency [Hz]
            Tmeas: PQ,  # frequencies [Hz]
            # eta:PQ
        ) -> PQ:
            ALP_lw_Hz = nu_a / self.Q_a
            # check(ALP_lw_Hz)
            tau_a = (1 / (np.pi * ALP_lw_Hz)).convert_to("s")

            # nu_a = nu_a.convert_to("Hz")
            # self.freq_uplimit = self.freq_uplimit.convert_to("Hz")
            nu_L = nu_a if (nu_a - self.nu_uplimit).value <= 0 else self.nu_uplimit

            T2 = self.GetT2(nu_L)
            Tdelta = self.GetTdelta(NMR_lw_ppm=self.NMR_lw_ppm, nu=nu_L)
            # check(self.NMR_lw_ppm)
            # check(nu_L)
            T2star = (T2 ** (-1) + Tdelta ** (-1)) ** (-1)
            # print("**************************")
            # check(nu_a)
            # check(T2)
            # check(T2star)
            # check(Tmeas)
            # Phi np.pi/2

            gin = self.getPick2In() * self.getM2Pick()
            # check(self.getPick2In())
            u = self.getSpecFac(
                nu_L=nu_a, nu_a=nu_a, T2=self.GetT2(nu_L), Tdelta=Tdelta, tau_a=tau_a
            )
            check(u)
            M0 = self.getM0(pol, ns=self.ns)
            tipAngle = self.getTipAngle(Omega_a=self.getOmega_a(), T2=T2, tau_a=tau_a)
            # check(M0 * sin(tipAngle.value))

            power_sig = self.getPower_sig(
                gin=gin,
                M0=self.getM0(pol, ns=self.ns),
                vol=vol,
                u=u,
                tipAngle=self.getTipAngle(
                    Omega_a=self.getOmega_a(), T2=T2star, tau_a=tau_a
                ),
            )

            power_SPN = self.getPower_SPN(
                gin=gin,
                M_SPN=self.getM0(pol=PQ(1, ""), ns=self.ns_SPN),
                vol=vol,
            )
            PSD_SPN = self.getPSD_SPN(power=power_SPN, Delta=1 / (np.pi * T2star))
            # check((SPN_PSDnoise**0.5).convert_to('microPhi_0 / Hz**0.5'))

            eta = self.getEfficPow(RBW_Hz=1 / Tmeas, ALP_lw_Hz=ALP_lw_Hz)
            # check(ALP_lw_Hz)
            powerNoise_MF = self.getPowerNoise_MF(
                PSDnoise_SQUID=self.getPSDnoise_SQUID(nu=nu_a),
                power_SPN=power_SPN,
                ALP_lw_Hz=ALP_lw_Hz,
                Tmeas=Tmeas,
                T2star=T2star,
            )

            glim = (5 * powerNoise_MF / (eta * power_sig)) ** 0.5 * self.gaNN_base
            # check((powerNoise_MF))
            # check(eta)
            # check(P_perp)
            glim = glim.convert_to("GeV**(-1)")
            if verbose:

                M_Transver_T2 = (M0 * np.sin(tipAngle.value)).convert_to(
                    "ampere / meter"
                )
                M_Transver_T2star = (
                    M0
                    * self.getTipAngle(
                        Omega_a=self.getOmega_a(), T2=T2star, tau_a=tau_a
                    )
                ).convert_to("ampere / meter")

                sample_R = PQ(4, "mm")
                sample_H = PQ(24, "mm")
                sample_area = 2 * np.pi * sample_R * sample_H
                sample_vol = np.pi * sample_R**2 * sample_H
                flux_sample = M_Transver_T2 * mu_0 * sample_area
                # flux_sample = flux_sample.convert_to('Phi_0')
                ratio = self.getM2Pick() * sample_vol / (sample_area)
                ratio = ratio.convert_to("")
                # check(ratio)
                T2_T2star_ratio = (T2 / T2star).convert_to("")
                self.rho_E_DM = self.rho_E_DM.convert_to("eV/m**3")

                print(
                    f"Transver magnetization (T2*) = {M_Transver_T2star.value:.2e}",
                    M_Transver_T2star.unit,
                )
                print(
                    f"Transver magnetization (T2) = {M_Transver_T2.value:.2e}",
                    M_Transver_T2.unit,
                )
                print(f"F0 = {nu_a.value:.2e}", nu_a.unit)
                print(f"T2 = {T2.value}", T2.unit)
                print(f"T2* = {T2star.value:.2e}", T2star.unit)
                print(
                    f"T2/T2* ratio = {T2_T2star_ratio.value:.2e}", T2_T2star_ratio.unit
                )
                print(f"M0 = {M0.value:.2e}", M0.unit)
                print(f"Volume = {vol.value:.2e}", vol.unit)
                print(
                    f"Coupling gaNN = {self.gaNN_base.value:.2e}", self.gaNN_base.unit
                )
                print(f"DM density = {self.rho_E_DM.value:.2e}", self.rho_E_DM.unit)
                print(f"DM rms velocity = {self.va.value:.2e}", self.va.unit)
                print(
                    f"Rabi frequency = {self.getOmega_a().value:.2e}",
                    self.getOmega_a().unit,
                )
                print(f"Axion Q factor = {self.Q_a.value:.2e}", self.Q_a.unit)
                print(f"axion coherence time = {tau_a.value:.2e}", tau_a.unit)
                # print(f' = {.value:.2e}', .unit)
                check(glim)
            return glim

        glim_list = []
        for i, freq in enumerate(freq_list):
            glim_list.append(sensi(freq, Tmeas_list[i]))
        # check(vol)
        # check(pol)
        # check(self.ns)
        # check(self.rho_E_DM)
        return glim_list

    def plotXe129_Sensi_Phase2(
        self,
        ax: plt.Axes,
        freq_list: list[PQ],  # frequencies [Hz]
        Tmeas_list: list[PQ],
        verbose: bool = False,
    ):
        """
        gaNN sensitivity with a thermally-polarized methanol

        compute SNR for gaNN = 1 GeV^-1, so as to estimate the gaNN limit
        """
        glim_list = self.getXe129_Sensi_Phase2(freq_list, Tmeas_list, verbose=verbose)
        glim_vals = []
        freq_vals = []
        for glim in glim_list:
            # assert isinstance(glim, PQ), "glim is not a PQ"
            glim = glim.convert_to("GeV**(-1)")
            glim_vals.append(glim.value)
        for freq in freq_list:
            # assert isinstance(glim, PQ), "glim is not a PQ"
            freq = freq.convert_to("Hz")
            freq_vals.append(freq.value)

        glim_vals = np.array(glim_vals)
        freq_vals = np.array(freq_vals)

        # ax01 = fig.add_subplot(gs[0, 1])  #
        # ax10 = fig.add_subplot(gs[1, 0])  #
        # ax11 = fig.add_subplot(gs[1, 1])  #
        # check(np.amin(freq))  # 1348562.406998
        # freq0 = 1348560
        ax.plot(
            freq_vals,
            glim_vals,
            linestyle="--",
            color="tab:green",
            label="updated CASPEr-G limit",
        )
        top = 1e-0
        ax.fill_between(
            x=freq_vals,
            y1=glim_vals,
            y2=top,
            color="tab:green",
            # edgecolor="tab:green",
            # linestyle='--',
            # linewidth=2,
            alpha=0.5,
            # label='updated CASPEr-G-LF limit',
            zorder=2,
        )
        # ax.set_xlim(0, 53)
        # ax.set_ylim(1e-10, 1e-2)

        ax.set_xscale("log")
        # ax.set_yscale('linear')
        # ax.set_xscale('log')
        ax.set_yscale("log")

        # ax.set_xticks(freq_vals)
        # ax.set_xticklabels(["1 kHz", "10 kHz", "100 kHz", "1.2 MHz"])
        # ax.set_yticks([1e-2, 1e-4, 1e-6, 1e-8, 1e-10])
        # ax.set_yticklabels([1, 10, 100, 1000])
        # ax.set_ylim(bottom=0.1)
        # ax.legend(loc='upper right')
        ax.grid(True)

        ax.set_xlabel(f"Frequency")
        ax.set_ylabel("$|g_\\mathrm{aNN}| [\\mathrm{GeV}^{-1}]$ ", color="k")

    def plot2017OverviewLimit(self, ax: plt.Axes, verbose: bool = False):
        filepath = rf"limit_data\AxionNeutron\Projections\CASPEr_wind.txt"
        masses, limits = np.loadtxt(filepath, unpack=True)
        freq_vals = []
        for mass in masses:
            # freq_vals.append(energy2freq(PQ(mass, "eV")).value)
            pass
        ax.plot(
            freq_vals,
            limits,
            linestyle="--",
            color="tab:red",
            label="CASPEr-G limit from 2018",
        )
        top = 1e-0
        ax.fill_between(
            x=freq_vals,
            y1=limits,
            y2=top,
            color="tab:red",
            edgecolor="tab:green",
            # linestyle='--',
            linewidth=0,
            alpha=0.3,
            # label='updated CASPEr-G-LF limit',
            zorder=2,
        )

    def measTime1tau_a(
        self,
        freq: PQ,
    ) -> PQ:
        return (self.Q_a / freq).convert_to("s")

    def measTime100tau_a(
        self,
        freq: PQ,
    ) -> PQ:
        return (100 * self.Q_a / freq).convert_to("s")

    def getTotalScanTime(
        self,
        freq_start: PQ,
        freq_stop: PQ,
        func_measTime: Callable[[PQ], PQ],  # measurement time a some frequency
    ) -> PQ:

        def func_measTime_s(
            # func_measTime: Callable[[PQ], PQ],
            freq: float,
        ):
            measTime = func_measTime(PQ(freq, "Hz")).convert_to("s")
            return measTime.value

        # def getTau_a(freq: PQ, Q_a: PQ):
        #     return (Q_a / freq).convert_to('s')

        result, error = quad(
            func_measTime_s,
            freq_start.convert_to("Hz").value,
            freq_stop.convert_to("Hz").value,
        )
        check(result)
        check(error)
        totalScanTime = PQ(result, "s").convert_to("year")
        check(totalScanTime)
        return totalScanTime


import numpy as np

mu0 = 4 * np.pi * 1e-7

# -------- Sample parameters --------
R_s = 0.01  # sample radius (m)
H_s = 0.02  # sample height (m)
M = 1.0  # magnetization (A/m)

# -------- Coil parameters --------
R_c = 0.015  # coil radius (m)
z_c = 0.03  # coil position (m)

# -------- Discretization --------
Nr_s, Nz_s = 50, 100  # sample grid (2D now!)
Nr_c = 200  # coil radial grid

# -------- Sample grid --------
r_s = np.linspace(0, R_s, Nr_s)
z_s = np.linspace(-H_s / 2, H_s / 2, Nz_s)

dr_s = R_s / Nr_s
dz_s = H_s / Nz_s

# -------- Coil grid --------
r_c = np.linspace(0, R_c, Nr_c)
dr_c = R_c / Nr_c

# -------- Precompute mesh --------
R_s_grid, Z_s_grid = np.meshgrid(r_s, z_s, indexing="ij")

# Volume element (already includes 2π from phi integration)
dV = 2 * np.pi * R_s_grid * dr_s * dz_s

# Dipole moment (z-direction)
m_z = M * dV

# Flatten source grid for vectorization
rs_flat = R_s_grid.flatten()
zs_flat = Z_s_grid.flatten()
mz_flat = m_z.flatten()

# -------- Compute flux --------
flux = 0.0

for rc in r_c:
    # Field point: (rc, z_c)

    # Vector from source → field point
    R = np.sqrt((rc - rs_flat) ** 2 + zs_flat**2 + z_c**2 - 2 * z_c * zs_flat)

    # Avoid singularities
    mask = R > 1e-12

    rz = z_c - zs_flat

    # Dipole field Bz component
    Bz = np.zeros_like(R)

    r_hat_z = rz[mask] / R[mask]

    Bz[mask] = (mu0 / (4 * np.pi)) * (
        (3 * mz_flat[mask] * r_hat_z**2 - mz_flat[mask]) / R[mask] ** 3
    )

    # Sum contributions
    Bz_total = np.sum(Bz)

    # Area element (ring on coil)
    dA = 2 * np.pi * rc * dr_c

    flux += Bz_total * dA

print("Magnetic flux (Wb):", flux)
