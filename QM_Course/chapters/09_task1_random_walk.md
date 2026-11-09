# Chapter 9 — Task 1: Random walks

**The task:** *"Create a model of a random walk of N steps of size s. Each step is
in a random direction, with angle θ chosen from a uniform distribution between 0
and 2π radians."*

**What we built beyond it:** RMS verification against s√N over 4000 walks, a
5000-walk displacement histogram tested against the Rayleigh distribution, and
the 50-walk overlay matching the challenge pack's own figure.

---

## 9.1 The physics

### Why physicists care

Robert Brown (1827) saw pollen grains jiggling in water. The explanation — that
invisible molecules were battering them — was still controversial *seventy years
later*, because nobody could see atoms. The random walk is the mathematical
model of that jiggle, and it gave the first quantitative, testable prediction
that settled the argument.

The same model describes diffusion of a scent across a room, heat spreading
through metal, polymer shapes, and the price of shares.

### The model

Start at the origin. Take N steps. Each step has fixed length s and a direction
θ drawn uniformly from [0, 2π). Steps are **independent** — no memory of the
previous direction.

Step i moves you by:

  Δxᵢ = s cos θᵢ  Δyᵢ = s sin θᵢ

Your position after k steps is the sum of the first k steps:

  x_k = Σ(i=1..k) Δxᵢ  y_k = Σ(i=1..k) Δyᵢ

That "sum of everything so far" is precisely a cumulative sum — the mathematical
justification for `np.cumsum`.

### The result worth proving: R_rms = s√N

Derived in Chapter 8 §8.5, and worth re-reading. Summary: the displacement
vector is **R** = Σ**sᵢ**; squaring gives Ns² from the self terms and zero from
the cross terms (independent directions), so

  **⟨R²⟩ = N s²  ⟹  R_rms = s√N**

Two consequences to notice out loud:

- **The average displacement is zero** (all directions equally likely) but the
  average *distance* is not. Sign cancellation vs magnitude.
- **Distance grows as √N, not N.** Doubling the time doesn't double your
  progress — it multiplies it by 1.41. Diffusion is slow, and that √ is why.

### The distribution: Rayleigh

Stronger than the mean: after many steps, x and y are each sums of many
independent contributions, so by the Central Limit Theorem each becomes Gaussian
with variance σ² = Ns²/2. The distance R = √(x²+y²) of two independent Gaussians
follows the **Rayleigh distribution**:

  P(R) = (R/σ²) exp(−R²/2σ²)

Checking your histogram against this curve tests the entire model, not just its
average.

---

## 9.2 Building the code from nothing

Open a new file, `walk.py`, and build it in stages. Type each stage, run it,
look at it.

### Stage 1 — one walk

```python
import numpy as np
import matplotlib.pyplot as plt

N = 1000
s = 1

angles = np.random.uniform(0, 2*np.pi, N)
dx = s*np.cos(angles)
dy = s*np.sin(angles)

x = np.cumsum(dx)
y = np.cumsum(dy)

plt.plot(x, y)
plt.show()
```

Line by line:

| Line | What it does | Why |
|---|---|---|
| `angles = np.random.uniform(0, 2*np.pi, N)` | N random directions | uniform = no preferred direction (§8.1) |
| `dx = s*np.cos(angles)` | horizontal component of every step | trigonometry, vectorised over all N |
| `x = np.cumsum(dx)` | running total = position after each step | §6.8 |
| `plt.plot(x, y)` | draws the path | y against x, so it's a map not a graph |

### Stage 2 — start at the origin

`cumsum` gives the position *after* step 1 onwards — the origin itself is
missing. Fix:

```python
x = np.concatenate(([0], np.cumsum(dx)))
y = np.concatenate(([0], np.cumsum(dy)))
```

Now the array has N+1 positions: the origin plus one per step. Small detail,
but a model that starts in the wrong place is wrong.

### Stage 3 — make it a function

```python
def random_walk(N, s):
    angles = np.random.uniform(0, 2*np.pi, N)
    dx = s*np.cos(angles)
    dy = s*np.sin(angles)
    x = np.concatenate(([0], np.cumsum(dx)))
    y = np.concatenate(([0], np.cumsum(dy)))
    return x, y
```

Why this matters: you're about to run 9000 walks. A function makes that three
lines instead of thousands. (§5.6)

### Stage 4 — presentation

```python
x, y = random_walk(1000, 1)
plt.figure()
plt.plot(x, y, lw=0.8)
plt.plot(0, 0, 'go', label='Start')
plt.plot(x[-1], y[-1], 'ro', label='End')
plt.title('2D Random Walk: N=1000, s=1')
plt.xlabel('x'); plt.ylabel('y')
plt.legend()
plt.axis('equal')
```

`x[-1]` is the last element (§4.1). `axis('equal')` is compulsory here: without
it the walk is stretched and the cloud's *shape* — the physics — is distorted.

### Stage 5 — the RMS verification

```python
for N in [100, 400, 900, 1600]:
    d_squared = []
    for trial in range(1000):
        x, y = random_walk(N, 1)
        d_squared.append(x[-1]**2 + y[-1]**2)
    rms = np.sqrt(np.mean(d_squared))
    print(f"N={N}:  RMS = {rms:.2f},  theory = {np.sqrt(N):.1f}")
```

The nested-loop structure from §3.5: outer = which N, inner = 1000 repeats.
`x[-1]**2 + y[-1]**2` is Pythagoras without the square root — we want the
*squared* distance (§8.5). Then average, then square-root once, at the end.

Expected output (yours may vary in the last digit — it's random):

```
N=100:  RMS = 10.07,  theory = 10.0
N=400:  RMS = 19.45,  theory = 20.0
N=900:  RMS = 29.95,  theory = 30.0
N=1600: RMS = 40.48,  theory = 40.0
```

### Stage 6 — the distribution test

```python
N, s, walks = 900, 1, 5000
finals = np.zeros(walks)
for i in range(walks):
    x, y = random_walk(N, s)
    finals[i] = np.sqrt(x[-1]**2 + y[-1]**2)

plt.figure(figsize=(8, 5))
plt.hist(finals, bins=40, density=True, alpha=0.7,
         label=f'{walks} simulated walks')
Rr = np.linspace(0, finals.max(), 300)
sigma2 = N*s**2/2
plt.plot(Rr, (Rr/sigma2)*np.exp(-Rr**2/(2*sigma2)), 'r', lw=2,
         label='Rayleigh distribution (theory)')
err = abs(np.mean(finals**2) - N*s**2)/(N*s**2)*100
plt.xlabel('final displacement R')
plt.ylabel('probability density')
plt.title(f'Final-displacement distribution, N={N}: '
          f'error in $\\langle R^2\\rangle$ = {err:.2f}%')
plt.legend()
```

Points of technique:

- `np.zeros(walks)` pre-allocates the results array — cleaner than appending.
- `density=True` normalises the histogram so it's comparable with P(R) (§8.6).
- `sigma2 = N*s**2/2` comes straight from the theory above.
- The error in the title is computed, not typed — the figure reports its own
  accuracy. Do this whenever you can.
- `$\\langle R^2\\rangle$` is LaTeX maths inside a matplotlib string; the double
  backslash escapes it in a normal Python string.

### Stage 7 — the 50-walk overlay

```python
plt.figure()
for i in range(50):
    x, y = random_walk(1000, 1)
    plt.plot(x, y, lw=0.5)
plt.plot(0, 0, 'ko', label='Common origin')
plt.title('50 random walks, N=1000, s=1')
plt.axis('equal')
plt.show()
```

matplotlib cycles colours automatically. The result is a roughly circular cloud
of radius ≈ √1000 ≈ 32 — check the axes and you can *see* the √N law.

---

## 9.3 What each figure is evidence for

| Figure | Claim it supports |
|---|---|
| Single walk | The model does what the task asks: N steps, uniform directions |
| RMS table | Quantitative agreement with ⟨R²⟩ = Ns² across four values of N |
| Histogram | The whole distribution is right, not just its average |
| 50-walk overlay | Isotropy — no preferred direction — and the visible √N scale |

A figure without a claim is decoration. Always know which sentence each figure
is defending.

---

## 9.4 Common bugs and what they look like

| Symptom | Cause |
|---|---|
| Path is a straight line | You plotted `dx, dy` instead of `x, y` |
| Walk starts away from origin | Missing the `concatenate([0], ...)` |
| Cloud looks like an ellipse | Missing `axis('equal')` |
| RMS wildly wrong | Averaged distances instead of squared distances |
| Histogram doesn't match curve | Forgot `density=True` |
| All 50 walks identical | Seeded inside the loop with the same seed |

---

## Exercises

1. Run the RMS test with 100 trials instead of 1000. How much worse is the
   agreement? Relate to §8.4.
2. Change the step size to s = 5 and re-run the RMS test. Does the theory line
   need updating? (It should read s√N — check your code uses `s`, not 1.)
3. Plot RMS distance against √N for N = 100 … 2500 and fit a straight line with
   `np.polyfit`. What should the gradient be? What do you get?
4. Modify `random_walk` to take a `bias` argument that adds a small constant to
   every angle... then think: does that produce drift? Try instead adding a
   constant `bias` to `dx` only. Plot 50 such walks. What physical situation
   does this represent?
5. Write a 3D random walk (hint: you need two angles, θ and φ, and the correct
   way to sample uniformly on a sphere is `cos θ` uniform in [−1,1]). Verify the
   RMS law still gives s√N.
6. **Stretch:** compute the *fractal dimension* of a long walk using the
   box-counting method, and compare with the theoretical value of 2 for a random
   walk.

Solutions: `solutions/ch09_solutions.py`

---

## What you now know

- The random walk model and why it mattered historically.
- The derivation ⟨R²⟩ = Ns², and why mean ≠ RMS.
- Building the model in seven stages, each individually testable.
- Why the origin must be prepended, and why `axis('equal')` is physics not style.
- Testing a distribution (Rayleigh) is stronger than testing a mean.

Next: [Chapter 10 — Task 2: Brownian motion](10_task2_brownian.md)
