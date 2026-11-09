# Chapter 14 — Task 6: Electron diffraction

**The task:** *"Create a computer model of the 'electron wave' rings on a phosphor
screen with accelerating voltage V as a variable (1kV to 5kV). Assume atomic
spacings d are layer spacings of graphite e.g. 0.123nm or 0.213nm. Check your
model by generating a 1/√V vs 1/sin θ straight line graph, where ring radius is
x = r sin 2θ and the tube radius is r = 65 mm."*

**Beyond it:** recovering both graphite spacings from the fitted gradients —
running the physics backwards to *measure* the atomic structure.

---

## 14.1 The physics

### Matter waves

De Broglie (1924) proposed that particles have a wavelength

  **λ = h/p**

Bizarre, but testable: if electrons are waves, they should **diffract**.
Davisson and Germer confirmed it in 1927 by scattering electrons off nickel;
G. P. Thomson did it with thin foils the same year. (Delicious detail: J. J.
Thomson won a Nobel for showing the electron is a particle, and his son G. P.
won one for showing it's a wave. Both were right.)

### The electron's wavelength in the tube

An electron accelerated through voltage V gains kinetic energy eV:

  ½mv² = eV  ⟹  p = mv = √(2mₑeV)

so

  **λ = h/√(2mₑeV)**

Numerically: λ(nm) ≈ 1.226/√V(volts). At 1 kV, λ ≈ 39 pm — comparable to atomic
spacings, which is exactly the condition for diffraction to be observable.
Higher voltage → shorter wavelength → *smaller* diffraction angles.

### Bragg's law and the geometry of the rings

Layers of graphite atoms separated by d reflect constructively when

  **2d sin θ = nλ**  (we use first order, n = 1)

Graphite is polycrystalline in the tube: countless tiny crystals at every
orientation. Whichever ones happen to satisfy Bragg's condition scatter, and
because all orientations are present, the scattered electrons form a **cone** —
which lands on the screen as a **ring**.

The scattering angle is 2θ (deviation from the straight-through beam is twice the
Bragg angle), so on a spherical screen of radius r the ring radius is

  **x = r sin 2θ**

Two spacings (0.213 nm and 0.123 nm) give two rings. The *smaller* spacing
diffracts through the *larger* angle, so d = 0.123 nm produces the **outer** ring.

### The linearising check the task asks for

From Bragg: sin θ = λ/2d, and λ ∝ 1/√V. Therefore

  sin θ = h/(2d√(2mₑe)) · 1/√V

so a plot of **1/√V against sin θ** is a straight line through the origin, with

  gradient = 2d√(2mₑe)/h

**Rearranging that gradient gives d.** That's the extension: fit the line, then
solve for the atomic spacing. You measure the structure of graphite from a
simulated screen.

Linearising is a core experimental technique: choose axes on which theory
predicts a straight line, because the human eye is superb at spotting deviations
from straightness and hopeless at judging curves.

---

## 14.2 The code

### The model

```python
h = 6.62607015e-34
e = 1.602176634e-19
me = 9.1093837015e-31

r_tube = 65e-3
d1, d2 = 0.213e-9, 0.123e-9

def ring_radius(V, d):
    lam = h / np.sqrt(2 * me * e * V)
    theta = np.arcsin(lam / (2 * d))
    return r_tube * np.sin(2 * theta)
```

Three lines, three pieces of physics: de Broglie, Bragg, geometry. Written this
way the function is checkable against a textbook line by line.

`np.arcsin` returns radians (as all numpy trig does). If the argument ever
exceeded 1 you'd get NaN — physically that would mean "no diffraction possible
at this wavelength", which is worth knowing (exercise 6).

### The screen views

```python
fig, axes = plt.subplots(1, 3, figsize=(12, 4.2))
for ax, V in zip(axes, [1000, 3000, 5000]):
    for d, colour in [(d1, 'lime'), (d2, 'cyan')]:
        x = ring_radius(V, d)
        ax.add_patch(Circle((0, 0), x*1e3, fill=False, color=colour, lw=2))
    ax.add_patch(Circle((0, 0), 1.5, color='white'))     # undiffracted beam
    ax.set_facecolor('darkgreen')
    ax.set_xlim(-40, 40); ax.set_ylim(-40, 40)
    ax.set_aspect('equal')
    ax.set_title(f'V = {V/1000:.0f} kV')
```

- `zip(axes, [...])` pairs each panel with its voltage (§7.4).
- Circles are **patches in data coordinates**, so a ring of radius 6.86 mm is
  drawn at exactly 6.86 mm on the axes (§7.6). Never fake it with markers.
- `x*1e3` converts metres to millimetres to match the axis units.
- The dark green background and white central spot imitate the phosphor screen —
  cheap, and it makes the figure instantly readable as an experiment.
- `set_aspect('equal')` is non-negotiable: rings must be circular.

Result: rings visibly shrink as voltage rises, because faster electrons have
shorter wavelengths and diffract less. The cyan (d = 0.123 nm) ring is always
outside the lime one.

### The verification and the backwards step

```python
V = np.linspace(1000, 5000, 30)
inv_sqrtV = 1 / np.sqrt(V)

for d, name in [(d1, 'd = 0.213 nm'), (d2, 'd = 0.123 nm')]:
    lam = h / np.sqrt(2 * me * e * V)
    sin_theta = lam / (2 * d)
    m_fit, c_fit = np.polyfit(sin_theta, inv_sqrtV, 1)
    d_recovered = m_fit * h / (2 * np.sqrt(2 * me * e))
    plt.plot(sin_theta, inv_sqrtV, 'o', ms=4, label=name)
    plt.plot(sin_theta, m_fit*sin_theta + c_fit, '-', lw=0.8)
    print(f'  {name}:  gradient = {m_fit:.4f},  intercept = {c_fit:.2e}')
    print(f'  atomic spacing recovered from gradient: {d_recovered*1e9:.3f} nm')
```

Output:

```
d = 0.213 nm:  gradient = 0.3474,  intercept = 5.67e-18
atomic spacing recovered from gradient: 0.213 nm

d = 0.123 nm:  gradient = 0.2006,  intercept = 5.67e-18
atomic spacing recovered from gradient: 0.123 nm
```

Two things to notice:

**The intercept is 5.67e-18 — that is zero.** Not "close to zero": floating-point
arithmetic can't produce exact zeros through this many operations (§2.4). An
intercept 17 orders of magnitude below the data range is a numerical zero, and
saying so demonstrates you understand your own numerics.

**The recovery is exact to three decimals.** The line `d_recovered = m_fit * h /
(2*np.sqrt(2*me*e))` is the gradient formula rearranged for d. You put d in at
the start, ran it through de Broglie, Bragg, geometry and a least-squares fit,
and got d back. That round trip is a proof of internal consistency, and it's the
closest a simulation comes to a laboratory measurement.

---

## 14.3 What a real experiment would add

Your model produces infinitely thin rings from a perfect polycrystal. A real
Teltron tube shows:

- **Ring thickness** — finite beam width, crystallite size, and detector
  resolution
- **Intensity variation** — structure factors mean some rings are brighter
- **Higher orders** (n = 2, 3) — fainter rings at larger angles
- **Background glow** — inelastic scattering

Adding a Gaussian brightness profile across each ring is the most rewarding
extension (exercise 4) and takes about six lines.

---

## Exercises

1. Print λ at 1, 3 and 5 kV in picometres. Verify the shortcut λ(nm) = 1.226/√V.
2. Compute both ring radii at V = 2.5 kV in mm. Which is outer, and why?
3. Plot ring radius against V from 1–5 kV for both spacings on one graph. Is the
   relationship linear? What does the shape tell you?
4. **Best extension:** replace the thin circles with a realistic glow. Build a
   2D grid with `np.meshgrid`, compute the radial distance of every pixel, and
   set brightness with `exp(-(rad - x_ring)²/2σ²)` for each ring. Display with
   `pcolormesh` and a green colormap.
5. Add second-order diffraction (n = 2 in Bragg's law) and show where those rings
   fall. Are they inside or outside the first-order ones?
6. At what voltage would λ/2d exceed 1 for the 0.123 nm spacing, making
   diffraction impossible? What does `np.arcsin` return there, and how should
   the code handle it?
7. Add realistic noise to `sin_theta`, re-fit, and see how well d is still
   recovered. This mimics a real experimenter's uncertainty.

Solutions: `solutions/ch14_solutions.py`

---

## What you now know

- De Broglie's hypothesis and its confirmation by electron diffraction.
- λ = h/√(2mₑeV), Bragg's law, and why polycrystals give rings.
- Why smaller spacing means larger ring, and rings shrink with voltage.
- Linearisation: choosing axes on which theory predicts a straight line.
- Fitting, then inverting the fit to *measure* a physical quantity.
- Recognising a numerical zero when you see one.

Next: [Chapter 15 — Task 7: Particle in a box](15_task7_particle_in_box.md)
