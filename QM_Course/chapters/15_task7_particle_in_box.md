# Chapter 15 — Task 7: Particle in a box and the uncertainty principle

**The task:** *"Particle-in-a-box solution to the Schrödinger Equation. Plot energy
vs quantum number, and probability densities |ψ|² vs displacement x in the box.
EXTENSION: Write up the model, and show that a particle in the box obeys the
Uncertainty Principle i.e. Δx Δp ≥ ħ/2."*

**Beyond it:** the uncertainty extension done by genuine numerical integration
over ten states, matching the exact analytic value to four significant figures.

---

## 15.1 The physics

### The Schrödinger equation

The equation of motion of quantum mechanics. Time-independent, one dimension:

  −(ħ²/2m) d²ψ/dx² + V(x)ψ = Eψ

ψ(x) is the **wavefunction**; |ψ(x)|² is the probability density for finding the
particle at x (Born's rule). The equation is an *eigenvalue problem*: only
certain E have acceptable solutions, and those discrete E are the allowed
energies. Quantisation isn't an extra assumption — it falls out of the boundary
conditions, exactly as the allowed frequencies of a guitar string do.

### Solving the box

Infinite walls at x = 0 and x = a; V = 0 inside. Inside the box:

  d²ψ/dx² = −k²ψ  with  k² = 2mE/ħ²

General solution ψ = A sin(kx) + B cos(kx). The wavefunction must be continuous
and vanish at the walls:

- ψ(0) = 0 forces B = 0
- ψ(a) = 0 forces sin(ka) = 0, so **ka = nπ** for integer n ≥ 1

Therefore k = nπ/a, and

  **Eₙ = ħ²k²/2m = n²h²/(8ma²)**

**Normalisation:** ∫₀^a |ψ|² dx = 1 gives A = √(2/a), so

  **ψₙ(x) = √(2/a) sin(nπx/a)**

Three consequences worth stating:

1. **Energy is quantised** — only n² multiples of E₁ are allowed.
2. **Zero-point energy:** E₁ ≠ 0. n = 0 would mean ψ ≡ 0 — no particle at all.
   A confined quantum particle can never be at rest. This is uncertainty
   made concrete.
3. **Nodes:** ψₙ has n−1 zeros inside the box, exactly like harmonics on a string.

For an electron in a 1 nm box, E₁ = 0.376 eV — comparable to chemical energies,
which is why this toy model describes quantum dots and conjugated molecules
surprisingly well.

### The uncertainty principle, properly

Heisenberg: **Δx Δp ≥ ħ/2**, where Δ means standard deviation:

  Δx = √(⟨x²⟩ − ⟨x⟩²),  Δp = √(⟨p²⟩ − ⟨p⟩²)

with expectation values ⟨f⟩ = ∫ ψ* f ψ dx.

For our box:

- ⟨x⟩ = a/2 by symmetry.
- ⟨x²⟩ = a²(1/3 − 1/(2n²π²)), so **Δx = a√(1/12 − 1/(2n²π²))**
- ⟨p⟩ = 0 (equal amplitudes moving both ways — a standing wave)
- ⟨p²⟩ = (nπħ/a)², so **Δp = nπħ/a**

Multiply:

  **Δx·Δp = ħ · (nπ/2)·√(1/3 − 2/(n²π²))**

For n = 1 this evaluates to **0.5678 ħ** — just above the Heisenberg bound of
0.5 ħ, and growing with n. The ground state of the box very nearly saturates the
uncertainty principle. (The state that exactly saturates it is the Gaussian, but
a Gaussian can't satisfy the box's boundary conditions.)

---

## 15.2 The code

### Energy levels

```python
h = 6.62607015e-34
hbar = 1.054571817e-34
e = 1.602176634e-19
me = 9.1093837015e-31
a = 1e-9                      # 1 nm box

def energy_eV(n):
    return n**2 * h**2 / (8 * me * a**2) / e

ns = np.arange(1, 8)
plt.plot(ns, energy_eV(ns), 'o', ms=7)
nfit = np.linspace(1, 7, 100)
plt.plot(nfit, energy_eV(1)*nfit**2, '--', lw=1, label='$E_n = E_1 n^2$')
for n in ns:
    plt.annotate(f'{energy_eV(n):.2f} eV', (n, energy_eV(n)),
                 textcoords='offset points', xytext=(8, -3))
```

The dashed curve is E₁n² drawn *continuously* — the discrete points must land on
it, which makes the n² scaling visible rather than asserted. `annotate` labels
each level with its value; `offset points` shifts the text a few pixels so it
doesn't sit on the marker.

Note `energy_eV(ns)` works on the whole array at once — vectorisation again.

### Probability densities

```python
x = np.linspace(0, a, 2000)
for n in range(1, 5):
    psi2 = (2/a) * np.sin(n*np.pi*x/a)**2
    plt.plot(x*1e9, psi2/1e9 + 3*(n-1), label=f'n = {n}')
    plt.axhline(3*(n-1), color='grey', lw=0.5)
```

`(2/a)·sin²(nπx/a)` is |ψₙ|² directly from the analytic solution. The
`+ 3*(n-1)` offsets each curve vertically so they stack instead of overlapping —
a standard presentation trick, with a faint baseline drawn for each. The `/1e9`
converts the density to per-nanometre so the numbers are human-sized.

Look at the result: n=1 is a single hump (most likely in the middle), n=2 has a
node exactly at the centre — the particle is *never* found there, despite being
found on both sides. That is quantum mechanics with no interpretation required.

### The uncertainty calculation — numerical integration

```python
for n in range(1, 11):
    psi = np.sqrt(2/a) * np.sin(n*np.pi*x/a)
    prob = psi**2
    mean_x = np.trapezoid(x*prob, x)
    mean_x2 = np.trapezoid(x**2*prob, x)
    dx = np.sqrt(mean_x2 - mean_x**2)
    dp = n * np.pi * hbar / a
    prod = dx*dp/hbar
    print(f'{n:>3} {dx:>12.3e} {dp:>13.3e} {prod:>11.4f} {"yes" if prod >= 0.5 else "NO":>8}')
```

**`np.trapezoid(y, x)`** approximates ∫y dx using the trapezium rule: it joins
consecutive sample points with straight lines and sums the trapezium areas,

  ∫ y dx ≈ Σ (yᵢ + yᵢ₊₁)/2 · (xᵢ₊₁ − xᵢ)

With 2000 points across the box the error is negligible — and *checking* that it
is negligible is the convergence test in exercise 4. (Older numpy calls this
`np.trapz`; it was renamed, hence the deprecation warning you may see on older
code.)

So `mean_x = ∫ x|ψ|²dx` is a genuine expectation-value integral, computed
numerically, not looked up. Δp uses the analytic result nπħ/a, which is exact for
this system.

Output:

```
  n       Δx (m)   Δp (kg m/s)     Δx·Δp/ħ    ≥ ½ ?
  1    1.808e-10     3.313e-25      0.5679      yes
  2    2.658e-10     6.626e-25      1.6703      yes
  3    2.788e-10     9.939e-25      2.6272      yes
 ...
 10    2.878e-10     3.313e-24      9.0414      yes
```

Compare n = 1: numerics give 0.5679, analytic gives 0.5678. Four-significant-
figure agreement between an integral computed on a grid and a closed-form
expression — that is a *validated* numerical method.

Then the figure that makes it visible:

```python
plt.plot(range(1, 11), products, 'o-', label='$\\Delta x\\,\\Delta p/\\hbar$')
plt.axhline(0.5, color='r', ls='--', label='Heisenberg limit $1/2$')
```

Every point sits above the red line. Notice too that Δx saturates around
0.288a ≈ a/√12 for large n — the particle spreads out uniformly, approaching the
*classical* result of a particle equally likely to be anywhere in the box. That's
the **correspondence principle** appearing in your own data.

---

## 15.3 Numerical integration: a short primer

Three methods you should know:

| Method | Idea | Error |
|---|---|---|
| Rectangle (Riemann) | sum f(xᵢ)·Δx | O(Δx) |
| **Trapezium** | join points with straight lines | O(Δx²) |
| Simpson | fit parabolas through triples | O(Δx⁴) |

Trapezium is the sweet spot for smooth functions on a fine grid: one line of
code, no assumptions, and error falling as the square of the spacing. Halving
the spacing quarters the error — which is exactly what exercise 4 asks you to
demonstrate.

The general rule: **whenever you compute an integral numerically, also check it
converges.** Run at two resolutions; if the answer moves in the fourth
significant figure, quote three.

---

## Exercises

1. Compute E₁ for an electron in boxes of 0.5, 1 and 2 nm. How does E scale with
   a? Explain physically why smaller boxes mean higher energies.
2. Compute the photon wavelength emitted for the n=2 → n=1 transition in a 1 nm
   box. Which part of the spectrum is that?
3. Verify normalisation numerically: integrate |ψₙ|² over the box for n = 1…5 and
   confirm each gives 1.000000.
4. **Convergence study:** compute Δx·Δp for n = 1 using 50, 200, 1000, 5000 and
   20000 grid points. Plot the error against the number of points on log axes.
   What power law do you get, and does it match the O(Δx²) claim?
5. Derive ⟨x²⟩ for the box analytically (integrate x²·(2/a)sin²(nπx/a)) and
   confirm your numerical value.
6. Compute ⟨p⟩ numerically using the momentum operator −iħ d/dx with
   `np.gradient` and confirm it is zero. Why must it be?
7. **Stretch:** solve the box numerically as a matrix eigenvalue problem —
   discretise the second derivative and use `np.linalg.eigh` — and compare the
   first five eigenvalues with n²E₁. This is how real quantum problems are
   solved when no analytic answer exists.

Solutions: `solutions/ch15_solutions.py`

---

## What you now know

- The Schrödinger equation as an eigenvalue problem; quantisation from boundary
  conditions.
- Full derivation of Eₙ and ψₙ, normalisation, nodes, zero-point energy.
- Expectation values, standard deviations, and the exact Δx·Δp for the box.
- The trapezium rule, its error order, and why convergence must be checked.
- Numerical results matching analytic ones to four figures = validation.
- The correspondence principle visible in Δx as n grows.

Next: [Chapter 16 — Task 8: Quantum cryptography](16_task8_cryptography.md)
