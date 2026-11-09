# Chapter 16 — Task 8: Quantum cryptography

**The task:** *"Create a visual calculator (e.g. some form of GUI or app) of the
Classical and Quantum mismatch probabilities, with the angles θ and φ as
variables. Perhaps as sliders, or via gesture controls?"*

Note this task *is* a GUI task — interactivity is the deliverable, not an
extension.

**Beyond it:** 2D heat maps of the whole parameter space, and identifying the
specific configuration where the two theories separate most dramatically.

---

## 16.1 The physics

### The setup

A source emits **entangled** photon pairs; one goes to Alice, one to Bob. Each
measures polarisation with a detector oriented at their own angle — θ for Alice,
φ for Bob. Each measurement gives one of two outcomes (call them X or Y).

The question: how often do their results **disagree**?

### Malus's law as the starting point

Classically, light of intensity I₀ polarised at angle α to a filter transmits
I = I₀cos²α. In the quantum single-photon reading, this becomes a *probability*:
a photon polarised along a given axis is detected in the X channel of a detector
at angle θ with probability cos²θ, and in the Y channel with sin²θ.

The pack states this directly:

  P(X_A) = cos²θ, P(Y_A) = sin²θ
  P(X_B) = cos²φ, P(Y_B) = sin²φ

### The classical (local realist) prediction

Assume each photon carries its own predetermined polarisation, and the two
detectors act independently. Then probabilities simply multiply:

  P(match) = P(X_A)P(X_B) + P(Y_A)P(Y_B) = cos²θcos²φ + sin²θsin²φ

  **P(mismatch)_classical = 1 − cos²θ cos²φ − sin²θ sin²φ**

### The quantum prediction

Quantum mechanically the pair is in an *entangled* state — it is not two photons
with two properties, it is one two-photon state. Measuring Alice's photon
**collapses** the pair: Bob's photon instantly acquires a definite polarisation
along Alice's measurement axis.

So Bob is no longer measuring a photon at some fixed angle; he is measuring a
photon polarised along θ, using a detector at φ. Malus's law now applies to the
*relative* angle φ − θ:

  P(match) = cos²θ·cos²(φ−θ) + sin²θ·cos²(φ−θ) = (cos²θ + sin²θ)cos²(φ−θ)

  **P(mismatch)_quantum = sin²(φ − θ)**

Only the *difference* of the angles matters. That's the fingerprint of
entanglement, and it is not reproducible by any local hidden-variable model.

### Where they disagree, and why it matters

| θ | φ | Classical | Quantum |
|---|---|---|---|
| 45° | 45° | 0.500 | **0.000** |
| 30° | 30° | 0.375 | **0.000** |
| 30° | 60° | 0.625 | 0.250 |
| 45° | 90° | 0.500 | 0.500 |

The decisive case is **aligned detectors** (θ = φ): quantum mechanics predicts
*perfect* correlation — mismatch exactly zero, always — while the classical
calculation can't get below 0.375 for those settings. Aspect's experiments in the
early 1980s found the quantum answer; the 2022 Nobel Prize went to Aspect,
Clauser and Zeilinger for that line of work.

### The cryptography

This is the basis of quantum key distribution (BB84/E91). Alice and Bob compare
detector settings publicly (but never results) and keep the runs where their
bases matched — those results are perfectly correlated and form a shared secret
key.

If Eve intercepts a photon, she must measure it — and measurement collapses the
state onto *her* basis, which is generally wrong. The photon Bob receives has
been altered. The correlation degrades, extra mismatches appear, and **Alice and
Bob detect the eavesdropper by comparing a sample of their results.** Security
guaranteed by physics rather than by computational difficulty.

---

## 16.2 The code

### The two models, as functions

```python
def classical_mismatch(th, ph):
    return 1 - np.cos(th)**2*np.cos(ph)**2 - np.sin(th)**2*np.sin(ph)**2

def quantum_mismatch(th, ph):
    return np.sin(ph - th)**2
```

Both take radians and work on scalars *or* arrays — which is why the same
functions serve the slider readout and the 200×200 heat map.

### Laying out a dashboard

```python
fig = plt.figure(figsize=(11, 6))
ax_arrows = fig.add_axes([0.06, 0.35, 0.36, 0.52])
ax_bars   = fig.add_axes([0.52, 0.35, 0.20, 0.52])
ax_curve  = fig.add_axes([0.78, 0.35, 0.20, 0.52])
ax_sth    = fig.add_axes([0.15, 0.16, 0.6, 0.04])
ax_sph    = fig.add_axes([0.15, 0.08, 0.6, 0.04])
```

`add_axes([left, bottom, width, height])` in figure fractions gives complete
control (§12.4). Three display panels above, two slider strips below.

### Sliders and the redraw callback

```python
s_th = Slider(ax_sth, 'Alice angle $\\theta$ (deg)', 0, 90, valinit=0)
s_ph = Slider(ax_sph, 'Bob angle $\\phi$ (deg)', 0, 90, valinit=30)

def draw(_=None):
    th = np.radians(s_th.val)
    ph = np.radians(s_ph.val)
    pc = classical_mismatch(th, ph)
    pq = quantum_mismatch(th, ph)
    ...redraw the three panels...
    fig.canvas.draw_idle()

s_th.on_changed(draw)
s_ph.on_changed(draw)
draw()                      # draw once at startup
```

The pattern (Chapter 19 in full):

1. Read the current slider values (`.val`).
2. Compute the physics — **sliders in degrees, physics in radians**; convert at
   the boundary, exactly as with eV → joules.
3. Redraw.
4. `draw_idle()` schedules an efficient refresh.
5. The `_=None` default lets you call `draw()` manually at startup, even though
   matplotlib passes the new value when a slider moves.

### The detector schematic

```python
for ang, colour, name in [(th, 'green', 'Alice'), (ph, 'blue', 'Bob')]:
    ax_arrows.annotate('', xy=(np.sin(ang), np.cos(ang)), xytext=(0, 0),
                       arrowprops=dict(color=colour, width=2))
    ax_arrows.annotate('', xy=(np.cos(ang), -np.sin(ang)), xytext=(0, 0),
                       arrowprops=dict(color=colour, width=1, alpha=0.4))
```

`annotate` with an empty string and `arrowprops` draws a pure arrow. Each
detector shows its Y axis (solid) and X axis (faint) — perpendicular, as they
must be. Watching the arrows rotate while the numbers change is what makes the
abstraction concrete for a viewer.

### The comparison curve

```python
ph_sweep = np.linspace(0, np.pi/2, 200)
th_fix = np.pi/4
ax_curve.plot(np.degrees(ph_sweep), quantum_mismatch(th_fix, ph_sweep), 'b',
              label='QM $\\sin^2(\\phi-45°)$')
ax_curve.plot(np.degrees(ph_sweep), classical_mismatch(th_fix, ph_sweep), 'r',
              label='classical (flat 0.5!)')
```

A deliberate choice: **fix Alice at 45° and sweep Bob**. At that setting the
classical curve is *exactly flat at 0.5* for all φ, while the quantum curve dips
to zero at φ = 45°. Choosing the parameter slice that maximally separates two
theories is a real skill — it's how experiments are designed.

### The heat maps

```python
th_g, ph_g = np.meshgrid(np.linspace(0, np.pi/2, 200),
                         np.linspace(0, np.pi/2, 200))
for ax, Z, name in [(axc, classical_mismatch(th_g, ph_g), 'Classical'),
                    (axq, quantum_mismatch(th_g, ph_g), 'Quantum')]:
    im = ax.pcolormesh(np.degrees(th_g), np.degrees(ph_g), Z,
                       cmap='inferno', vmin=0, vmax=1)
```

**`np.meshgrid`** turns two 1D coordinate arrays into two 2D grids covering every
combination — 40,000 (θ,φ) pairs. Your functions then evaluate all of them in
one vectorised call. This is how you compute a field over a plane, and you'll use
it again for orbitals (Chapter 18).

`vmin=0, vmax=1` fixes the colour scale on both panels so they're directly
comparable — a subtle but important point: two heat maps with different
auto-scaled colour ranges cannot be compared by eye.

The structural difference is then obvious: the quantum map depends only on
φ−θ, so it's constant along diagonals. The classical map has no such symmetry.
The picture *shows* that entanglement depends only on relative angle.

---

## Exercises

1. Find, by scanning with `np.meshgrid`, the (θ,φ) pair where |classical −
   quantum| is largest. What are the two probabilities there?
2. Verify θ = φ gives exactly zero quantum mismatch for ten random angles.
3. Extend the sliders to 0–180°. Does anything new appear? What symmetry do you
   observe, and why does sin² produce it?
4. Model Eve: assume she intercepts a fraction f of photons, measuring each in a
   random basis and re-sending. Derive (or reason out) the resulting mismatch
   and plot it against f. At what f could Alice and Bob detect her with 100
   sample bits?
5. Compute the CHSH quantity S = |E(a,b) − E(a,b′) + E(a′,b) + E(a′,b′)| where
   E = 1 − 2·P(mismatch), at the classic angles (0°, 22.5°, 45°, 67.5°). Local
   realism requires S ≤ 2; quantum mechanics allows up to 2√2 ≈ 2.83. Which do
   you get from each model?
6. Add a third panel showing the *difference* between the two heat maps with a
   diverging colormap.

Solutions: `solutions/ch16_solutions.py`

---

## What you now know

- Malus's law as a probability; the classical (independent) mismatch formula.
- Entanglement, collapse, and why the quantum result depends only on φ−θ.
- The aligned-detector case that separates the theories, and its experimental
  history (Aspect; Nobel 2022).
- How quantum key distribution detects eavesdroppers physically.
- Slider callbacks: read → convert units → compute → redraw.
- `meshgrid` for evaluating a function over a plane; fixing colour scales for
  fair comparison.

Next: [Chapter 17 — Task 9: Compton scattering](17_task9_compton.md)
