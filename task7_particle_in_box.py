import numpy as np
import matplotlib.pyplot as plt

hbar = 1.054571817e-34
h = 6.62607015e-34
e = 1.602176634e-19
me = 9.1093837015e-31

a = 1e-9

def energy_eV(n):
    return n**2 * h**2 / (8 * me * a**2) / e

ns = np.arange(1, 8)
plt.figure(figsize=(8, 5))
plt.plot(ns, energy_eV(ns), 'o', ms=7)
nfit = np.linspace(1, 7, 100)
plt.plot(nfit, energy_eV(1)*nfit**2, '--', lw=1,
         label='$E_n = E_1 n^2$')
for n in ns:
    plt.annotate(f'{energy_eV(n):.2f} eV', (n, energy_eV(n)),
                 textcoords='offset points', xytext=(8, -3))
plt.xlabel('quantum number n')
plt.ylabel('energy $E_n$ (eV)')
plt.title(f'Particle in a box: energy levels (electron, a = 1 nm)')
plt.legend()

x = np.linspace(0, a, 2000)
plt.figure(figsize=(8, 6))
for n in range(1, 5):
    psi2 = (2/a) * np.sin(n*np.pi*x/a)**2
    plt.plot(x*1e9, psi2/1e9 + 3*(n-1), label=f'n = {n}')
    plt.axhline(3*(n-1), color='grey', lw=0.5)
plt.xlabel('position x (nm)')
plt.ylabel('$|\\psi_n(x)|^2$ (offset per level)')
plt.title('Probability densities $|\\psi_n|^2$: n-1 nodes for level n')
plt.legend(loc='upper right')

print('Uncertainty principle check (numerical integration):')
print(f'{"n":>3} {"Δx (m)":>12} {"Δp (kg m/s)":>13} {"Δx·Δp/ħ":>11} {"≥ ½ ?":>8}')
products = []
for n in range(1, 11):
    psi = np.sqrt(2/a) * np.sin(n*np.pi*x/a)
    prob = psi**2
    mean_x = np.trapezoid(x*prob, x)
    mean_x2 = np.trapezoid(x**2*prob, x)
    dx = np.sqrt(mean_x2 - mean_x**2)
    dp = n * np.pi * hbar / a
    prod = dx*dp/hbar
    products.append(prod)
    print(f'{n:>3} {dx:>12.3e} {dp:>13.3e} {prod:>11.4f} {"yes" if prod >= 0.5 else "NO":>8}')

plt.figure(figsize=(8, 5))
plt.plot(range(1, 11), products, 'o-', label='$\\Delta x\\,\\Delta p/\\hbar$')
plt.axhline(0.5, color='r', ls='--', label='Heisenberg limit $1/2$')
plt.xlabel('quantum number n')
plt.ylabel('$\\Delta x\\,\\Delta p / \\hbar$')
plt.title('Every state obeys $\\Delta x\\,\\Delta p \\geq \\hbar/2$')
plt.legend()
plt.show()
