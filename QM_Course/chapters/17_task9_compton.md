# Chapter 17 — Task 9: Compton scattering

**The task:** *"Plot fractional wavelength shift Δλ/λ, electron recoil speed v and
electron recoil angle φ vs photon scattering angle θ."*

**Beyond it:** three photon energies spanning X-ray to gamma, fully relativistic
recoil speeds, and a built-in energy-conservation test that closes to machine
precision at every angle.

---

## 17.1 The physics

### Why Compton mattered

By 1923 the photon was still contentious. Planck had quantised emission and
Einstein had explained the photoelectric effect, but many physicists regarded
quantisation as a property of *matter's interaction* with light rather than of
light itself.

Compton scattered X-rays off graphite and found the scattered radiation had a
*longer wavelength*, shifted by an amount depending only on the scattering
angle. No wave theory can do that: a wave scattering off an electron re-radiates
at the same frequency. But treat it as a **billiard-ball collision between a
photon and an electron** — conserving relativistic energy and momentum — and the
result falls out exactly. The photon was real.

### The derivation

A photon of wavelength λ carries energy E = hc/λ and momentum p = h/λ. It hits a
stationary electron (rest energy mₑc²), scatters through angle θ, and the
electron recoils at angle φ.

**Energy conservation:**

  hc/λ + mₑc² = hc/λ′ + γmₑc²

**Momentum conservation** (two components):

  h/λ = (h/λ′)cos θ + γmₑv cos φ
  0 = (h/λ′)sin θ − γmₑv sin φ

Three equations. Eliminate v and φ (square and add the momentum equations, then
substitute the energy equation) and you get, remarkably simply:

  **λ′ − λ = (h/mₑc)(1 − cos θ)**

The prefactor is the **Compton wavelength** of the electron:

  λ_C = h/(mₑc) = 2.426 pm

Notes worth making:

- The shift is **absolute**, not fractional: it depends only on θ, not on λ.
  So the *fractional* shift Δλ/λ is large for short-wavelength (energetic)
  photons and negligible for visible light — which is why we never notice
  Compton scattering in daily life.
- Maximum shift at θ = 180° (backscatter): Δλ = 2λ_C = 4.85 pm.
- At θ = 0 (no deflection) nothing happens, as it must.

### Electron recoil

Energy taken by the electron:

  K = hc/λ − hc/λ′

Relativistic speed from the Lorentz factor:

  γ = 1 + K/(mₑc²),  **v = c√(1 − 1/γ²)**

Using the non-relativistic ½mv² here would be *wrong* at gamma energies — for a
511 keV photon the backscattered electron reaches 0.8c, where relativistic
corrections are enormous. Getting this right is a genuine discriminator between
a careful entry and a sloppy one.

The recoil angle comes from the momentum triangle:

  tan φ = (sin θ/λ′) / (1/λ − cos θ/λ′)

and φ → 90° as θ → 0 (a barely-deflected photon gives the electron a sideways
nudge), φ → 0 as θ → 180° (backscattered photon drives the electron straight
forward).

---

## 17.2 The code

### Constants and the Compton wavelength

```python
h = 6.62607015e-34
c = 2.99792458e8
e = 1.602176634e-19
me = 9.10938356e-31

lam_C = h / (me * c)
print(f'Compton wavelength λ_C = h/(mₑc) = {lam_C*1e12:.3f} pm')   # 2.426 pm
```

Computed, not typed. Same principle as E₀ in Chapter 13.

### Three beams

```python
beams = {"Compton's X-rays (71.1 pm, 17.4 keV)": 71.1e-12,
         'γ-ray, E = 511 keV': h*c/(0.511e6*e),
         'γ-ray, E = 1.24 MeV': h*c/(1.24e6*e)}
```

Chosen deliberately:

- **71.1 pm** is the actual molybdenum Kα line Compton used — historical fidelity.
- **511 keV** is the electron rest energy, so λ = λ_C exactly and the maximum
  fractional shift is *exactly* 2. A built-in check.
- **1.24 MeV** pushes into the strongly relativistic regime (v = 0.94c).

Writing `h*c/(0.511e6*e)` converts an energy in eV to a wavelength inline — no
magic numbers.

### The calculation

```python
theta = np.linspace(0.001, np.pi, 500)

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
```

Every line is one physics statement, evaluated for all 500 angles at once.

Two technical points:

**Why `theta` starts at 0.001 rather than 0.** At exactly θ = 0 the recoil angle
is a 0/0 limit and the electron speed is zero; starting a hair above avoids the
ambiguity without visibly changing the plot. Sidestepping a removable singularity
like this is normal practice — but you should know it's there and say so.

**`np.arctan2(y, x)` rather than `arctan(y/x)`** — it takes the two components
separately and therefore returns the angle in the correct quadrant (§6.4). With
plain `arctan` the recoil angle would flip sign in part of the range.

### The self-test

```python
check = E0 - (E1[-1] + KE[-1])
print(f'  energy conservation residual at 180 deg: {check:.2e} J (should be ~0)')
```

Output for all three beams: `0.00e+00`.

This is a **unit test built into a physics program**. It verifies that the
energies you computed actually satisfy the conservation law you started from —
catching algebra slips, unit errors and typos automatically. Professional
scientific code is full of these; student code almost never is, and judges
notice.

Printed results:

```
Compton's X-rays: max fractional shift 0.0683, max recoil speed 0.0659 c
γ-ray 511 keV:    max fractional shift 2.0000, max recoil speed 0.8000 c
γ-ray 1.24 MeV:   max fractional shift 4.8532, max recoil speed 0.9433 c
```

The bold ones are exact-by-theory checks: 511 keV must give exactly 2.0000 and
exactly 0.800c. Getting those digits right is evidence the whole relativistic
chain is correct.

---

## 17.3 Reading the three panels

**Fractional shift** rises monotonically with θ, saturating at 2λ_C/λ₀. The
X-ray curve barely lifts off zero — 7% — while the 1.24 MeV curve reaches 4.85:
the scattered photon has nearly six times its original wavelength and has lost
most of its energy.

**Recoil speed** rises steeply then flattens as it approaches c — the relativistic
speed limit made visible. A non-relativistic calculation would sail past c, which
is exactly the sort of nonsense a check catches.

**Recoil angle** falls from 90° to 0° in all cases; the curvature differs because
higher-energy photons transfer momentum more forwards.

---

## Exercises

1. Verify Δλ at θ = 90° equals λ_C exactly (2.426 pm) for all three beams. Why
   is it independent of λ₀?
2. Compute the fractional shift for **visible** light (500 nm) at 180°. Express
   it in parts per million. Why is Compton scattering irrelevant in optics?
3. Add a fourth beam at 100 keV and find the angle at which the electron takes
   half the photon's energy.
4. Plot the *scattered photon energy* against θ for all three beams and identify
   the "Compton edge" — the maximum energy transferred to the electron. This
   feature is directly visible in real gamma-ray spectra.
5. Verify momentum conservation numerically as a second self-test: compute the
   total x and y momentum before and after for every angle and print the largest
   residual.
6. Show that the non-relativistic formula v = √(2K/mₑ) exceeds c for the 1.24 MeV
   beam beyond some angle. At which angle does it break down?
7. **Stretch:** implement the Klein–Nishina formula for the *probability* of
   scattering at each angle and plot the angular distribution. This is what
   determines how often each θ actually occurs.

Solutions: `solutions/ch17_solutions.py`

---

## What you now know

- Why Compton's experiment established the photon as a particle.
- The full derivation of Δλ = λ_C(1 − cos θ) from relativistic conservation laws.
- Compton wavelength; absolute vs fractional shift; the 511 keV special case.
- Relativistic recoil via the Lorentz factor, and why the classical formula fails.
- `arctan2` for correct quadrants; avoiding removable singularities deliberately.
- Building conservation-law self-tests into physics code.

Next: [Chapter 18 — Task 10: Hydrogen orbitals](18_task10_orbitals.md)
