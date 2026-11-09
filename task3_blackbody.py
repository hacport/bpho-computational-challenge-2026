import numpy as np
import matplotlib.pyplot as plt


h  = 6.62607015e-34
c  = 2.99792458e8
kB = 1.380649e-23
Rgas = 8.314462618


lam = np.linspace(1e-8, 3e-6, 2000)

def planck(lam, T):
    """Spectral radiance B(lambda, T), W sr^-1 m^-3"""
    return (2*h*c**2 / lam**5) / np.expm1(h*c / (lam*kB*T))

plt.figure(figsize=(9, 5))
for T in [3000, 4000, 5000, 5778, 6000]:
    label = f'{T} K (Sun)' if T == 5778 else f'{T} K'
    plt.plot(lam*1e9, planck(lam, T), label=label)


Ts = np.linspace(2500, 6500, 200)
lam_peak = 2.897771955e-3 / Ts
plt.plot(lam_peak*1e9, planck(lam_peak, Ts), 'k--', lw=1,
         label="Wien's law $\\lambda_{max}=b/T$")


plt.axvspan(380, 700, color='yellow', alpha=0.15, label='visible light')

rayleigh_jeans = 2*c*kB*5778 / lam**4
plt.plot(lam*1e9, rayleigh_jeans, 'r:', lw=1.5,
         label='Rayleigh–Jeans (classical, 5778 K)')

plt.xlim(0, 3000)
plt.ylim(0, 5e13)
plt.xlabel('wavelength $\\lambda$ (nm)')
plt.ylabel('spectral radiance $B(\\lambda,T)$  (W sr$^{-1}$ m$^{-3}$)')
plt.title('Planck black-body spectrum')
plt.legend()


for T in [3000, 4000, 5000, 5778, 6000]:
    print(f'T = {T} K:  peak at {2.897771955e-3/T*1e9:.0f} nm')

from cie_color import spectrum_to_rgb
lam_vis = np.linspace(380e-9, 740e-9, 300)
for i, T in enumerate([3000, 4000, 5000, 5778, 6000]):
    Bv = planck(lam_vis, T)
    glow = spectrum_to_rgb(lam_vis*1e9, Bv/Bv.max())
    plt.gca().add_patch(plt.Rectangle((2450, 4.3e13 - i*0.45e13), 400, 0.35e13,
                                      color=glow))
    plt.text(2420, 4.45e13 - i*0.45e13, f'{T} K glows:', fontsize=8,
             ha='right', va='center')


def einstein_C(T, TE):
    """Molar heat capacity, Einstein model. TE = Einstein temperature."""
    x = TE / T
    return 3*Rgas * x**2 * np.exp(x) / np.expm1(x)**2
`
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
