import numpy as np
import matplotlib.pyplot as plt

h = 6.62607015e-34
c = 2.99792458e8
e = 1.602176634e-19
me = 9.10938356e-31

lam_C = h / (me * c)
print(f'Compton wavelength λ_C = h/(mₑc) = {lam_C*1e12:.3f} pm\n')

theta = np.linspace(0.001, np.pi, 500)

beams = {"Compton's X-rays (71.1 pm, 17.4 keV)": 71.1e-12,
         'γ-ray, E = 511 keV': h*c/(0.511e6*e),
         'γ-ray, E = 1.24 MeV': h*c/(1.24e6*e)}

fig, axes = plt.subplots(1, 3, figsize=(13, 4.4))

for name, lam0 in beams.items():
    dlam = lam_C * (1 - np.cos(theta))
    lam1 = lam0 + dlam
    frac = dlam / lam0

    E0 = h*c/lam0
    E1 = h*c/lam1
    KE = E0 - E1
    gamma = 1 + KE/(me*c**2)
    v = c*np.sqrt(1 - 1/gamma**2)

    phi = np.arctan2(np.sin(theta)/lam1, 1/lam0 - np.cos(theta)/lam1)

    axes[0].plot(np.degrees(theta), frac, label=name)
    axes[1].plot(np.degrees(theta), v/c, label=name)
    axes[2].plot(np.degrees(theta), np.degrees(phi), label=name)

    E0_eV = E0/e
    print(f'{name}')
    print(f'  max fractional shift (180 deg): {frac[-1]:.4f}')
    print(f'  max recoil speed: {v[-1]/c:.4f} c')
    check = E0 - (E1[-1] + KE[-1])
    print(f'  energy conservation residual at 180 deg: {check:.2e} J (should be ~0)\n')

axes[0].set_ylabel('fractional shift $\\Delta\\lambda/\\lambda_0$')
axes[0].set_title('wavelength shift')
axes[1].set_ylabel('electron recoil speed  $v/c$')
axes[1].set_title('recoil speed (relativistic)')
axes[2].set_ylabel('electron recoil angle $\\phi$ (deg)')
axes[2].set_title('recoil angle')
for ax in axes:
    ax.set_xlabel('photon scattering angle $\\theta$ (deg)')
    ax.legend(fontsize=7)
fig.suptitle("Compton scattering: $\\lambda' - \\lambda = "
             "\\frac{h}{m_e c}(1-\\cos\\theta)$")
plt.tight_layout()
plt.show()
