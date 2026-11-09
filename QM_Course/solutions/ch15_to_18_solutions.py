"""
Solutions: Chapters 15-18
(particle in a box, quantum cryptography, Compton, orbitals)
"""
import numpy as np
import matplotlib.pyplot as plt
from math import factorial

h = 6.62607015e-34
hbar = 1.054571817e-34
c = 2.99792458e8
e = 1.602176634e-19
me = 9.1093837015e-31

print("=" * 60)
print("CHAPTER 15 - Particle in a box")
print("=" * 60)

def E_box(n, a, m=me):
    return n**2 * h**2 / (8*m*a**2) / e

# 15.1
print("Ex 1: ground state energy vs box width")
for a_nm in [0.5, 1.0, 2.0]:
    print(f"  a = {a_nm} nm: E1 = {E_box(1, a_nm*1e-9):.3f} eV")
print("  E ~ 1/a^2: halving the box quadruples the energy. Tighter")
print("  confinement means larger momentum uncertainty, hence more energy.")

# 15.2
a = 1e-9
dE = (E_box(2, a) - E_box(1, a)) * e
print(f"\nEx 2: n=2 -> 1 photon: {dE/e:.3f} eV, "
      f"{h*c/dE*1e9:.0f} nm (infrared)")

# 15.3 normalisation
print("\nEx 3: normalisation check")
x = np.linspace(0, a, 20000)
for n in range(1, 6):
    psi = np.sqrt(2/a)*np.sin(n*np.pi*x/a)
    print(f"  n={n}: integral = {np.trapezoid(psi**2, x):.6f}")

# 15.4 convergence study
print("\nEx 4: convergence of the uncertainty product (n=1)")
exact = 0.5*np.sqrt(np.pi**2/3 - 2)
print(f"  exact analytic value = {exact:.8f}")
for npts in [50, 200, 1000, 5000, 20000]:
    xg = np.linspace(0, a, npts)
    psi = np.sqrt(2/a)*np.sin(np.pi*xg/a)
    prob = psi**2
    mx = np.trapezoid(xg*prob, xg)
    mx2 = np.trapezoid(xg**2*prob, xg)
    dx = np.sqrt(mx2 - mx**2)
    dp = np.pi*hbar/a
    prod = dx*dp/hbar
    print(f"  {npts:>6} points: {prod:.8f}  error {abs(prod-exact):.2e}")
print("  Error falls roughly as 1/N^2, matching the trapezium rule's O(dx^2).")

# 15.5 analytic <x^2>
n = 1
mx2_analytic = a**2*(1/3 - 1/(2*n**2*np.pi**2))
xg = np.linspace(0, a, 20000)
psi = np.sqrt(2/a)*np.sin(n*np.pi*xg/a)
print(f"\nEx 5: <x^2> analytic {mx2_analytic:.6e}, "
      f"numerical {np.trapezoid(xg**2*psi**2, xg):.6e}")

# 15.6 <p> = 0
dpsi = np.gradient(psi, xg)
p_integrand = psi*dpsi
print(f"\nEx 6: <p> integral = {np.trapezoid(p_integrand, xg):.3e} (zero)")
print("  A standing wave is an equal superposition of +k and -k travelling")
print("  waves, so the mean momentum must vanish.")

# 15.7 matrix eigenvalue solution
print("\nEx 7: solving the box numerically as a matrix problem")
N = 400
xg = np.linspace(0, a, N+2)[1:-1]
dx = xg[1] - xg[0]
main = np.full(N, -2.0)
off = np.ones(N-1)
Lap = (np.diag(main) + np.diag(off, 1) + np.diag(off, -1)) / dx**2
H = -(hbar**2/(2*me)) * Lap
vals = np.linalg.eigvalsh(H)
print(f"  {'n':>2} {'numerical (eV)':>16} {'analytic (eV)':>15}")
for i in range(5):
    print(f"  {i+1:>2} {vals[i]/e:>16.4f} {E_box(i+1, a):>15.4f}")
print("  This is how real quantum problems are solved when no formula exists.")

print("\n" + "=" * 60)
print("CHAPTER 16 - Quantum cryptography")
print("=" * 60)

def classical_mismatch(th, ph):
    return 1 - np.cos(th)**2*np.cos(ph)**2 - np.sin(th)**2*np.sin(ph)**2

def quantum_mismatch(th, ph):
    return np.sin(ph - th)**2

# 16.1 biggest disagreement
g = np.linspace(0, np.pi/2, 400)
TH, PH = np.meshgrid(g, g)
diff = np.abs(classical_mismatch(TH, PH) - quantum_mismatch(TH, PH))
i, j = np.unravel_index(np.argmax(diff), diff.shape)
print(f"Ex 1: largest gap at theta={np.degrees(TH[i,j]):.1f} deg, "
      f"phi={np.degrees(PH[i,j]):.1f} deg")
print(f"  classical {classical_mismatch(TH[i,j], PH[i,j]):.4f}, "
      f"quantum {quantum_mismatch(TH[i,j], PH[i,j]):.4f}")

# 16.2 aligned detectors
rng = np.random.default_rng(5)
angles = rng.uniform(0, np.pi/2, 10)
print(f"\nEx 2: aligned detectors, max quantum mismatch = "
      f"{np.max(quantum_mismatch(angles, angles)):.2e}  (exactly zero)")

# 16.5 CHSH
print("\nEx 5: CHSH test at the optimal Bell angles")
def E_quantum(a1, b1):
    return 1 - 2*quantum_mismatch(a1, b1)
def E_classical(a1, b1):
    return 1 - 2*classical_mismatch(a1, b1)

a1, a2 = 0, np.radians(45)
b1, b2 = np.radians(22.5), np.radians(67.5)
S_q = abs(E_quantum(a1,b1) - E_quantum(a1,b2) + E_quantum(a2,b1) + E_quantum(a2,b2))
S_c = abs(E_classical(a1,b1) - E_classical(a1,b2) + E_classical(a2,b1)
          + E_classical(a2,b2))
print(f"  quantum  S = {S_q:.4f}   (Tsirelson bound 2*sqrt(2) = {2*np.sqrt(2):.4f})")
print(f"  classical S = {S_c:.4f}   (local realism requires S <= 2)")

print("\n" + "=" * 60)
print("CHAPTER 17 - Compton scattering")
print("=" * 60)

lam_C = h/(me*c)

# 17.1
print(f"Ex 1: shift at 90 deg = {lam_C*1e12:.3f} pm for every beam")
print("  Independent of lambda_0 because the formula contains only theta.")

# 17.2
lam0 = 500e-9
print(f"\nEx 2: visible light (500 nm) at 180 deg:")
print(f"  fractional shift = {2*lam_C/lam0*1e6:.2f} parts per million - "
      f"undetectable in optics.")

# 17.4 Compton edge
print("\nEx 4: Compton edge (max energy given to the electron)")
for E_keV in [100, 511, 1240]:
    lam_in = h*c/(E_keV*1e3*e)
    lam_out = lam_in + 2*lam_C
    K_max = h*c/lam_in - h*c/lam_out
    print(f"  {E_keV:>4} keV photon: edge at {K_max/e/1e3:.1f} keV")

# 17.5 momentum conservation check
theta = np.linspace(0.001, np.pi, 500)
lam_in = 71.1e-12
dlam = lam_C*(1 - np.cos(theta))
lam_out = lam_in + dlam
K = h*c/lam_in - h*c/lam_out
gamma = 1 + K/(me*c**2)
v = c*np.sqrt(1 - 1/gamma**2)
phi = np.arctan2(np.sin(theta)/lam_out, 1/lam_in - np.cos(theta)/lam_out)
px = h/lam_in - h/lam_out*np.cos(theta) - gamma*me*v*np.cos(phi)
py = h/lam_out*np.sin(theta) - gamma*me*v*np.sin(phi)
print(f"\nEx 5: max momentum residual: x {np.max(np.abs(px)):.2e}, "
      f"y {np.max(np.abs(py)):.2e} kg m/s")

# 17.6 where the classical formula fails
lam_in = h*c/(1.24e6*e)
dlam = lam_C*(1 - np.cos(theta))
K = h*c/lam_in - h*c/(lam_in + dlam)
v_class = np.sqrt(2*K/me)
bad = theta[v_class > c]
print(f"\nEx 6: classical v exceeds c beyond theta = "
      f"{np.degrees(bad[0]):.1f} deg")

print("\n" + "=" * 60)
print("CHAPTER 18 - Hydrogenic orbitals")
print("=" * 60)

def assoc_laguerre(k, alpha, x):
    Lm1 = np.ones_like(x)
    if k == 0:
        return Lm1
    L0 = 1 + alpha - x
    for i in range(1, k):
        Lm1, L0 = L0, ((2*i + 1 + alpha - x)*L0 - (i + alpha)*Lm1) / (i + 1)
    return L0

def radial(n, l, r, Z=1):
    rho = 2*Z*r/n
    norm = np.sqrt((2*Z/n)**3 * factorial(n-l-1) / (2*n*factorial(n+l)))
    return norm * np.exp(-rho/2) * rho**l * assoc_laguerre(n-l-1, 2*l+1, rho)

# 18.1 n=4 normalisation
r = np.linspace(0, 120, 60000)
print("Ex 1: n=4 normalisation")
for l in range(4):
    P = r**2 * radial(4, l, r)**2
    print(f"  n=4 l={l}: {np.trapezoid(P, r):.6f}, "
          f"<r> = {np.trapezoid(r*P, r):.3f} (exact {0.5*(48-l*(l+1)):.3f})")

# 18.2 node counting
print("\nEx 2: radial nodes (expect n-l-1)")
rr = np.linspace(0.01, 60, 20000)
for n, l in [(3,0), (3,1), (3,2)]:
    R = radial(n, l, rr)
    nodes = np.sum(np.diff(np.sign(R)) != 0)
    print(f"  n={n} l={l}: found {nodes}, expected {n-l-1}")

# 18.4 Z scaling
print("\nEx 4: He+ (Z=2)")
for Z in [1, 2]:
    P = r**2 * radial(1, 0, r, Z)**2
    print(f"  Z={Z}: <r> = {np.trapezoid(r*P, r):.4f} a0")
print("  <r> scales as 1/Z: double the charge, half the radius.")

# figures
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
rr = np.linspace(0.001, 10, 2000)
axes[0].plot(rr, radial(1, 0, rr)**2, label=r'$|R_{10}|^2$ (density)')
axes[0].plot(rr, rr**2*radial(1, 0, rr)**2, label=r'$r^2|R_{10}|^2$ (radial prob)')
axes[0].axvline(1, color='k', ls=':', label='Bohr radius')
axes[0].set_xlabel('r (a0)'); axes[0].legend()
axes[0].set_title('Ch18 Ex3: two different questions')

for n, l, lab in [(3,0,'3s'), (3,1,'3p'), (3,2,'3d')]:
    axes[1].plot(rr, radial(n, l, rr), label=lab)
axes[1].axhline(0, color='k', lw=0.5)
axes[1].set_xlabel('r (a0)'); axes[1].legend()
axes[1].set_title('radial functions: count the zero crossings')
plt.tight_layout()
plt.show()
