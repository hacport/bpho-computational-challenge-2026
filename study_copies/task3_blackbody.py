import numpy as np
import matplotlib.pyplot as plt

# ---- constants (SI) ----
h  = 6.62607015e-34   # Planck constant
c  = 2.99792458e8     # speed of light
kB = 1.380649e-23     # Boltzmann constant
Rgas = 8.314462618    # molar gas constant

# ========== Figure 1: Planck black-body spectrum ==========
lam = np.linspace(1e-8, 3e-6, 2000)          # wavelength: 10 nm to 3 um

def planck(lam, T):
    """Spectral radiance B(lambda, T), W sr^-1 m^-3"""
    return (2*h*c**2 / lam**5) / np.expm1(h*c / (lam*kB*T))

plt.figure(figsize=(9, 5))
for T in [3000, 4000, 5000, 5778, 6000]:
    label = f'{T} K (Sun)' if T == 5778 else f'{T} K'
    plt.plot(lam*1e9, planck(lam, T), label=label)

# elite touch 1: Wien's displacement law locus through the peaks
Ts = np.linspace(2500, 6500, 200)
lam_peak = 2.897771955e-3 / Ts               # Wien: lambda_max = b/T
plt.plot(lam_peak*1e9, planck(lam_peak, Ts), 'k--', lw=1,
         label="Wien's law $\\lambda_{max}=b/T$")

# elite touch 2: shade the visible band
plt.axvspan(380, 700, color='yellow', alpha=0.15, label='visible light')

plt.xlim(0, 3000)
plt.xlabel('wavelength $\\lambda$ (nm)')
plt.ylabel('spectral radiance $B(\\lambda,T)$  (W sr$^{-1}$ m$^{-3}$)')
plt.title('Planck black-body spectrum')
plt.legend()

# print peak wavelengths (for the video)
for T in [3000, 4000, 5000, 5778, 6000]:
    print(f'T = {T} K:  peak at {2.897771955e-3/T*1e9:.0f} nm')

# ========== Figure 2: Einstein heat capacity of solids ==========
def einstein_C(T, TE):
    """Molar heat capacity, Einstein model. TE = Einstein temperature."""
    x = TE / T
    return 3*Rgas * x**2 * np.exp(x) / np.expm1(x)**2

T = np.linspace(1, 500, 1000)
metals = {'lead (T$_E$=67 K)': 67, 'gold (T$_E$=121 K)': 121,
          'copper (T$_E$=245 K)': 245, 'iron (T$_E$=350 K)': 350}

plt.figure(figsize=(9, 5))
for name, TE in metals.items():
    plt.plot(T, einstein_C(T, TE), label=name)
plt.axhline(3*Rgas, color='k', ls='--', lw=1,
            label='Dulong–Petit limit 3R $\\approx$ 24.9')
plt.xlabel('temperature T (K)')
plt.ylabel('molar heat capacity C (J K$^{-1}$ mol$^{-1}$)')
plt.title("Einstein's model of heat capacity of solids")
plt.legend()
plt.show()