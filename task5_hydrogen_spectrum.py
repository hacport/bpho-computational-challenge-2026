import numpy as np
import matplotlib.pyplot as plt

h = 6.62607015e-34
c = 2.99792458e8
e = 1.602176634e-19
me = 9.1093837015e-31
eps0 = 8.8541878128e-12

E0 = me * e**4 / (8 * eps0**2 * h**2)

series = {'Lyman (n1=1)': (1, 'purple'), 'Balmer (n1=2)': (2, 'teal'),
          'Paschen (n1=3)': (3, 'orange'), 'Brackett (n1=4)': (4, 'brown')}

measured_balmer = {656.3: 'H-alpha (red)', 486.1: 'H-beta (blue-green)',
                   434.0: 'H-gamma (violet)', 410.2: 'H-delta (violet)'}

plt.figure(figsize=(10, 5.5))
print(f'ground state energy E1 = {-E0/e:.2f} eV\n')

for name, (n1, colour) in series.items():
    lams, Es = [], []
    for n2 in range(n1+1, n1+15):
        E_photon = E0 * (1/n1**2 - 1/n2**2)
        lam = h*c / E_photon
        lams.append(lam*1e9)
        Es.append(E_photon/e)
    plt.plot(lams, Es, 'o-', ms=4, lw=0.8, color=colour, label=name)
    lam_limit = h*c / (E0/n1**2) * 1e9
    plt.axvline(lam_limit, color=colour, ls=':', lw=0.8)

plt.axvspan(380, 700, color='yellow', alpha=0.15, label='visible light')
plt.xscale('log')
plt.xlabel('photon wavelength $\\lambda$ (nm, log scale)')
plt.ylabel('photon energy (eV)')
plt.title('Hydrogen emission spectrum: $E = E_0(1/n_1^2 - 1/n_2^2)$')
plt.legend()

print('Balmer series check vs laboratory values:')
for n2 in [3, 4, 5, 6]:
    E_photon = E0 * (1/4 - 1/n2**2)
    lam_nm = h*c / E_photon * 1e9
    meas = list(measured_balmer.keys())[n2-3]
    print(f'  n={n2} -> 2:  model {lam_nm:.1f} nm,  measured {meas} nm '
          f'({measured_balmer[meas]}),  diff {abs(lam_nm-meas)/meas*100:.3f} %')

from cie_color import wavelength_to_rgb

fig2, ax2 = plt.subplots(figsize=(10, 2.6))
ax2.set_facecolor('black')
for n2 in range(3, 20):
    E_photon = E0 * (1/4 - 1/n2**2)
    lam_nm = h*c / E_photon * 1e9
    if 380 < lam_nm < 740:
        ax2.axvline(lam_nm, color=wavelength_to_rgb(lam_nm), lw=3)
        if n2 <= 6:
            ax2.text(lam_nm, 1.02, f'{lam_nm:.0f}', ha='center', fontsize=8)
ax2.set_xlim(380, 740)
ax2.set_ylim(0, 1)
ax2.set_yticks([])
ax2.set_xlabel('wavelength (nm)')
ax2.set_title('Balmer series as seen through a spectroscope '
              '(true CIE 1931 colours)')

plt.show()
