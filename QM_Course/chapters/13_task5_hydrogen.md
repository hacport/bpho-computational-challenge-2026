# Chapter 13 — Task 5: The hydrogen spectrum and Bohr's model

**The task:** *"Hydrogen emission spectrum and Bohr's model of a hydrogenic atom.
Create a graph of photon energy vs wavelength for photon emissions from hydrogen
atoms due to transitions between electron energy levels."*

**Beyond it:** computing the ground-state energy from fundamental constants (no
Rydberg constant typed in), comparison against measured laboratory wavelengths
to better than 0.04%, series limits marked, and a true-colour spectroscope view
using CIE colorimetry.

---

## 13.1 The physics

### The puzzle

Heated hydrogen emits light at a few sharp, precise wavelengths — not a
continuous rainbow. In the visible: 656.3 nm (red), 486.1 nm (blue-green),
434.0 nm (violet), 410.2 nm (violet). Balmer found in 1885 that these fit a
numerical formula, but nobody knew *why*.

Classical physics was worse than silent: an orbiting electron accelerates, must
radiate, and should spiral into the nucleus in about 10⁻¹¹ s. **Classically,
atoms cannot exist.**

### Bohr's postulates (1913)

1. Electrons occupy **stationary states** of fixed energy and do not radiate
   while in them.
2. Angular momentum is quantised: L = nħ.
3. Light is emitted when an electron jumps *between* states, carrying exactly the
   energy difference: hf = E_i − E_f.

### Deriving the energy levels (worth doing once)

Balance Coulomb attraction against circular motion:

  (1/4πε₀)(e²/r²) = mv²/r

Quantise angular momentum: mvr = nħ. Solve the pair for r and v:

  r_n = 4πε₀ħ²n²/(m e²) = a₀n²,  with a₀ = 5.29 × 10⁻¹¹ m (the **Bohr radius**)

Total energy E = KE + PE = ½mv² − e²/4πε₀r gives

  **Eₙ = − mₑe⁴ / (8ε₀²h²) · 1/n² = −13.6 eV / n²**

The prefactor mₑe⁴/8ε₀²h² is the **Rydberg energy**, E₀ ≈ 13.606 eV.

A transition from n₂ down to n₁ emits

  **E_photon = E₀(1/n₁² − 1/n₂²)**,  λ = hc/E_photon

Series are named by their lower level: n₁ = 1 Lyman (UV), 2 Balmer (visible),
3 Paschen (IR), 4 Brackett, 5 Pfund.

Each series has a **limit**: n₂ → ∞ gives E = E₀/n₁², the highest-energy (shortest
wavelength) photon of that series — the ionisation energy from level n₁.

### Honesty about Bohr

Bohr's model gets hydrogen's *energies* right and everything else wrong: it
fails for multi-electron atoms, says nothing about line intensities, and its
picture of orbits contradicts the uncertainty principle (Chapter 15). The
Schrödinger equation (Chapter 18) supersedes it while reproducing the same
energies. Knowing the limits of a model is part of knowing the model.

---

## 13.2 The code

### Computing E₀ from scratch

```python
h = 6.62607015e-34
c = 2.99792458e8
e = 1.602176634e-19
me = 9.1093837015e-31
eps0 = 8.8541878128e-12

E0 = me * e**4 / (8 * eps0**2 * h**2)
print(f'ground state energy E1 = {-E0/e:.2f} eV')      # -13.61 eV
```

**Do not type 13.6 in.** Building E₀ from the five fundamental constants means
the model is *derived*, and the printed −13.61 eV is then a result rather than
an input. This is the difference between a model and a lookup table.

### Generating the series

```python
series = {'Lyman (n1=1)': (1, 'purple'), 'Balmer (n1=2)': (2, 'teal'),
          'Paschen (n1=3)': (3, 'orange'), 'Brackett (n1=4)': (4, 'brown')}

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
```

Notes:

- The dictionary values are **tuples** `(n1, colour)`, unpacked in the loop
  header: `for name, (n1, colour) in ...` — nested unpacking (§4.3).
- `range(n1+1, n1+15)` — transitions must come from a *higher* level, hence
  starting at n1+1.
- The dotted `axvline` marks each series limit, computed by setting n₂ → ∞.

### Log scale — a deliberate choice

```python
plt.xscale('log')
```

Lyman lines sit near 100 nm, Pfund lines near 7500 nm — a factor of 75. On a
linear axis, all the visible structure collapses into a sliver. A log axis shows
every series clearly, and the fact that each series occupies its own band
becomes obvious.

### The comparison with laboratory data

```python
measured_balmer = {656.3: 'H-alpha (red)', 486.1: 'H-beta (blue-green)',
                   434.0: 'H-gamma (violet)', 410.2: 'H-delta (violet)'}

for n2 in [3, 4, 5, 6]:
    E_photon = E0 * (1/4 - 1/n2**2)
    lam_nm = h*c / E_photon * 1e9
    meas = list(measured_balmer.keys())[n2-3]
    print(f'  n={n2} -> 2:  model {lam_nm:.1f} nm,  measured {meas} nm '
          f'({measured_balmer[meas]}),  diff {abs(lam_nm-meas)/meas*100:.3f} %')
```

Output:

```
n=3 -> 2:  model 656.1 nm,  measured 656.3 nm (H-alpha (red)),  diff 0.029 %
n=4 -> 2:  model 486.0 nm,  measured 486.1 nm (H-beta),         diff 0.019 %
n=5 -> 2:  model 433.9 nm,  measured 434.0 nm (H-gamma),        diff 0.015 %
n=6 -> 2:  model 410.1 nm,  measured 410.2 nm (H-delta),        diff 0.032 %
```

**This table is the point of the task.** Anyone can plot a formula; this
compares a computed model with the physical world and quantifies the agreement.

**Where does the residual 0.03% come from?** Two separate effects, and chasing
them down is a lesson in itself.

**1. The reduced mass.** Bohr assumes an infinitely heavy nucleus. In reality the
electron and proton orbit their common centre of mass, so the correct mass is
μ = mₑm_p/(mₑ+m_p) ≈ 0.99946 mₑ — a 0.054% correction.

**2. Air versus vacuum.** The familiar values 656.3 nm and 486.1 nm are
*air* wavelengths, measured in a laboratory at atmospheric pressure. Your model
computes *vacuum* wavelengths. Air's refractive index (1.000277) makes vacuum
wavelengths 0.028% longer — comparable to the discrepancy you're trying to
explain.

Apply both corrections and compare like with like:

```
 n     plain   reduced  measured    error
 3    656.11    656.47    656.46  0.0012%
 4    486.01    486.27    486.26  0.0019%
 5    433.94    434.17    434.17  0.0006%
 6    410.07    410.29    410.28  0.0024%
```

Agreement improves from 0.03% to about 0.001% — a twentyfold improvement, and now
limited only by the precision of the constants.

**The general lesson matters more than the numbers:** when a model and a
measurement disagree slightly, check whether they are even *the same quantity*
before blaming the model. Half of experimental physics is that check.
(This is exercise 3.)

### The spectroscope view

```python
from cie_color import wavelength_to_rgb

fig2, ax2 = plt.subplots(figsize=(10, 2.6))
ax2.set_facecolor('black')
for n2 in range(3, 20):
    E_photon = E0 * (1/4 - 1/n2**2)
    lam_nm = h*c / E_photon * 1e9
    if 380 < lam_nm < 740:
        ax2.axvline(lam_nm, color=wavelength_to_rgb(lam_nm), lw=3)
```

Each Balmer line is drawn at its true wavelength in its true colour, computed
from CIE colour-matching functions (Chapter 21). The result looks like what you
would see through a real spectroscope: a red line, a cyan line, and violet lines
crowding towards the series limit. The crowding is itself physics — energy
levels bunch up as n grows, since Eₙ ∝ 1/n².

---

## Exercises

1. Print the wavelength of the first four Lyman lines. Which part of the spectrum
   are they in? Why can't you see hydrogen's strongest transition?
2. Compute the ionisation energy of hydrogen from the ground state (n=1 → ∞) and
   compare with the accepted 13.598 eV.
3. Redo the Balmer comparison using the reduced mass μ = mₑm_p/(mₑ+m_p) with
   m_p = 1.6726219e-27 kg. By how much do the errors improve?
4. Add the Pfund series (n₁ = 5) to the plot with its limit.
5. Hydrogenic ions: energies scale as Z². Compute the Balmer-equivalent lines for
   He⁺ (Z = 2) and state where they fall.
6. Deuterium has a heavier nucleus (m ≈ 2m_p). Compute the *isotope shift* of the
   H-alpha line — the wavelength difference between hydrogen and deuterium. (This
   is how deuterium was discovered in 1931.)
7. **Break it:** replace `E0` with a hard-coded 13.6 eV and see how the printed
   comparison changes. Which digits move?

Solutions: `solutions/ch13_solutions.py`

---

## What you now know

- Why classical atoms should collapse, and Bohr's postulates.
- The derivation of Eₙ = −13.6 eV/n² and the Bohr radius.
- Series, series limits, and why lines crowd towards them.
- Computing E₀ from fundamental constants, not looking it up.
- Comparing with laboratory data and *explaining* the residual via reduced mass.
- Log axes for multi-decade data; true-colour spectral rendering.

Next: [Chapter 14 — Task 6: Electron diffraction](14_task6_diffraction.md)
