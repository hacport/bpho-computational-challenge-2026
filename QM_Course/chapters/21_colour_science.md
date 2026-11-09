# Chapter 21 — Colour science: turning wavelengths into pixels

**Goal:** understand `cie_color.py` — the module that computes what a spectrum
actually *looks like*, instead of guessing.

---

## 21.1 Colour is a property of eyes, not light

Light has a spectrum: power at each wavelength. Colour is what your brain
constructs from three cone signals. The two are not the same thing, and the gap
between them is where all the interesting physics lives.

Your retina has three cone types with broad, overlapping sensitivities (roughly
peaking blue, green, yellow-green). Any spectrum is reduced to just **three
numbers** — the total response of each cone type. That's a colossal loss of
information, and it has a famous consequence: **metamerism**, where two
completely different spectra produce identical cone responses and therefore look
identical. A yellow sodium lamp and a red+green mix on your monitor are
physically unrelated and visually indistinguishable.

So "what colour is 3000 K black-body radiation?" is a question about human vision
as much as about physics — and it has a precise, standardised answer.

---

## 21.2 The CIE 1931 system

In 1931 the Commission Internationale de l'Éclairage standardised colour by
measuring the average human observer. The result is three **colour-matching
functions** x̄(λ), ȳ(λ), z̄(λ). Given any spectrum I(λ), you compute the
**tristimulus values**:

  X = ∫ I(λ) x̄(λ) dλ,  Y = ∫ I(λ) ȳ(λ) dλ,  Z = ∫ I(λ) z̄(λ) dλ

These three numbers *are* the colour, as far as human vision is concerned. Note
ȳ was deliberately defined to match the eye's overall brightness response, so Y
doubles as luminance.

The published functions are lookup tables, but there's an excellent analytic
approximation (Wyman, Sloan & Shirley, 2013) using sums of **piecewise Gaussians**
— Gaussians with different widths on each side:

```python
def cie_xyz_bar(lam_nm):
    def g(x, mu, s1, s2):
        s = np.where(x < mu, s1, s2)         # different width below/above peak
        return np.exp(-0.5*((x - mu)/s)**2)
    l = np.asarray(lam_nm, dtype=float)
    xbar = (1.056*g(l, 599.8, 37.9, 31.0) + 0.362*g(l, 442.0, 16.0, 26.7)
            - 0.065*g(l, 501.1, 20.4, 26.2))
    ybar = 0.821*g(l, 568.8, 46.9, 40.5) + 0.286*g(l, 530.9, 16.3, 31.1)
    zbar = 1.217*g(l, 437.0, 11.8, 36.0) + 0.681*g(l, 459.0, 26.0, 13.8)
    return xbar, ybar, zbar
```

**`np.where(condition, a, b)`** is the vectorised if-else: element-wise, take `a`
where the condition is true and `b` where it's false. Here it picks the left or
right width depending on which side of the peak you're on. Learn this function —
it replaces loops full of `if` statements.

Note x̄ has *two* peaks (one in the red, a small one in the blue) — that's real:
the long-wavelength cone has a secondary blue sensitivity, which is why extreme
violet looks slightly reddish.

---

## 21.3 From XYZ to a screen colour

XYZ is device-independent. Monitors use **sRGB**. The conversion is a fixed
matrix followed by a nonlinear step:

```python
XYZ_TO_RGB = np.array([[ 3.2406, -1.5372, -0.4986],
                       [-0.9689,  1.8758,  0.0415],
                       [ 0.0557, -0.2040,  1.0570]])

def xyz_to_srgb(X, Y, Z):
    rgb = XYZ_TO_RGB @ np.array([X, Y, Z])
    rgb = np.clip(rgb, 0, None)
    if rgb.max() > 0:
        rgb = rgb / rgb.max()
    rgb = np.where(rgb <= 0.0031308, 12.92*rgb, 1.055*rgb**(1/2.4) - 0.055)
    return np.clip(rgb, 0, 1)
```

Three steps, each worth understanding:

**1. The matrix multiply.** `@` is Python's matrix-multiplication operator. The
matrix encodes the actual chromaticities of the standard red, green and blue
phosphors.

**2. Clipping negatives.** Negative components mean the colour is **outside the
sRGB gamut** — a real colour your monitor physically cannot display. Pure
spectral cyan is a common example. Clipping is the crude fix; more sophisticated
methods desaturate towards white instead. Worth knowing that the limitation is
in the *display*, not your maths.

**3. Gamma correction.** This is the step almost everyone omits, and its absence
is why amateur spectrum plots look wrong. Screens don't respond linearly to
signal values: physical brightness ≈ signal^2.2. So a signal of 0.5 gives about
22% of full brightness, not 50%. To display a linear intensity correctly you must
apply the inverse — the `1.055·x^(1/2.4) − 0.055` transfer function, with a small
linear segment near zero to avoid an infinite slope.

Skip gamma and every colour comes out too dark and desaturated. Include it and
your spectrum looks like a real spectrum.

---

## 21.4 Two public functions

### Single wavelength → colour

```python
def wavelength_to_rgb(lam_nm, brightness=1.0):
    xbar, ybar, zbar = cie_xyz_bar(lam_nm)
    rgb = xyz_to_srgb(float(xbar), float(ybar), float(zbar))
    fade = 1.0
    if lam_nm < 420:
        fade = max(0.25, (lam_nm - 380)/40)
    elif lam_nm > 660:
        fade = max(0.25, (740 - lam_nm)/80)
    return tuple(np.clip(rgb * brightness * fade, 0, 1))
```

The `fade` factor dims the extreme violet and deep red ends, where the eye's
sensitivity falls off — so a 700 nm line looks dimmer than a 550 nm one, as it
should. This is a perceptual nicety on top of the colorimetry, and it's why the
hydrogen spectroscope view looks convincing.

Checked outputs:

```
410 nm → (0.40, 0.00, 0.75)   violet
486 nm → (0.00, 0.75, 1.00)   cyan       (H-beta)
546 nm → (0.00, 1.00, 0.00)   green      (mercury line)
589 nm → (1.00, 0.51, 0.00)   orange     (sodium D)
656 nm → (1.00, 0.00, 0.00)   red        (H-alpha)
```

Compare with a real spectrum chart — these are right.

### Whole spectrum → colour

```python
def spectrum_to_rgb(lam_nm, intensity):
    xbar, ybar, zbar = cie_xyz_bar(lam_nm)
    X = np.trapezoid(intensity*xbar, lam_nm)
    Y = np.trapezoid(intensity*ybar, lam_nm)
    Z = np.trapezoid(intensity*zbar, lam_nm)
    return tuple(xyz_to_srgb(X, Y, Z))
```

The tristimulus integrals, done numerically with the trapezium rule (§15.3).
Feed it a Planck spectrum and you get the colour of a star:

```
1500 K → (1.00, 0.42, 0.00)   ember orange
3000 K → (1.00, 0.72, 0.43)   warm incandescent
5778 K → (1.00, 0.95, 0.92)   near-white (the Sun)
9000 K → (0.84, 0.88, 1.00)   blue-white
```

This is the **Planckian locus** — the path hot objects trace through colour space
— and you computed it from Planck's law plus human physiology. Nothing was
chosen by eye.

It also explains "colour temperature" on light bulb boxes: a 2700 K bulb is
labelled that way because its spectrum matches a 2700 K black body. Confusingly,
higher temperature means "cooler" looking light — because bluer.

---

## 21.5 Where this is used in the project

| Task | Use |
|---|---|
| 3 — black body | Glow swatch per temperature, from `spectrum_to_rgb` |
| 4 — photoelectric app | Lamp and photon colour from `wavelength_to_rgb` |
| 5 — hydrogen | True-colour Balmer lines on black |

Three tasks, one module, zero repeated code. That's what a shared library is for
— and writing `cie_color.py` as a standalone importable module (with its own
`__main__` demo that draws the spectrum strip) is exactly how a real project
would be organised.

---

## Exercises

1. Run `cie_color.py` directly to see the spectrum strip. Compare it with a
   photograph of a real spectrum online.
2. Print the RGB for 400, 450, 500, 550, 600, 650, 700 nm and check each against
   what you'd expect by name.
3. Compute and plot the colours of black bodies from 1000 K to 12000 K as a strip
   of swatches. Where does it pass closest to white?
4. **Break it:** remove the gamma correction (return the linear rgb directly) and
   redraw the spectrum strip. Describe the difference precisely.
5. Sodium's D lines are at 589.0 and 589.6 nm. Compute the colour of an equal
   mixture and compare with the colour of 589.3 nm alone. Are they the same? What
   does this demonstrate about metamerism?
6. Compute the colour of a "flat" white spectrum (equal intensity at all
   wavelengths). Is it exactly (1,1,1)? Should it be?
7. **Stretch:** plot the CIE chromaticity diagram — compute x = X/(X+Y+Z),
   y = Y/(X+Y+Z) for every wavelength and draw the horseshoe curve, with your
   Planckian locus overlaid on it.

Solutions: `solutions/ch21_solutions.py`

---

## What you now know

- Colour is a three-number reduction of a spectrum by human cones; metamerism.
- CIE 1931 colour-matching functions and tristimulus integrals.
- Piecewise-Gaussian approximation, and `np.where` as a vectorised if-else.
- XYZ → sRGB via matrix, gamut clipping, and why gamma correction is essential.
- Computing the colour of a spectral line and of a whole spectrum.
- The Planckian locus, and what "colour temperature" really means.

**End of Part 4.**

Next: [Chapter 22 — Capstone: rebuild everything](22_capstone.md)
