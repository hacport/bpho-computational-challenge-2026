# Chapter 6 — numpy: arrays and vectorised thinking

**Goal:** the single most valuable chapter in this course. Learn to do maths on
thousands of numbers at once, and understand every numpy call in your project.

---

## 6.1 The idea

A Python list holds *things*. A numpy **array** holds *numbers of the same type*,
laid out in one solid block of memory, so the computer can do arithmetic on all
of them at once.

```python
import numpy as np          # 'np' is universal convention

lst = [1, 2, 3, 4]
arr = np.array([1, 2, 3, 4])

print(lst * 2)     # [1, 2, 3, 4, 1, 2, 3, 4]   list: repeats!
print(arr * 2)     # [2 4 6 8]                  array: multiplies!
```

That difference is the whole point. With arrays, `*` means *multiply every
element* — which is what a physicist means.

```python
angles = np.array([0.0, 1.57, 3.14])
dx = 0.5 * np.cos(angles)     # cosine of all three, scaled - one line
```

This is **vectorisation**: expressing "do this to every number" as a single
operation. It is faster (numpy loops in C, not Python), shorter, and reads like
the equation it implements.

---

## 6.2 Making arrays

```python
np.array([1, 2, 3])              # from a list
np.zeros(5)                      # [0. 0. 0. 0. 0.]
np.ones(3)                       # [1. 1. 1.]
np.full(4, 7.0)                  # [7. 7. 7. 7.]
np.zeros((30, 2000))             # a 30 x 2000 GRID of zeros
np.arange(1, 8)                  # [1 2 3 4 5 6 7]   like range()
np.linspace(0, 1, 5)             # [0.   0.25 0.5  0.75 1.  ]
```

**`linspace` is the workhorse of physics plotting.** `np.linspace(a, b, n)` gives
`n` evenly spaced points from `a` to `b` **inclusive**. Every graph in your
project starts with one:

```python
lam = np.linspace(1e-8, 3e-6, 2000)      # 2000 wavelengths for Planck's law
theta = np.linspace(0.001, np.pi, 500)   # 500 scattering angles for Compton
r = np.linspace(0, 60, 20000)            # 20000 radii for orbital integration
```

More points = smoother curve and more accurate integration, at the cost of
speed. 500–2000 is usually plenty for a graph; 20000 for careful integration.

`np.arange` vs `np.linspace`: arange takes a *step size* and excludes the end;
linspace takes a *number of points* and includes it. For plotting, use linspace.

---

## 6.3 Shape

Every array has a shape — its dimensions.

```python
a = np.zeros(5)
print(a.shape)         # (5,)      one-dimensional, 5 items

b = np.zeros((30, 2000))
print(b.shape)         # (30, 2000)  two-dimensional: 30 rows, 2000 columns
print(b.size)          # 60000       total number of elements
```

Two-dimensional arrays are grids. The diffusion experiment used one as a lab
notebook: **row = which run, column = which time step**.

```python
d2 = np.zeros((runs, frames))
d2[run, t] = bx**2 + by**2       # write into row 'run', column 't'
```

Reading `d2[3, 100]`: "run number 3, time step 100". Rows first, then columns —
same as matrices in maths.

---

## 6.4 Element-wise maths and broadcasting

All the arithmetic operators work element-wise:

```python
a = np.array([1.0, 2.0, 3.0])
b = np.array([10.0, 20.0, 30.0])

a + b        # [11. 22. 33.]
a * b        # [10. 40. 90.]
b / a        # [10. 10. 10.]
a ** 2       # [1. 4. 9.]
```

Mixing an array with a single number is called **broadcasting** — the number is
applied to every element:

```python
a * 5           # [5. 10. 15.]
a + 100         # [101. 102. 103.]
1 / np.sqrt(V)  # works on the whole array at once
```

This is why the physics formulas look exactly like the textbook:

```python
def planck(lam, T):
    return (2*h*c**2 / lam**5) / np.expm1(h*c / (lam*kB*T))
```

`lam` is 2000 wavelengths; every operation applies to all of them; the result is
2000 radiances. One line, no loop, and it *reads like Planck's law*.

### Maths functions

```python
np.sin, np.cos, np.tan, np.arcsin, np.arctan2
np.sqrt, np.exp, np.log, np.abs
np.expm1(x)        # exp(x) - 1, accurately for small x
np.degrees, np.radians
np.pi              # 3.14159...
```

Use `np.` versions, not the `math` module, when working with arrays — `math.cos`
only handles one number at a time.

**`np.arctan2(y, x)`** deserves a note: it computes the angle of the point
(x, y) *and gets the quadrant right*, unlike plain `arctan(y/x)`. Your orbital
code uses it to find the azimuthal angle φ, and the Compton code to find the
recoil angle.

---

## 6.5 Indexing, slicing and the last element

Same rules as lists:

```python
x[0]        # first
x[-1]       # last  -- the walker's final position
x[10:20]    # a slice
x[::2]      # every second element
x[f > 1e15] # <- see next section
```

For 2D arrays, use a comma:

```python
d2[5, 100]      # single element: row 5, column 100
d2[5, :]        # the whole of row 5      (all time steps of run 5)
d2[:, 100]      # the whole of column 100 (all runs at time 100)
```

---

## 6.6 Boolean masks — the most powerful idea here

Compare an array with a number and you get an array of True/False:

```python
dist = np.array([2.0, 7.0, 4.0, 9.0])
hit = dist < 5
print(hit)            # [ True False  True False]
```

That's a **mask**. Use it as an index to select only the True positions:

```python
print(dist[hit])      # [2. 4.]
```

And you can *assign* through it:

```python
dist[hit] = 0
print(dist)           # [0. 7. 0. 9.]
```

This is how collision detection works without a single `if`:

```python
dist = np.sqrt((x - bx)**2 + (y - by)**2)   # 200 distances, one line
hit = dist < R                              # 200 True/False
ux = (x[hit] - bx) / dist[hit]              # only the colliders
x[hit] = bx + R*ux                          # move only them
```

And how the photoelectric graph refuses to draw below cutoff:

```python
V[f < f0] = np.nan       # NaN = "not a number"; matplotlib skips it
```

Companion functions:

```python
np.any(hit)      # True if ANY element is True
np.all(hit)      # True only if ALL are
np.sum(hit)      # counts the Trues (True counts as 1)
np.where(hit)    # gives the positions where True
```

`if np.any(hit):` in your code means "did anything collide this frame?" — one
cheap test before doing the collision maths.

---

## 6.7 Reductions: turning many numbers into one

```python
np.sum(a)          # total
np.mean(a)         # average
np.max(a), np.min(a)
np.argmax(a)       # POSITION of the maximum, not its value
np.std(a)          # standard deviation
```

`argmax` is how you found the Bohr radius:

```python
peak_1s = r[np.argmax(r**2 * radial(1, 0, r)**2)]
```

Read it inside-out: compute the radial probability at every radius → find the
*index* of the biggest → look up the radius at that index. Answer: 0.999 a₀.
That's a numerical measurement of a physical constant from your own model.

### The `axis` argument

On a 2D array you can reduce along one direction:

```python
msd = np.mean(d2, axis=0)     # average DOWN the columns -> one value per time
np.mean(d2, axis=1)           # average ACROSS the rows  -> one value per run
```

`axis=0` collapses rows (the 30 runs), leaving 2000 time points. That is
precisely "average the experiments together, keeping the time axis" — the whole
Einstein diffusion result in one call.

Mnemonic: **axis=0 collapses the rows, axis=1 collapses the columns.**

---

## 6.8 Cumulative operations

```python
steps = np.array([1, 2, 3, 4])
np.cumsum(steps)        # [1 3 6 10]   running total
```

Each output is the sum of everything up to that point. Which is exactly how you
turn *steps* into *positions*:

```python
x = np.cumsum(dx)       # where I am after each step
```

Add the starting point at the front:

```python
x = np.concatenate(([0], np.cumsum(dx)))
```

`np.concatenate` glues arrays together — here, a one-element array `[0]` in
front of the path so the walk begins at the origin.

---

## 6.9 Clipping and other tidy-ups

```python
np.clip(x, -L, L)       # anything below -L becomes -L, above L becomes L
```

Used for the box walls: escaping molecules are planted on the wall. Simple,
fast, and physically defensible as a crude reflecting boundary.

```python
np.round(a, 3)
np.sort(a)
np.unique(a)
np.trapezoid(y, x)      # numerical integration - Chapter 15
np.polyfit(x, y, 1)     # straight-line fit - Chapter 12
np.meshgrid(gx, gy)     # 2D coordinate grids - Chapter 18
```

Each of these gets its own proper treatment in the chapter where the project
first uses it.

---

## 6.10 Speed — see it for yourself

Type this and run it. It is worth the 30 seconds.

```python
import numpy as np, time

n = 2_000_000
a = np.random.uniform(0, 1, n)

t0 = time.time()
total = 0.0
for value in a:
    total += value * 2
t1 = time.time()

t2 = time.time()
total2 = np.sum(a * 2)
t3 = time.time()

print(f"loop:  {t1-t0:.3f} s")
print(f"numpy: {t3-t2:.3f} s")
print(f"speedup: {(t1-t0)/(t3-t2):.0f}x")
```

Typically 50–200× faster. That factor is the difference between your Brownian
animation running smoothly and stuttering; between the diffusion study taking 20
seconds and 20 minutes.

---

## Exercises

Create `ch06_exercises.py`.

1. Make `np.linspace(0, 2*np.pi, 9)` and print its sine. Which entries should be
   zero? Are they *exactly* zero? Explain (Chapter 2 §2.4).
2. Create 1000 random angles, convert to dx, dy with step size 2, and use cumsum
   to build a path. Print the final position and the distance from the origin.
3. Make `d = np.array([3.0, 7.0, 1.0, 9.0, 5.0])`. Using a mask, print only the
   values below 6, count how many there are, and set them all to zero.
4. Build a 4×6 array of zeros. Fill row `i`, column `j` with `i*j` using nested
   loops. Then print the mean of each row (`axis=1`) and each column (`axis=0`).
5. Verify `np.argmax` behaviour: for `np.array([5, 2, 9, 4])`, print both
   `np.max` and `np.argmax` and state the difference in one sentence.
6. **Break it:** compute `np.exp(x) - 1` and `np.expm1(x)` for
   `x = 1e-12`. Print both with `.20e` formatting. Which is right, and why does
   it matter for Planck's law at long wavelengths?
7. Run the speed test in §6.10 and write the speedup factor in a comment.

---

## What you now know

- Arrays do maths element-wise; broadcasting applies scalars to everything.
- `linspace` builds the x-axis of every physics graph; shape describes dimensions.
- 2D arrays are grids — `[row, column]`; `axis=0` averages down the runs.
- Boolean masks select and modify subsets: collisions, cutoffs, filters.
- `cumsum` turns steps into positions; `concatenate` adds the origin.
- `argmax` finds *where*, not *what* — how you measured the Bohr radius.
- Vectorised code is 50–200× faster than looping, and reads like physics.

Next: [Chapter 7 — matplotlib](07_matplotlib.md)
