# Chapter 11 — Task 3: Planck's law and Einstein's heat capacity

**The task:** *"Plot the Planck 'Black Body radiation' spectrum B(λ,T) for several
temperatures, and also plot Einstein's model of molar heat capacity of solids vs
temperature for various atomic crystals such as gold, copper, iron."*

**Beyond it:** the Wien's-law locus threading every peak, the Rayleigh–Jeans
curve showing the ultraviolet catastrophe, computed CIE glow colours, and the
Dulong–Petit classical limit drawn as a reference line.

This is where quantum mechanics actually begins.

---

## 11.1 The physics: how the quantum was forced into existence

### The problem in 1900

Heat something and it glows. Classical physics — treating light as waves in
thermal equilibrium, each mode carrying kT of energy — predicts the
**Rayleigh–Jeans law**:

  B(λ,T) = 2ckT / λ⁴

It works beautifully at long wavelengths and is a catastrophe at short ones:
as λ → 0, B → ∞. Integrated over all wavelengths, every warm object would emit
infinite energy. Ehrenfest named it the **ultraviolet catastrophe**.

### Planck's fix

Planck (1900) assumed, initially as a mathematical trick he disliked, that an
oscillator of frequency f can only have energy in **discrete packets** E = hf.
The consequence: high-frequency (short-λ) modes need a big packet of energy to
be excited at all, and at temperature T there simply isn't enough thermal energy
to pay for them. Short wavelengths are *frozen out*, and the divergence
disappears:

  **B(λ,T) = (2hc²/λ⁵) · 1/(exp(hc/λk_BT) − 1)**

That equation is the birth certificate of quantum mechanics.

**Check the limit yourself** (a genuinely instructive exercise): for large λ,
hc/λkT is small, and exp(u) − 1 ≈ u, so

  B → (2hc²/λ⁵)·(λk_BT/hc) = 2ck_BT/λ⁴

which is Rayleigh–Jeans. Planck's law *contains* the classical result as its
long-wavelength limit — exactly as a good theory should.

### Wien's displacement law

Differentiating B with respect to λ and setting it to zero gives the peak:

  **λ_max T = b = 2.898 × 10⁻³ m·K**

Hotter → bluer. The Sun at 5778 K peaks at 502 nm — in the middle of the visible
band, which is not a coincidence: eyes evolved where the light is.

### Einstein's heat capacity

Same quantisation, applied to a solid's vibrating atoms. Classically each atom
has 3 degrees of freedom × kT, giving the **Dulong–Petit** result C = 3R ≈ 24.9
J K⁻¹ mol⁻¹, independent of temperature. But experimentally C *falls* towards
zero at low T — another classical failure.

Einstein (1907) modelled a solid as N independent oscillators of one frequency
with quantised energy, giving

  **C = 3R (θ_E/T)² e^(θ_E/T) / (e^(θ_E/T) − 1)²**

where θ_E = hf/k_B is the **Einstein temperature**, characteristic of the
material (stiff, light atoms → high θ_E). As T → ∞ this tends to 3R (classical
limit recovered again); as T → 0 it dies exponentially, because there isn't
enough thermal energy to excite even one quantum of vibration.

*(Aside for interest: real solids follow C ∝ T³ at very low T; Debye's 1912
model, which allows a spectrum of frequencies, fixes this. Einstein's model is
qualitatively right and much simpler.)*

---

## 11.2 The code

### Planck's law as a function

```python
h  = 6.62607015e-34
c  = 2.99792458e8
kB = 1.380649e-23

def planck(lam, T):
    """Spectral radiance B(lambda, T), W sr^-1 m^-3."""
    return (2*h*c**2 / lam**5) / np.expm1(h*c / (lam*kB*T))
```

Two details that matter:

**`np.expm1(x)` instead of `np.exp(x) - 1`.** At long wavelengths the exponent is
tiny, `exp(x)` is very close to 1, and subtracting two nearly-equal floats
destroys precision (§2.4). `expm1` is built to compute e^x − 1 accurately for
small x. Using it is a small mark of competence.

**Bracketing the denominator.** `h*c / (lam*kB*T)` — remove those brackets and
you compute (hc/λ)·k_B·T, which is nonsense (§2.3).

The function works on a single wavelength *or* a whole array, because every
operation inside is vectorised. That's not an accident — it's why we write
physics this way.

### The family of curves

```python
lam = np.linspace(1e-8, 3e-6, 2000)      # 10 nm to 3 um

plt.figure(figsize=(9, 5))
for T in [3000, 4000, 5000, 5778, 6000]:
    label = f'{T} K (Sun)' if T == 5778 else f'{T} K'
    plt.plot(lam*1e9, planck(lam, T), label=label)
```

`lam*1e9` converts metres to nanometres for the axis — **compute in SI, display
in convenient units**. That rule prevents an enormous class of bugs.

The `if ... else` inside an f-string is a *conditional expression*: it picks one
of two values inline. Useful for labelling one special case.

### The Wien locus — the elite touch

```python
Ts = np.linspace(2500, 6500, 200)
lam_peak = 2.897771955e-3 / Ts
plt.plot(lam_peak*1e9, planck(lam_peak, Ts), 'k--', lw=1,
         label="Wien's law $\\lambda_{max}=b/T$")
```

The clever bit: feed *200 temperatures* into Wien's law to get their peak
wavelengths, then evaluate Planck's law **at those peaks**. The resulting dashed
curve passes exactly through the crest of every solid line. It is a visual proof
that your implementation satisfies the analytic peak condition — a check, not a
decoration.

### The catastrophe

```python
rayleigh_jeans = 2*c*kB*5778 / lam**4
plt.plot(lam*1e9, rayleigh_jeans, 'r:', lw=1.5,
         label='Rayleigh–Jeans (classical, 5778 K)')
plt.ylim(0, 5e13)
```

Note the `ylim`: without it, the diverging classical curve squashes everything
else to a flat line. Clipping the view is legitimate — the curve visibly runs
off the top of the plot, which is precisely the point being made.

### The computed glow colours

```python
from cie_color import spectrum_to_rgb
lam_vis = np.linspace(380e-9, 740e-9, 300)
for i, T in enumerate([3000, 4000, 5000, 5778, 6000]):
    Bv = planck(lam_vis, T)
    glow = spectrum_to_rgb(lam_vis*1e9, Bv/Bv.max())
    plt.gca().add_patch(plt.Rectangle((2450, 4.3e13 - i*0.45e13), 400, 0.35e13,
                                      color=glow))
```

Each swatch's colour is *derived from the spectrum itself* by integrating
against the CIE colour-matching functions (Chapter 21) — not chosen by eye. The
1500 K swatch is ember orange, the Sun near-white, 9000 K blue-white. Physics
determining pixels.

### Einstein's heat capacity

```python
Rgas = 8.314462618

def einstein_C(T, TE):
    """Molar heat capacity, Einstein model. TE = Einstein temperature."""
    x = TE / T
    return 3*Rgas * x**2 * np.exp(x) / np.expm1(x)**2

T = np.linspace(1, 500, 1000)
metals = {'lead (T$_E$=67 K)': 67, 'gold (T$_E$=121 K)': 121,
          'copper (T$_E$=245 K)': 245, 'iron (T$_E$=350 K)': 350}

for name, TE in metals.items():
    plt.plot(T, einstein_C(T, TE), label=name)
plt.axhline(3*Rgas, color='k', ls='--', lw=1,
            label='Dulong–Petit limit 3R $\\approx$ 24.9')
```

- `x = TE/T` first makes the formula readable and avoids repeating the division.
- `np.expm1(x)**2` again — the same accuracy argument, squared.
- `T` starts at 1, not 0: dividing by zero would give infinity. (Try `T=0` and
  read the warning; understanding *why* is the exercise.)
- The dictionary carries LaTeX in the keys so the legend renders `T_E` properly.
- `axhline` at 3R shows the classical prediction the quantum curves approach
  from below but never exceed — the whole point of the figure.

---

## 11.3 Reading your own figures

**Planck figure.** Higher T → taller *and* left-shifted peaks. Area under each
curve grows as T⁴ (Stefan–Boltzmann — a good exercise to verify numerically).
The Sun's curve peaks inside the shaded visible band. The dotted classical curve
diverges at small λ.

**Heat-capacity figure.** All curves rise from zero and saturate at 3R. Lead
(soft, heavy atoms, low θ_E) reaches the classical limit at low temperature;
iron (stiff, light) needs far more heat. At room temperature, lead is
essentially classical while iron is not — a quantum effect you can hold in your
hand.

---

## Exercises

1. Verify Stefan–Boltzmann numerically: integrate `planck(lam, T)` over
   wavelength with `np.trapezoid` for several T, and check the total is
   proportional to T⁴. (Fit `log(total)` against `log(T)` — the gradient should
   be 4.)
2. Verify Wien's law numerically: for each T, find the peak with `np.argmax` and
   check λ_max·T is constant. How close to 2.898e-3 do you get, and what limits
   the accuracy?
3. Show the Rayleigh–Jeans limit: plot the ratio of Planck to Rayleigh–Jeans
   against λ for T = 5778 K. At what wavelength does the classical formula
   become 10% wrong?
4. Add tungsten (θ_E ≈ 240 K) and aluminium (θ_E ≈ 290 K) to the heat-capacity
   plot. At 300 K, what fraction of the classical value has each metal reached?
5. Derive Wien's law yourself: differentiate B with respect to λ, set to zero,
   and show you get the transcendental equation x = 5(1 − e^(−x)) with
   x = hc/λk_BT. Solve it numerically (a `while` loop or `np.linspace` search)
   and recover b = 2.898e-3.
6. **Break it:** replace `np.expm1(u)` with `np.exp(u) - 1` and plot the ratio of
   the two versions at very long wavelengths (say 1 mm). Where do they diverge?

Solutions: `solutions/ch11_solutions.py`

---

## What you now know

- Why classical physics diverged, and how quantisation removed the divergence.
- Planck's law, its Rayleigh–Jeans limit, and Wien's displacement law.
- Einstein's heat capacity model, the Einstein temperature, Dulong–Petit.
- `expm1` for numerical accuracy; SI internally, convenient units for display.
- Evaluating a formula *along* a locus to prove a peak condition.
- Colours computed from spectra rather than chosen.

Next: [Chapter 12 — Task 4: The photoelectric effect](12_task4_photoelectric.md)
