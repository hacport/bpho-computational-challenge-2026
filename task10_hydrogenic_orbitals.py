import numpy as np
import matplotlib.pyplot as plt
from math import factorial

def assoc_laguerre(k, alpha, x):
    Lm1 = np.ones_like(x)
    if k == 0:
        return Lm1
    L0 = 1 + alpha - x
    for i in range(1, k):
        Lm1, L0 = L0, ((2*i + 1 + alpha - x)*L0 - (i + alpha)*Lm1) / (i + 1)
    return L0

def assoc_legendre(l, m, x):
    pmm = np.ones_like(x)
    if m > 0:
        pmm = (-1)**m * np.prod(np.arange(1, 2*m, 2)) * (1 - x**2)**(m/2)
    if l == m:
        return pmm
    pmmp1 = x * (2*m + 1) * pmm
    if l == m + 1:
        return pmmp1
    for ll in range(m + 2, l + 1):
        pmm, pmmp1 = pmmp1, (x*(2*ll - 1)*pmmp1 - (ll + m - 1)*pmm) / (ll - m)
    return pmmp1

def radial(n, l, r, Z=1):
    rho = 2*Z*r/n
    norm = np.sqrt((2*Z/n)**3 * factorial(n-l-1) / (2*n*factorial(n+l)))
    return norm * np.exp(-rho/2) * rho**l * assoc_laguerre(n-l-1, 2*l+1, rho)

def sph_harm_real(l, m, theta, phi):
    norm = np.sqrt((2*l+1)/(4*np.pi) * factorial(l-m)/factorial(l+m))
    Y = norm * assoc_legendre(l, m, np.cos(theta))
    if m > 0:
        Y = Y * np.sqrt(2) * np.cos(m*phi)
    return Y

def psi(n, l, m, x, y, z, Z=1):
    r = np.sqrt(x**2 + y**2 + z**2) + 1e-12
    theta = np.arccos(z/r)
    phi = np.arctan2(y, x)
    return radial(n, l, r, Z) * sph_harm_real(l, m, theta, phi)

if __name__ == '__main__':
    print('Verification (all lengths in Bohr radii a0):')
    r = np.linspace(0, 60, 20000)
    for n, l in [(1, 0), (2, 0), (2, 1), (3, 0), (3, 1), (3, 2)]:
        P = r**2 * radial(n, l, r)**2
        norm = np.trapezoid(P, r)
        mean_r = np.trapezoid(r*P, r)
        print(f'  n={n} ℓ={l}:  ∫|ψ|²dV = {norm:.6f} (exact 1),  '
              f'⟨r⟩ = {mean_r:.3f} a₀ (exact {0.5*(3*n**2 - l*(l+1)):.3f})')
    peak_1s = r[np.argmax(r**2 * radial(1, 0, r)**2)]
    print(f'  1s radial probability peaks at r = {peak_1s:.4f} a₀ (exact 1 — the Bohr radius)\n')

    orbitals = [(1, 0, 0), (2, 0, 0), (2, 1, 0),
                (2, 1, 1), (3, 1, 0), (3, 2, 0),
                (3, 2, 1), (3, 2, 2), (4, 2, 0)]

    fig1, axes = plt.subplots(3, 3, figsize=(11, 11))
    for ax, (n, l, m) in zip(axes.flat, orbitals):
        extent = 6*n
        g = np.linspace(-extent, extent, 300)
        X, Z = np.meshgrid(g, g)
        density = psi(n, l, m, X, 0*X, Z)**2
        ax.pcolormesh(X, Z, density, cmap='inferno',
                      norm=plt.matplotlib.colors.PowerNorm(0.4))
        ax.set_title(f'n={n}, l={l}, m={m}', fontsize=10)
        ax.set_aspect('equal')
        ax.set_xticks([]); ax.set_yticks([])
    fig1.suptitle('Hydrogen orbitals: $|\\psi_{nlm}|^2$ in the x-z plane '
                  '(box spans $\\pm 6n\\,a_0$)')

    fig2 = plt.figure(figsize=(8, 5))
    for n, l, name in [(1, 0, '1s'), (2, 0, '2s'), (2, 1, '2p'),
                       (3, 0, '3s'), (3, 1, '3p'), (3, 2, '3d')]:
        P = r**2 * radial(n, l, r)**2
        plt.plot(r, P, label=name)
    plt.xlim(0, 30)
    plt.xlabel('radius r ($a_0$)')
    plt.ylabel('radial probability $r^2 R_{nl}^2$')
    plt.title('Radial probability distributions')
    plt.legend()

    fig3 = plt.figure(figsize=(11, 5.5))
    rng = np.random.default_rng(0)
    for idx, (n, l, m) in enumerate([(2, 1, 0), (3, 2, 0)]):
        ax = fig3.add_subplot(1, 2, idx+1, projection='3d')
        extent = 6*n
        pts = rng.uniform(-extent, extent, (400000, 3))
        dens = psi(n, l, m, pts[:, 0], pts[:, 1], pts[:, 2])**2
        keep = rng.uniform(0, dens.max(), 400000) < dens
        P = pts[keep][:8000]
        ax.scatter(P[:, 0], P[:, 1], P[:, 2], s=1, alpha=0.25,
                   c=P[:, 2], cmap='coolwarm')
        ax.set_title(f'Monte Carlo sample of $|\\psi|^2$:  n={n}, l={l}, m={m}')
        ax.set_xlim(-extent, extent); ax.set_ylim(-extent, extent)
        ax.set_zlim(-extent, extent)
    fig3.suptitle('3D visualization: each dot is one sample of the electron '
                  'probability cloud')
    plt.show()
