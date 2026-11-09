# Chapter 7 — matplotlib: drawing graphs properly

**Goal:** produce publication-quality figures, understand the figure/axes model,
and know why some code says `plt.` and some says `ax.`.

---

## 7.1 The simplest possible graph

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2*np.pi, 200)
y = np.sin(x)

plt.plot(x, y)
plt.show()
```

`plt.plot(x, y)` draws y against x; `plt.show()` opens the window and **pauses
the program** until you close it. Nothing after `plt.show()` runs until then —
which is why it is always the last line.

---

## 7.2 Decoration: the difference between a plot and a figure

An undecorated graph is worthless in physics. Minimum standard:

```python
plt.plot(x, y, lw=0.8, color='red', label='simulation')
plt.xlabel('time (s)')
plt.ylabel('displacement (m)')
plt.title('Damped oscillation')
plt.legend()
plt.grid(alpha=0.3)
plt.show()
```

Rules you should adopt permanently:

1. **Every axis has a quantity and a unit.** `x (nm)`, not `x`.
2. **Every line that isn't obvious gets a `label=` and you call `plt.legend()`.**
3. **A title states what the figure shows**, not "Figure 1".

### Line styles and colours

```python
plt.plot(x, y, 'r--')            # red dashed - shorthand
plt.plot(x, y, 'ko', ms=8)       # black circles, marker size 8
plt.plot(x, y, 'b.', ms=3)       # small blue dots (the gas molecules)
plt.plot(x, y, color='teal', lw=2, ls=':')   # explicit form
```

Shorthand letters: `b`lue `g`reen `r`ed `c`yan `m`agenta `y`ellow blac`k` `w`hite.
Markers: `.` `o` `s` (square) `x` `+` `v`. Lines: `-` `--` `-.` `:`.

### Other useful calls

```python
plt.axhline(24.9, color='k', ls='--')     # horizontal reference line
plt.axvline(656.3, color='r')             # vertical line
plt.axvspan(380, 700, color='yellow', alpha=0.15)   # shaded band
plt.xlim(0, 3000); plt.ylim(0, 5e13)      # zoom
plt.xscale('log')                          # log axis
plt.axis('equal')                          # equal aspect - for maps/walks
plt.text(x, y, 'note')                     # free text
plt.annotate('0.38 eV', (n, E), textcoords='offset points', xytext=(8,-3))
```

`axhline` draws the Dulong–Petit limit in Task 3 and the Heisenberg limit in
Task 7. `axvspan` shades the visible band in three different tasks. `axis('equal')`
is essential for random walks — without it, a circular cloud looks like an
ellipse and you'd draw the wrong physical conclusion.

---

## 7.3 Several figures at once

Each `plt.figure()` starts a new canvas:

```python
plt.figure(figsize=(8, 5))
plt.plot(x, y1)
plt.title('First figure')

plt.figure(figsize=(9, 5))
plt.plot(x, y2)
plt.title('Second figure')

plt.show()          # ONE show at the end - opens both windows
```

`figsize=(width, height)` is in inches. `(8, 5)` or `(9, 5)` suits most graphs;
square `(6, 6)` suits orbitals and walks.

---

## 7.4 Subplots: several panels in one figure

```python
fig, axes = plt.subplots(1, 3, figsize=(13, 4.4))

axes[0].plot(theta, shift)
axes[0].set_title('wavelength shift')
axes[1].plot(theta, speed)
axes[2].plot(theta, angle)

for ax in axes:
    ax.set_xlabel('scattering angle (deg)')

fig.suptitle('Compton scattering')
plt.tight_layout()
plt.show()
```

`plt.subplots(rows, cols)` returns **the figure** and **an array of axes**.
That's the Compton three-panel figure exactly.

For a grid, `axes` is 2D; `.flat` lets you loop over all panels in order:

```python
fig, axes = plt.subplots(3, 3, figsize=(11, 11))
for ax, (n, l, m) in zip(axes.flat, orbitals):
    ...
```

`zip` walks two lists in step — nine axes with nine quantum-number triples.

`plt.tight_layout()` fixes overlapping labels. Use it whenever panels look
cramped.

---

## 7.5 `plt.` versus `ax.` — the thing that confuses everyone

There are two interfaces to matplotlib.

**The `plt.` (state-machine) interface** — commands act on "the current figure":

```python
plt.plot(x, y)
plt.xlabel('x')
```

Quick, fine for single figures.

**The object-oriented interface** — you hold the objects and command them:

```python
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xlabel('x')
```

Notice the naming difference: `plt.xlabel(...)` becomes `ax.set_xlabel(...)`.
Same for `set_title`, `set_xlim`, `set_xticks`.

**Use the object form whenever you have more than one panel, or when you need to
modify a plot later** — which includes every animation and every GUI. That's why
your Brownian and app files all start `fig, ax = plt.subplots()`.

`plt.gca()` ("get current axes") converts from one world to the other when you
need to.

---

## 7.6 Artists and handles: how animation is possible

`ax.plot()` doesn't just draw — it *returns the object it drew* (an "artist"):

```python
dots, = ax.plot(x, y, 'b.', ms=3)
```

Keep that handle and you can move it later without redrawing the whole figure:

```python
dots.set_data(new_x, new_y)
```

That single capability is the entire basis of animation, and it's why the
trailing comma matters (§4.3: `plot` returns a list; the comma unpacks it).

Patches work the same way:

```python
from matplotlib.patches import Circle
big = Circle((0, 0), R, fill=False, color='r', lw=2)
ax.add_patch(big)
...
big.center = (bx, by)         # move it
```

**Crucially, a patch is drawn in *data* coordinates.** A `Circle` of radius R=5
genuinely spans 5 units on the axes, whereas `plot(..., 'ro', ms=20)` draws a
marker 20 *screen points* wide, unrelated to the physics. When you spotted that
your red marker didn't match the collision radius, this was the fix. **Never let
a drawing lie about the model.**

---

## 7.7 Colour maps for 2D data

To show a quantity over a plane (like |ψ|²):

```python
plt.pcolormesh(X, Z, density, cmap='inferno')
plt.colorbar(label='probability density')
```

or `imshow` for a regular grid image. Choose the colormap deliberately:

- `viridis` — perceptually uniform, safe default, colour-blind friendly
- `inferno` / `magma` — dark-to-bright, superb for probability densities
- `coolwarm` / `bwr` — diverging, for data with a meaningful zero (± wavefunctions)
- avoid `jet` — it creates false detail; it is out of fashion for good reason

### Non-linear brightness

Orbital densities vary over orders of magnitude, so a linear scale shows one
bright dot and blackness. The fix:

```python
norm=plt.matplotlib.colors.PowerNorm(0.4)
```

which raises the values to a power before mapping to colour, revealing the faint
outer lobes. `LogNorm()` does a similar job logarithmically. This is a
*presentation* choice, not a physics change — and you should say so if asked.

---

## 7.8 Saving figures

```python
plt.savefig('planck.png', dpi=300, bbox_inches='tight')
```

- `dpi=300` for reports; 80–100 for quick views
- `bbox_inches='tight'` trims white space
- `.pdf` or `.svg` give infinite-resolution vector output for documents
- **`savefig` must come before `show()`** — showing can clear the figure

---

## 7.9 A style checklist for figures you'd submit

Before any figure leaves your computer:

- [ ] axis labels with units
- [ ] legend if more than one line
- [ ] title that states the finding
- [ ] sensible limits (no huge empty regions)
- [ ] `axis('equal')` if the axes represent the same physical dimension
- [ ] readable font sizes at the size it'll be viewed
- [ ] reference lines for theory/limits where relevant
- [ ] colours distinguishable in greyscale where possible

Compare the first random walk you drew (no labels, no dots) with the final one
(start/end markers, title, equal aspect). Same physics; one is evidence, one is
a doodle.

---

## Exercises

Create `ch07_exercises.py`.

1. Plot sin(x) and cos(x) on one figure over 0 to 4π with labels, legend, title,
   grid, and axis labels.
2. Recreate the "two figures" pattern: figure 1 with a decaying exponential,
   figure 2 with its logarithm, one `plt.show()` at the end.
3. Make a 2×2 subplot grid showing y = x, x², x³, x⁴ over 0 to 2, each titled.
   Use `axes.flat` and `tight_layout`.
4. Draw a circle of radius 3 using `Circle` *and* a marker with `ms=30` on the
   same axes with `axis('equal')`. Resize the window and note which one changes
   physical size. Write one sentence explaining which you'd use for a collision
   radius.
5. Plot `np.random.uniform(0, 1, (50, 50))` with `pcolormesh` using three
   different colormaps and a colorbar. Which shows structure best?
6. Take any figure from exercises 1–3, save it at `dpi=300` with tight bounding
   box, and open the PNG to confirm.

---

## What you now know

- `plot` + labels + legend + title is the minimum acceptable figure.
- `figure` starts a canvas; `subplots` builds panels; one `show()` at the end.
- `plt.` versus `ax.` — use the object form for anything interactive.
- Artists are returned and can be moved: `set_data`, `.center` — that's animation.
- Patches use data coordinates; markers use screen points. Don't let art lie.
- Colormaps and `PowerNorm` for 2D densities; `savefig` before `show`.

Next: [Chapter 8 — Randomness and simulation](08_randomness.md)
