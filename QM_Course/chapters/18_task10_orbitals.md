# Chapter 18 — Task 10: Hydrogenic orbitals

**The task:** *"Plot 2D slices and 3D visualizations of the probability density |ψ|²
for an electron in a hydrogenic atom, given n, l, m quantum numbers. Use the
provided solutions to the Schrödinger Equation as a recipe."*

**Beyond it:** implementing the special functions from their recurrence relations
rather than importing them, numerical verification of normalisation and ⟨r⟩,
Monte Carlo 3D clouds, m-state morphing, and LCAO molecular orbitals for H₂⁺.

The most demanding chapter — and the most rewarding.

---

## 18.1 The physics

### From Bohr to Schrödinger

Bohr gave the right energies for the wrong reasons. Solving the Schrödinger
equation for the Coulomb potential V(r) = −Ze²/4πε₀r gives the same energies
*and* the full three-dimensional structure.

Because the potential depends only on r, the equation **separates** in spherical
coordinates:

  **ψ_{nlm}(r,θ,φ) = R_{nl}(r) · Y_l^m(θ,φ)**

a radial part times an angular part. Three separation constants emerge as three
quantum numbers:

| Symbol | Name | Allowed values | Controls |
|---|---|---|---|
| n | principal | 1, 2, 3, … | energy, overall size |
| l | angular momentum | 0 … n−1 | shape (s, p, d, f) |
| m | magnetic | −l … +l | orientation |

with E_n = −13.6Z²/n² eV — depending on n *only*. That degeneracy (different l,
m sharing an energy) is special to the 1/r potential.

### The radial part

  R_{nl}(r) = √[(2Z/na₀)³ (n−l−1)!/(2n(n+l)!)] · e^(−ρ/2) ρ^l L_{n−l−1}^{2l+1}(ρ)

with ρ = 2Zr/na₀ and L the **associated Laguerre polynomials**. The pieces:

- `e^(−ρ/2)` — exponential decay; the electron is bound
- `ρ^l` — suppresses the wavefunction at the origin for l > 0 (angular momentum
  keeps the electron away from the nucleus)
- Laguerre polynomial — its zeros are the **radial nodes**; there are n−l−1 of them

### The angular part

  Y_l^m(θ,φ) = √[(2l+1)/4π · (l−m)!/(l+m)!] · P_l^m(cos θ) e^{imφ}

with P the **associated Legendre functions**. These give the familiar shapes:
l=0 spherical, l=1 dumbbells, l=2 four-lobed clovers. There are l angular nodes,
so **total nodes = n−1** always.

Because e^{imφ} is complex, we use **real combinations** (cos mφ and sin mφ),
which is what chemists draw as p_x, p_y, p_z. Your code does this with the
`np.sqrt(2)*np.cos(m*phi)` factor.

### What |ψ|² means

|ψ|²dV is the probability of finding the electron in volume dV. The electron is
not orbiting; there is no trajectory. The cloud *is* the description.

Two different, easily confused quantities:

- **|ψ|²** — probability *per unit volume* at a point. Largest at the nucleus for 1s.
- **r²|R|²** — probability per unit *radius*, accounting for the shell of area
  4πr² at radius r. Peaks at a₀ for 1s.

Both are correct answers to different questions. The second is why "the electron
is most likely found at the Bohr radius" is true, even though the density is
highest at r = 0.

**Useful exact results for checking:** ∫|ψ|²dV = 1, and

  ⟨r⟩ = (a₀/2)[3n² − l(l+1)]

---

## 18.2 Implementing special functions from recurrences

`scipy` has these built in, but implementing them yourself is both more
impressive and more instructive — and it removes a dependency.

### Associated Laguerre

```python
def assoc_laguerre(k, alpha, x):
    Lm1 = np.ones_like(x)
    if k == 0:
        return Lm1
    L0 = 1 + alpha - x
    for i in range(1, k):
        Lm1, L0 = L0, ((2*i + 1 + alpha - x)*L0 - (i + alpha)*Lm1) / (i + 1)
    return L0
```

The recurrence relation is

  (i+1)L_{i+1}^α = (2i+1+α−x)L_i^α − (i+α)L_{i−1}^α

Start from L₀ = 1 and L₁ = 1+α−x, then climb. The key line is the **simultaneous
assignment** (§4.3):

```python
Lm1, L0 = L0, (new value using both)
```

Both right-hand sides are evaluated *before* either assignment happens, so the
old `L0` is still available while computing the new one. Written as two separate
statements it would be wrong.

`np.ones_like(x)` makes an array of ones with the same shape as `x` — so the
function works whether `x` is one number or a 300×300 grid.

### Associated Legendre

```python
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
```

Same strategy: start with the closed-form P_m^m, step up to P_{m+1}^m, then
recur. `np.prod(np.arange(1, 2*m, 2))` computes the double factorial (2m−1)!! =
1·3·5·…

**Why recurrences at all?** Writing each polynomial out explicitly would need a
separate formula per (n,l) — dozens of lines, all opportunities for typos.
A recurrence is one loop that generates them all, exactly, to any order. This is
how numerical libraries genuinely do it.

### Assembling ψ

```python
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
```

Working in units of the Bohr radius (a₀ = 1) keeps the numbers near 1 and avoids
awkward powers of 10 — a standard trick called **atomic units**.

The `+ 1e-12` prevents division by zero exactly at the origin. A tiny fudge, and
you should be able to justify it: it shifts r by a millionth of a millionth of a
Bohr radius, far below any visible or numerical consequence.

The Cartesian → spherical conversion is standard: r by Pythagoras in 3D,
θ = arccos(z/r), φ = arctan2(y, x).

`Z=1` as a default means the same code does He⁺ (Z=2) or Li²⁺ (Z=3) for free
(§5.2).

---

## 18.3 Verification — the part that earns marks

```python
r = np.linspace(0, 60, 20000)
for n, l in [(1,0), (2,0), (2,1), (3,0), (3,1), (3,2)]:
    P = r**2 * radial(n, l, r)**2
    norm = np.trapezoid(P, r)
    mean_r = np.trapezoid(r*P, r)
    print(f'  n={n} ℓ={l}:  ∫|ψ|²dV = {norm:.6f} (exact 1),  '
          f'⟨r⟩ = {mean_r:.3f} a₀ (exact {0.5*(3*n**2 - l*(l+1)):.3f})')

peak_1s = r[np.argmax(r**2 * radial(1, 0, r)**2)]
print(f'  1s radial probability peaks at r = {peak_1s:.4f} a₀')
```

Output:

```
  n=1 ℓ=0:  ∫|ψ|²dV = 1.000000 (exact 1),  ⟨r⟩ = 1.500 a₀ (exact 1.500)
  n=2 ℓ=0:  ∫|ψ|²dV = 1.000000 (exact 1),  ⟨r⟩ = 6.000 a₀ (exact 6.000)
  n=2 ℓ=1:  ∫|ψ|²dV = 1.000000 (exact 1),  ⟨r⟩ = 5.000 a₀ (exact 5.000)
  ...
  1s radial probability peaks at r = 0.9990 a₀
```

Three independent checks passing:

1. **Normalisation to six decimal places** — your Laguerre polynomials and
   normalisation constants are right. If either were wrong this would not be 1.
2. **⟨r⟩ matching (a₀/2)[3n²−l(l+1)] for six states** — a much stronger test than
   normalisation alone, since it probes the shape of the distribution.
3. **The 1s peak at 0.999 a₀** — you have *measured the Bohr radius* from your own
   wavefunction, recovering Bohr's 1913 result from Schrödinger's 1926 equation.

Note also that the integral uses r²|R|² — the radial probability, complete with
the volume factor. Integrating |R|² alone would not give 1, and knowing why is
the difference between following a recipe and understanding it.

---

## 18.4 The visualisations

### 2D slices

```python
extent = 6*n
g = np.linspace(-extent, extent, 300)
X, Z = np.meshgrid(g, g)
density = psi(n, l, m, X, 0*X, Z)**2
ax.pcolormesh(X, Z, density, cmap='inferno',
              norm=plt.matplotlib.colors.PowerNorm(0.4))
```

- `meshgrid` builds the (x,z) coordinate grid; `0*X` sets y = 0 — the x–z plane.
- `extent = 6*n` scales the window with the orbital, since size grows as n².
- `PowerNorm(0.4)` compresses the dynamic range so faint outer lobes are visible
  (§7.7) — a display choice, stated as such.

Read the gallery: 1s a ball; 2s a ball with a shell (one radial node); 2p two
lobes with a nodal plane; 3d the four-lobed clover. Count the nodes in each and
check against n−1 total.

### 3D Monte Carlo clouds

```python
rng = np.random.default_rng(0)
pts = rng.uniform(-extent, extent, (400000, 3))
dens = psi(n, l, m, pts[:,0], pts[:,1], pts[:,2])**2
keep = rng.uniform(0, dens.max(), 400000) < dens
P = pts[keep][:8000]
ax.scatter(P[:,0], P[:,1], P[:,2], s=1, alpha=0.25, c=P[:,2], cmap='coolwarm')
```

Rejection sampling (§8.7): scatter candidates uniformly, keep each with
probability proportional to the local density. The survivors are a true sample
of |ψ|².

Philosophically this is the *honest* orbital picture: quantum mechanics gives a
distribution, and these are draws from it. An isosurface — the usual textbook
picture — is a single arbitrary contour, prettier but less truthful. You should
be able to defend the choice either way.

### Morphing between m states

```python
w = 0.5 - 0.5*np.cos(np.pi*t)          # smooth 0 -> 1
d = (1-w)*d1 + w*d2
```

A linear interpolation between two densities, with a cosine **easing** so the
transition accelerates and decelerates rather than jerking. Note honestly what
this is: a *visual* interpolation between two stationary states, not a physical
time evolution (a true superposition would need complex amplitudes and would
show interference). Saying that out loud is better than letting a judge wonder.

### LCAO: making a molecule

```python
p1 = psi(1, 0, 0, X, 0*X, Z - R/2)     # atom A
p2 = psi(1, 0, 0, X, 0*X, Z + R/2)     # atom B
norm_p = 1/np.sqrt(2 + 2*np.exp(-R)*(1 + R + R**2/3))
norm_m = 1/np.sqrt(2 - 2*np.exp(-R)*(1 + R + R**2/3))
bond = (norm_p*(p1 + p2))**2
anti = (norm_m*(p1 - p2))**2
```

**Linear Combination of Atomic Orbitals.** Two hydrogen 1s orbitals centred at
±R/2:

- **Sum** → *bonding* orbital σ_g: constructive interference between the nuclei,
  electron density piles up in the middle, pulling the nuclei together. That
  accumulation *is* the covalent bond.
- **Difference** → *antibonding* σ_u*: a nodal plane exactly halfway, zero
  density between the nuclei, higher energy.

The normalisation constants include the **overlap integral**
S = e^{−R}(1 + R + R²/3), the exact analytic result for two 1s orbitals — so the
plotted densities are properly normalised at every bond length.

Drag the slider: at large R you see two separate atoms; as they approach, the
bonding orbital's central density grows. You are watching a chemical bond form,
built from a differential equation. This is the beginning of quantum chemistry,
and it's a genuine step beyond what the task asked for.

---

## Exercises

1. Verify normalisation for n = 4, l = 0…3. Does it hold to six decimals?
2. Count radial nodes in the 3s, 3p and 3d radial functions by finding sign
   changes in `radial(...)`. Do they match n−l−1?
3. Plot the 1s density along a line through the nucleus *and* the radial
   probability r²|R|² on the same figure. Explain to someone why one peaks at 0
   and the other at a₀.
4. Set Z = 2 (He⁺). By what factor should ⟨r⟩ shrink? Verify numerically.
5. Add the y–z and x–y slice planes as options and confirm that the m = 1 and
   m = 2 orbitals look different in each.
6. Extend the LCAO to **H₃⁺**: three 1s orbitals at the corners of an equilateral
   triangle. Plot the fully symmetric combination. (Normalisation can be
   approximate here — state that you've approximated it.)
7. Build a p_x + p_z hybrid ("sp hybrid") and plot it. Which way does it point?
8. **Stretch:** compute the LCAO bonding energy as a function of R by evaluating
   the relevant integrals numerically, and find the equilibrium bond length.
   Compare with the true H₂⁺ value of 2.00 a₀.

Solutions: `solutions/ch18_solutions.py`

---

## What you now know

- Separation of variables, the three quantum numbers, and what each controls.
- Radial and angular parts; nodes; real vs complex spherical harmonics.
- |ψ|² versus r²|R|² — the distinction that explains the Bohr radius.
- Implementing Laguerre and Legendre from recurrences with simultaneous assignment.
- Three-way numerical verification: normalisation, ⟨r⟩, and the 1s peak.
- meshgrid slices, PowerNorm display scaling, Monte Carlo clouds.
- LCAO: bonding and antibonding orbitals, the overlap integral, and how a
  covalent bond appears out of interference.

**End of Part 3.** Every physics model in the project is now yours.

Next: [Chapter 19 — Widgets and interactivity](19_widgets.md)
