# Chapter 12 — Task 4: The photoelectric effect

**The task:** *"Plot photoelectron stopping voltage vs frequency (or in-vacuum
wavelength) of incident photons for various metals. EXTENSION: Create an animated
app like the PhET demo."*

**Beyond it:** honest below-cutoff masking with NaN, a simulated noisy Millikan
experiment that recovers Planck's constant to 0.06%, and a full virtual-lab app
with a retarding-voltage measurement.

---

## 12.1 The physics

### The experiment that broke the wave theory

Shine light on a metal; electrons come out. Wave theory predicts three things,
all of which are **wrong**:

| Wave theory says | Experiment says |
|---|---|
| Brighter light → more energetic electrons | Brightness changes only the *number* |
| Any colour works if bright enough | Below a threshold frequency, *nothing* happens |
| Faint light needs time to accumulate energy | Emission is instantaneous |

### Einstein's photon explanation (1905, and his actual Nobel)

Light arrives as **quanta** of energy E = hf. One photon is absorbed by one
electron. The electron must pay the **work function** W to escape the metal;
whatever's left is kinetic energy:

  **KE_max = hf − W**

Everything now fits. Brightness = more photons = more electrons, but each still
carries hf. Below f₀ = W/h, no single photon can pay the exit fee, so nothing
happens at any brightness.

### Measuring it: the stopping voltage

Apply a reverse voltage to repel the electrons. When the voltage exactly stops
the most energetic ones, eV_s = KE_max:

  **V_s = (hf − W)/e**

Plot V_s against f and you get a straight line:

- **gradient = h/e** — the same for every metal (universal constant!)
- **x-intercept = f₀ = W/h** — material-specific threshold
- **y-intercept = −W/e**

Millikan did exactly this in 1916, hoping to *disprove* Einstein, and ended up
producing the best measurement of h then available. Your code repeats the
experiment.

---

## 12.2 The graph, and one honest detail

```python
metals = {'caesium': 2.10, 'sodium': 2.28, 'zinc': 4.31,
          'copper': 4.70, 'platinum': 5.65}     # work functions in eV

f = np.linspace(0, 2.5e15, 1000)

for name, W_eV in metals.items():
    W = W_eV * e                # convert eV -> joules
    f0 = W / h
    V = (h*f - W) / e
    V[f < f0] = np.nan          # below cutoff: nothing happens
    plt.plot(f/1e15, V, label=f'{name} (W = {W_eV} eV)')
    print(f'{name:9s}: cutoff f0 = {f0/1e15:.3f} PHz,  '
          f'cutoff wavelength = {c/f0*1e9:.0f} nm')
```

**The `np.nan` line is the physics.** Without it the formula happily returns
negative stopping voltages below threshold, which don't exist — there are no
electrons at all. `np.nan` ("not a number") tells matplotlib to draw nothing
there, so each line *begins* at its own cutoff. A lesser entry plots the whole
line and quietly asserts something false.

Note also the unit conversion: work functions are quoted in eV because that's
convenient for humans; the formula needs joules. Convert at the boundary, then
work in SI (§11.2).

Printed output:

```
caesium  : cutoff f0 = 0.508 PHz,  cutoff wavelength = 590 nm
sodium   : cutoff f0 = 0.551 PHz,  cutoff wavelength = 544 nm
zinc     : cutoff f0 = 1.042 PHz,  cutoff wavelength = 288 nm
copper   : cutoff f0 = 1.136 PHz,  cutoff wavelength = 264 nm
platinum : cutoff f0 = 1.366 PHz,  cutoff wavelength = 219 nm
```

Read that table physically: caesium and sodium respond to *visible* light (which
is why caesium is used in photocells), while zinc, copper and platinum need
ultraviolet. That's why the classic classroom demo uses a zinc plate and a UV
lamp.

---

## 12.3 Simulating the experiment: recovering h

Plotting a formula proves nothing — the graph is the equation. The real
demonstration is to **generate data, add noise, fit it, and see if the physics
comes back out.**

```python
rng = np.random.default_rng(1)
fs = np.linspace(1.5e15, 2.5e15, 12)                    # 12 measurements
Vs_data = (h*fs - metals['platinum']*e)/e + rng.normal(0, 0.05, fs.size)

m_fit, c_fit = np.polyfit(fs, Vs_data, 1)
h_measured = m_fit * e
W_measured = -c_fit
```

Step by step:

1. **Twelve frequencies** — a realistic number of lab readings.
2. **`rng.normal(0, 0.05, 12)`** adds Gaussian noise of standard deviation 0.05 V
   — imitating real measurement scatter. The seed makes it reproducible (§8.2).
3. **`np.polyfit(x, y, 1)`** fits a polynomial of degree 1 — a straight line — by
   least squares, returning `[gradient, intercept]`.
4. **`h_measured = m_fit * e`** — since gradient = h/e, multiplying by e recovers
   h from *the data*, not from the constant we typed in.

Output:

```
h from fitted gradient = 6.6298e-34 J s   (true 6.6261e-34, error 0.06 %)
W from fitted intercept = 5.64 eV   (true 5.65 eV)
```

**Why this is the strongest part of the task.** You have shown that if a real
student did this experiment with realistic errors, they would measure Planck's
constant to a fraction of a percent. That's an experimental-physics claim, made
computationally.

### What least squares actually does

Given points (xᵢ, yᵢ), it finds the line y = mx + c minimising the total squared
vertical distance Σ(yᵢ − mxᵢ − c)². Setting the derivatives to zero gives closed
forms:

  m = [n Σxy − Σx Σy] / [n Σx² − (Σx)²],  c = ȳ − m x̄

`polyfit` solves this for you. Worth implementing once by hand — it's exercise 5.

---

## 12.4 The virtual lab (the named extension)

The app has four moving parts. The pattern generalises to any interactive
physics tool.

**1. Layout with explicit axes.** Each control and panel gets its own rectangle
in figure coordinates `[left, bottom, width, height]`, all in the range 0–1:

```python
ax = fig.add_axes([0.30, 0.13, 0.68, 0.80])        # the main scene
ax_lam = fig.add_axes([0.05, 0.54, 0.17, 0.03])    # a slider strip
```

**2. Widgets and callbacks** (full treatment in Chapter 19):

```python
s_lam = Slider(ax_lam, '', 160, 800, valinit=400, color='#0969da')
s_lam.on_changed(refresh_static)     # call this function whenever it moves
```

**3. Drawn apparatus** — patches, not photos: `FancyBboxPatch` for the chamber,
`Rectangle` for the plates, `Circle` for the meter, `Polygon` for the lamp
housing. Everything positioned in data coordinates so it scales together.

**4. The animation loop**, which is where the physics lives:

```python
k = 0.26
v0 = k*np.sqrt(max(KE, 0)/e)          # launch speed from KE (v ∝ √KE)
gap = an_x - cath_x
decel = k**2 * s_ret.val / (2*gap)    # uniform deceleration from the field
...
el_v[live] -= decel                   # electrons slow down
el_x[live] += el_v[live]
back = live & (el_x < cath_x + 0.1)   # turned back before reaching the anode
```

The deceleration is chosen so that an electron launched with the KE corresponding
to voltage V_s exactly fails to reach the anode. Consequence: **the animation
obeys the same equation as the graph**, so when you raise the retarding slider
past V_s the current genuinely falls to zero. Verified:

```
current at V = 0.5 V (< Vs = 0.82) : 5.58
current at V = 2.5 V (> Vs)        : 0.00
current at 700 nm on sodium        : 0.00   (below cutoff)
```

That's not decoration — it's a working instrument you can take a measurement
from. Raise the voltage until the meter reads zero and you have measured V_s.

**5. Physically honest emission statistics:**

```python
n_new = np.random.binomial(n_hit, min(rate, 1.0))
```

Each photon that lands has a probability (the intensity) of ejecting an
electron. Increasing intensity increases the *count*; only wavelength changes
each electron's *speed*. The app therefore demonstrates the exact fact that
killed the wave theory.

---

## 12.5 The relationship between the two files

`task4_photoelectric.py` — the analysis: graph, cutoffs, fitted h.
`task4_app_photoelectric.py` — the instrument: interactive, animated.

Different jobs, different files (same reasoning as Chapter 10's split). They
agree with each other because both implement eV_s = hf − W, and demonstrating
that agreement on camera is worth more than either alone.

---

## Exercises

1. Add three metals (potassium 2.30 eV, silver 4.26 eV, gold 5.10 eV) and print
   their cutoff wavelengths. Which respond to visible light?
2. Change the noise level to 0.2 V and re-fit. How does the error in h change?
   Now increase to 50 data points at the same noise — quantify the improvement
   and relate it to §8.4.
3. Fit *every* metal's simulated data and print the mean and standard deviation
   of the eight h values you obtain.
4. Plot stopping voltage against **wavelength** instead of frequency. Why is the
   frequency version preferred for extracting h?
5. Implement least squares yourself with the closed-form equations in §12.3 and
   check against `np.polyfit` on the same data.
6. In the app, add a readout showing the *predicted* stopping voltage, then
   verify by hand that the current dies exactly there for three different
   metal/wavelength combinations.
7. **Break it:** delete the `V[f < f0] = np.nan` line. What does the graph now
   claim, and why is it false?

Solutions: `solutions/ch12_solutions.py`

---

## What you now know

- Why the photoelectric effect refuted wave theory; E = hf and KE = hf − W.
- V_s vs f is a straight line of gradient h/e — the basis of Millikan's measurement.
- Masking with `np.nan` to avoid drawing physics that doesn't exist.
- `polyfit` least-squares fitting, and recovering a constant *from data*.
- Building a virtual instrument whose animation obeys the same equation as the
  graph — and taking a real measurement from it.

Next: [Chapter 13 — Task 5: The hydrogen spectrum](13_task5_hydrogen.md)
