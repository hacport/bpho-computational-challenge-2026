# Chapter 10 — Task 2: Brownian motion and animation

**The task:** *"Consider N small particles of mass m and radius r moving randomly,
some of which collide with a large particle of mass M and radius R. Use a random
walk to model the smaller particles, and conservation of momentum to model
collisions with the larger particle. Animate the subsequent motion."*

**Beyond it:** viscous damping (making it a Langevin model), a live
squared-displacement panel, and a 30-run study showing MSD ∝ t — Einstein's 1905
result.

This is the hardest chapter in Part 3. Take it slowly.

---

## 10.1 The physics

### The historical stakes

Einstein's 1905 paper on Brownian motion was not about pollen. It was an
argument that **atoms exist**, aimed at physicists who thought them a
convenient fiction. His logic: if matter is made of molecules in thermal motion,
a suspended particle must be bombarded unevenly and must therefore wander in a
specific, calculable way. Perrin measured it in 1908, found agreement, and the
atomic debate ended. He got the 1926 Nobel Prize.

So Task 1 *assumed* a random walk. Task 2 *derives* one from mechanics.

### The mechanics of one collision

A molecule (mass m) strikes a large particle (mass M) with m ≪ M. Momentum is
conserved:

  m u_before + M V_before = m u_after + M V_after

The change in the large particle's velocity from one hit is of order

  ΔV ≈ (m/M) u

So each individual kick is tiny (m/M ~ 10⁻¹² in reality), but there are ~10²⁰
collisions per second, and crucially they **don't cancel exactly**. The
imbalance is a random walk in velocity — hence in position.

**The direction of the kick.** Model the particles as hard discs. The impulse
acts along the *line of centres*. If the molecule sits at position **p** and the
big particle at **b**, the unit vector from big to small is

  **û** = (**p** − **b**) / |**p** − **b**|

The molecule pushes inwards; by Newton's third law the big particle recoils
outwards along −**û**. That minus sign in the code is Newton's third law.

### Why drag is needed: the Langevin equation

Our first version had no friction, so kicks accumulated and the particle glided
off like a puck on ice. Real pollen sits in water, where viscous drag removes
momentum almost instantly (Stokes drag F = −6πηrv).

Adding a drag term gives the **Langevin equation** (1908):

  M dV/dt = −γV + F_random(t)

*deterministic damping + random forcing*. Our discrete version is exactly this:

```python
bvx = drag * bvx          # the -γV term, as a per-frame multiplier
bvx = bvx - (m/M)*s*np.sum(ux)   # the random force from collisions
```

A drag factor of 0.97 means "keep 97% of your velocity each frame", equivalent
to exponential decay with time constant τ = −Δt/ln(0.97) ≈ 33 frames. Choosing
that number by comparing the trajectory shape to the expected jagged behaviour
is legitimate model calibration — say so, and say what too-large and too-small
look like (frozen; gliding).

### The prediction to test: MSD ∝ t

Einstein's headline result: for diffusion in 2D,

  ⟨|R(t) − R(0)|²⟩ = 4Dt

Mean squared displacement grows **linearly with time**. Note this is the same
statement as Task 1's ⟨R²⟩ = Ns², since N ∝ t. Straight line = diffusion.

At very short times, before the particle has been kicked enough, motion is
"ballistic" (MSD ∝ t²) — that's the little curve at the start of your plot, and
naming it *ballistic-to-diffusive crossover* is a genuine piece of insight.

---

## 10.2 Building it: stage by stage

### Stage 1 — a crowd of walkers

The mental shift from Chapter 9: there, an array was **one particle over time**.
Here, an array is **many particles at one instant**.

```python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

Np, s, L = 200, 0.5, 50
x = np.random.uniform(-L, L, Np)
y = np.random.uniform(-L, L, Np)

fig, ax = plt.subplots()
dots, = ax.plot(x, y, 'b.', ms=3)
ax.set_xlim(-L, L); ax.set_ylim(-L, L)
ax.set_aspect('equal')

def update(frame):
    global x, y
    angles = np.random.uniform(0, 2*np.pi, Np)
    x = x + s*np.cos(angles)
    y = y + s*np.sin(angles)
    dots.set_data(x, y)
    return dots,

anim = FuncAnimation(fig, update, frames=300, interval=30)
plt.show()
```

**How animation works.** `FuncAnimation` holds a clock. Every `interval`
milliseconds it calls your `update` function once, passing the frame number.
Your job inside `update` is: advance the physics by one tick, then move the
existing artists with `set_data`. It redraws only what changed — far faster than
rebuilding the figure.

**Three things that trip people up:**

1. `global x, y` — without it, each frame edits a private copy and nothing moves
   (§5.4).
2. `anim = ...` — you must keep the animation object in a variable. If Python
   garbage-collects it, the animation silently stops.
3. `return dots,` must be the last line, and the comma makes it a tuple.

Fresh random angles every frame = no memory = a true random walk in time.

### Stage 2 — the big particle

```python
m, M, R = 1.0, 25.0, 5.0
bx, by = 0.0, 0.0        # position
bvx, bvy = 0.0, 0.0      # velocity - starts at REST
```

Starting at rest is the experimental cleanliness: any motion it acquires must
have come from collisions, because we programmed none.

Draw it as a **patch**, not a marker (§7.6), so its drawn radius equals its
physical radius:

```python
from matplotlib.patches import Circle
big = Circle((bx, by), R, fill=False, color='r', lw=2)
ax.add_patch(big)
```

### Stage 3 — collision detection with a mask

```python
dist = np.sqrt((x - bx)**2 + (y - by)**2)     # 200 distances at once
hit = dist < R                                 # 200 True/False
```

Pythagoras, vectorised (§6.4), then a boolean mask (§6.6). No `if` statements,
no loop over particles.

### Stage 4 — the kick

```python
if np.any(hit):
    ux = (x[hit] - bx) / dist[hit]      # unit vectors, big -> molecule
    uy = (y[hit] - by) / dist[hit]
    bvx = bvx - (m/M) * s * np.sum(ux)  # Newton's 3rd law: recoil is -u
    bvy = bvy - (m/M) * s * np.sum(uy)
    x[hit] = bx + R*ux                  # place hitters on the rim
    y[hit] = by + R*uy
```

- Dividing by `dist[hit]` normalises to unit vectors — pure direction.
- `(m/M)*s` is the momentum-conserving velocity change per hit.
- `np.sum` adds simultaneous kicks; opposite-side hits cancel, which is exactly
  why the net motion is small and random rather than a steady shove.
- The last two lines prevent molecules from getting stuck inside the disc and
  re-colliding every frame — a numerical necessity, not physics.

### Stage 5 — drag, motion, walls

```python
bvx = drag * bvx
bvy = drag * bvy
bx = bx + bvx
by = by + bvy
bx = np.clip(bx, -L+R, L-R)
by = np.clip(by, -L+R, L-R)
```

State updated by its own velocity — the `state = f(state)` heartbeat again. The
clip keeps the disc inside the box, offset by R so its edge doesn't cross the
wall.

Molecules get the same treatment right after their step:

```python
x = np.clip(x, -L, L)
y = np.clip(y, -L, L)
```

Keeping the gas density constant means the bombardment never dries up.

### Stage 6 — the trail and the live MSD panel

```python
trail_x, trail_y = [], []          # lists, because they GROW (§4.5)
trail, = ax.plot([], [], 'r-', lw=0.8)
...
trail_x.append(bx)
trail_y.append(by)
trail.set_data(trail_x, trail_y)
```

And the second panel:

```python
fig, (ax, ax_msd) = plt.subplots(1, 2, figsize=(11, 5.2),
                                 gridspec_kw={'width_ratios': [1.15, 1]})
msd_t, msd_v = [], []
msd_line, = ax_msd.plot([], [], 'b')
...
msd_t.append(frame)
msd_v.append(bx**2 + by**2)
msd_line.set_data(msd_t, msd_v)
ax_msd.relim(); ax_msd.autoscale_view()
```

`relim()` recomputes the data limits and `autoscale_view()` rescales the axes —
necessary because the curve is growing beyond the original limits.

---

## 10.3 The measurement run (no animation)

Drawing is ~100× slower than arithmetic, so the quantitative study lives in a
separate file with no graphics at all inside the loops:

```python
d2 = np.zeros((runs, frames))            # lab notebook: rows=runs, cols=time

for run in range(runs):
    x = np.random.uniform(-L, L, Np)     # RESET - the clean test tube
    y = np.random.uniform(-L, L, Np)
    bx, by = 0.0, 0.0
    bvx, bvy = 0.0, 0.0
    for t in range(frames):
        ... identical physics, no plotting ...
        d2[run, t] = bx**2 + by**2

msd = np.mean(d2, axis=0)                # average over runs (§6.7)
plt.plot(msd)
```

Note there is **no function** here and therefore **no `global`** — the loop is
the clock. Wrapping the physics in an uncalled `def` is the classic error, and
it produces a perfectly flat line at zero (a recipe on the shelf never cooks).

Interpretation of the result:

- Rising, roughly straight → diffusive, Einstein confirmed.
- Curved at the start → ballistic-to-diffusive crossover.
- Flattening at the end → the box walls limit how far it can roam (*confined
  diffusion*). Honest to point out.

---

## 10.4 Assumptions in this model — state them

Good modelling means owning the simplifications:

1. Molecules don't collide with **each other**, only with the big particle.
2. Collisions are treated as impulses along the line of centres; we don't track
   the molecule's post-collision velocity properly.
3. Molecule speed is fixed (`s` per frame) — a proxy for temperature, not a
   Maxwell–Boltzmann distribution.
4. Drag is a constant per-frame factor, not derived from Stokes' law.
5. Walls are absorbing-then-replacing rather than elastic reflectors.

Every one of these is defensible for the phenomenon being demonstrated, and
naming them is what a physicist does. Each is also a ready-made extension.

---

## Exercises

1. Set `drag = 1.0` (no damping) and watch. Describe what happens and explain it
   in terms of accumulated momentum.
2. Set `M = 200`. What happens to the trail, and why? Predict before running.
3. Add a counter of total collisions and display it in the title using
   `np.sum(hit)` accumulated over frames.
4. Change `s` (molecule speed) and observe the effect on the MSD gradient. What
   physical quantity is `s` standing in for?
5. Fit a straight line to the linear part of your MSD curve with `np.polyfit`
   and extract the diffusion coefficient D from gradient = 4D.
6. **Harder:** implement proper elastic hard-disc collisions — reflect the
   molecule's velocity about the line of centres as well as kicking the disc.
   Does the qualitative behaviour change?
7. **Break it:** move the reset lines outside the `for run` loop in the
   measurement file. Plot the MSD and explain the shape you get.

Solutions: `solutions/ch10_solutions.py`

---

## What you now know

- Brownian motion as the historical proof of atoms; Einstein 1905, Perrin 1908.
- Momentum-conserving impulses along the line of centres, and why the sign is
  Newton's third law.
- Why damping is required, and that the result is a Langevin model.
- `FuncAnimation`: the clock, `global`, keeping the object alive, `set_data`.
- Masks for collision detection with no loops.
- Separating the animated demo from the measurement run, and why.
- MSD ∝ t as the testable prediction, with ballistic and confined regimes visible.

Next: [Chapter 11 — Task 3: Planck and Einstein](11_task3_blackbody.md)
