"""
Solutions: Chapters 11-14
(black body, photoelectric, hydrogen, electron diffraction)
"""
import numpy as np
import matplotlib.pyplot as plt

# The very short wavelengths in the Stefan-Boltzmann integral make the
# exponential overflow; the result is correctly zero there, so we silence
# the harmless warning rather than pretend it does not happen.
np.seterr(over='ignore', divide='ignore', invalid='ignore')

h = 6.62607015e-34
c = 2.99792458e8
kB = 1.380649e-23
e = 1.602176634e-19
me = 9.1093837015e-31
mp = 1.6726219e-27
eps0 = 8.8541878128e-12
Rgas = 8.314462618

print("=" * 60)
print("CHAPTER 11 - Planck and Einstein")
print("=" * 60)

def planck(lam, T):
    return (2*h*c**2 / lam**5) / np.expm1(h*c / (lam*kB*T))

# 11.1  Stefan-Boltzmann: total power ~ T^4
lam = np.linspace(1e-9, 5e-5, 40000)
Ts = np.array([2000, 3000, 4000, 5000, 6000])
totals = np.array([np.trapezoid(planck(lam, T), lam) for T in Ts])
power, _ = np.polyfit(np.log(Ts), np.log(totals), 1)
print(f"Ex 1: log-log gradient = {power:.4f}  (Stefan-Boltzmann predicts 4)")

# 11.2  Wien's law numerically
print("\nEx 2: Wien check")
lam_fine = np.linspace(1e-8, 5e-6, 200000)
for T in [3000, 5000, 5778]:
    peak = lam_fine[np.argmax(planck(lam_fine, T))]
    print(f"  T={T}: lam_max*T = {peak*T:.6e} m K  (exact 2.897772e-3)")
print("  Accuracy is limited by the wavelength grid spacing.")

# 11.3  where Rayleigh-Jeans fails
T = 5778
rj = 2*c*kB*T / lam**4
ratio = rj / planck(lam, T)
idx = np.argmin(np.abs(ratio - 1.10))
print(f"\nEx 3: Rayleigh-Jeans is 10% too high at lam = {lam[idx]*1e6:.1f} um")

# 11.4  Einstein heat capacity at 300 K
def einstein_C(T, TE):
    x = TE/T
    return 3*Rgas * x**2 * np.exp(x) / np.expm1(x)**2

print("\nEx 4: fraction of the classical 3R value reached at 300 K")
for name, TE in [('lead', 67), ('gold', 121), ('copper', 245),
                 ('tungsten', 240), ('aluminium', 290), ('iron', 350)]:
    frac = einstein_C(300, TE) / (3*Rgas)
    print(f"  {name:10s} TE={TE:3d} K:  {frac*100:.1f} %")

# 11.5  Solve Wien's transcendental equation
x = 5.0
for _ in range(100):
    x = 5*(1 - np.exp(-x))
b = h*c/(x*kB)
print(f"\nEx 5: solved x = {x:.6f}, giving b = {b:.6e} m K")

print("\n" + "=" * 60)
print("CHAPTER 12 - Photoelectric effect")
print("=" * 60)

metals = {'caesium': 2.10, 'potassium': 2.30, 'sodium': 2.28, 'silver': 4.26,
          'zinc': 4.31, 'copper': 4.70, 'gold': 5.10, 'platinum': 5.65}

# 12.1
print("Ex 1: cutoff wavelengths")
for name, W in metals.items():
    lam0 = h*c/(W*e)*1e9
    vis = "VISIBLE" if lam0 > 380 else "UV only"
    print(f"  {name:10s} W={W:.2f} eV  cutoff {lam0:.0f} nm   {vis}")

# 12.2  noise and number of points
print("\nEx 2-3: recovering h from noisy data")
rng = np.random.default_rng(1)
for noise, npts in [(0.05, 12), (0.20, 12), (0.20, 50)]:
    fs = np.linspace(1.5e15, 2.5e15, npts)
    V = (h*fs - 5.65*e)/e + rng.normal(0, noise, npts)
    grad, _ = np.polyfit(fs, V, 1)
    err = abs(grad*e - h)/h*100
    print(f"  noise {noise:.2f} V, {npts:>2} points: h error = {err:.3f} %")

hs = []
for name, W in metals.items():
    fs = np.linspace(1.5e15, 2.5e15, 12)
    V = (h*fs - W*e)/e + rng.normal(0, 0.05, 12)
    grad, _ = np.polyfit(fs, V, 1)
    hs.append(grad*e)
print(f"  across all metals: h = {np.mean(hs):.4e} +/- {np.std(hs):.2e} J s")

print("\nEx 4: plotting against WAVELENGTH gives a curve (V ~ 1/lam), so the")
print("  gradient is not constant and h cannot be read off directly.")

# 12.5  least squares by hand
fs = np.linspace(1.5e15, 2.5e15, 12)
V = (h*fs - 5.65*e)/e + rng.normal(0, 0.05, 12)
n = len(fs)
m_manual = (n*np.sum(fs*V) - np.sum(fs)*np.sum(V)) / (n*np.sum(fs**2) - np.sum(fs)**2)
m_np, _ = np.polyfit(fs, V, 1)
print(f"\nEx 5: manual gradient {m_manual:.6e}, polyfit {m_np:.6e}")

print("\n" + "=" * 60)
print("CHAPTER 13 - Hydrogen")
print("=" * 60)

E0 = me * e**4 / (8 * eps0**2 * h**2)
print(f"E0 = {E0/e:.4f} eV")

# 13.1  Lyman series
print("\nEx 1: Lyman series (n -> 1)")
for n2 in range(2, 6):
    E = E0*(1 - 1/n2**2)
    print(f"  n={n2} -> 1: {h*c/E*1e9:.1f} nm  (ultraviolet - invisible)")

# 13.2  ionisation
print(f"\nEx 2: ionisation energy = {E0/e:.3f} eV (accepted 13.598 eV)")

# 13.3  reduced mass  -- with an important subtlety about air vs vacuum
mu = me*mp/(me+mp)
E0_red = mu * e**4 / (8 * eps0**2 * h**2)
print("\nEx 3: Balmer with and without reduced mass")
print("  NOTE: the familiar values 656.3 / 486.1 nm are AIR wavelengths.")
print("  Our model computes VACUUM wavelengths. Air's refractive index")
print("  (n = 1.000277) makes vacuum values about 0.028% longer.")
lab_air = {3: 656.28, 4: 486.13, 5: 434.05, 6: 410.17}
n_air = 1.000277
print(f"\n  {'n':>2} {'plain':>9} {'reduced':>9} {'measured':>9} {'error':>8}")
for n2, air in lab_air.items():
    vac = air * n_air                       # convert measurement to vacuum
    l1 = h*c/(E0*(1/4 - 1/n2**2))*1e9
    l2 = h*c/(E0_red*(1/4 - 1/n2**2))*1e9
    print(f"  {n2:>2} {l1:>9.2f} {l2:>9.2f} {vac:>9.2f} "
          f"{abs(l2-vac)/vac*100:>7.4f}%")
print("  Compared like with like, the reduced mass brings the error down")
print("  to a few parts in 100,000 - a hundredfold improvement.")
print("  Lesson: when a model and a measurement disagree slightly, check")
print("  whether they are even the same quantity before blaming the model.")

# 13.5  He+
print("\nEx 5: He+ (Z=2) 'Balmer' lines scale as Z^2 = 4x the energy")
for n2 in [3, 4]:
    E = 4*E0*(1/4 - 1/n2**2)
    print(f"  n={n2} -> 2: {h*c/E*1e9:.1f} nm (ultraviolet)")

# 13.6  deuterium isotope shift
md = 2*mp
mu_d = me*md/(me+md)
E0_d = mu_d * e**4 / (8 * eps0**2 * h**2)
lam_H = h*c/(E0_red*(1/4 - 1/9))*1e9
lam_D = h*c/(E0_d*(1/4 - 1/9))*1e9
print(f"\nEx 6: H-alpha  H: {lam_H:.3f} nm,  D: {lam_D:.3f} nm")
print(f"  isotope shift = {lam_H-lam_D:.3f} nm  (how deuterium was found in 1931)")

print("\n" + "=" * 60)
print("CHAPTER 14 - Electron diffraction")
print("=" * 60)

r_tube = 65e-3
d1, d2 = 0.213e-9, 0.123e-9

# 14.1
print("Ex 1: de Broglie wavelengths")
for V in [1000, 3000, 5000]:
    lam_e = h/np.sqrt(2*me*e*V)
    print(f"  V={V:>4} V: {lam_e*1e12:.2f} pm  (shortcut 1.226/sqrt(V) = "
          f"{1.226/np.sqrt(V)*1000:.2f} pm)")

# 14.2
print("\nEx 2: ring radii at 2.5 kV")
for d, name in [(d1, '0.213 nm'), (d2, '0.123 nm')]:
    lam_e = h/np.sqrt(2*me*e*2500)
    th = np.arcsin(lam_e/(2*d))
    print(f"  d={name}: radius {r_tube*np.sin(2*th)*1e3:.2f} mm")
print("  Smaller spacing -> larger Bragg angle -> OUTER ring.")

# 14.6  when diffraction becomes impossible
lam_needed = 2*d2
V_min = h**2/(2*me*e*lam_needed**2)
print(f"\nEx 6: below V = {V_min:.1f} V, lam/2d > 1 and arcsin returns NaN")
print("  Physically: the wavelength is too long for any Bragg reflection.")

# 14.7  noisy recovery of d
print("\nEx 7: recovering d from noisy data")
V = np.linspace(1000, 5000, 30)
rng2 = np.random.default_rng(3)
for d, name in [(d1, '0.213 nm'), (d2, '0.123 nm')]:
    lam_e = h/np.sqrt(2*me*e*V)
    sin_th = lam_e/(2*d) * (1 + rng2.normal(0, 0.01, V.size))
    grad, _ = np.polyfit(sin_th, 1/np.sqrt(V), 1)
    d_rec = grad * h / (2*np.sqrt(2*me*e))
    print(f"  true {name}: recovered {d_rec*1e9:.4f} nm with 1% noise")

plt.figure(figsize=(8, 5))
for d, name in [(d1, 'd = 0.213 nm'), (d2, 'd = 0.123 nm')]:
    lam_e = h/np.sqrt(2*me*e*V)
    th = np.arcsin(lam_e/(2*d))
    plt.plot(V/1000, r_tube*np.sin(2*th)*1e3, 'o-', ms=3, label=name)
plt.xlabel('accelerating voltage (kV)')
plt.ylabel('ring radius (mm)')
plt.title('Ch14 Ex3: ring radius falls with voltage (not linearly)')
plt.legend()
plt.show()
