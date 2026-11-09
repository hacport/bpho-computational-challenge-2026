# numpy cheat sheet

## Creating arrays

```python
np.array([1, 2, 3])
np.zeros(5)                 np.zeros((30, 2000))     # 1D / 2D
np.ones(3)                  np.full(4, 7.0)
np.ones_like(x)             np.zeros_like(x)         # same shape as x
np.arange(1, 8)             # 1..7, step-based, excludes stop
np.linspace(0, 1, 5)        # 5 points, includes both ends  <- use for plots
np.meshgrid(gx, gy)         # 2D coordinate grids
```

## Inspecting

```python
a.shape      a.size      a.dtype      len(a)
```

## Element-wise maths (vectorised)

```python
a + b   a - b   a * b   a / b   a ** 2
np.sin np.cos np.tan np.arcsin np.arccos np.arctan
np.arctan2(y, x)            # correct quadrant
np.sqrt np.exp np.log np.abs
np.expm1(x)                 # exp(x)-1, accurate for small x
np.degrees np.radians
np.pi
```

## Indexing and slicing

```python
a[0]  a[-1]  a[2:5]  a[::2]
d2[row, col]     d2[3, :]     d2[:, 100]
```

## Boolean masks

```python
hit = dist < R              # array of True/False
a[hit]                      # select
a[hit] = 0                  # assign to selection
np.any(hit)  np.all(hit)  np.sum(hit)  np.where(hit)
np.where(cond, a, b)        # vectorised if-else
mask1 & mask2               # AND   (use &, not 'and')
mask1 | mask2               # OR
~mask                       # NOT
```

## Reductions

```python
np.sum  np.mean  np.std  np.max  np.min
np.argmax(a)                # POSITION of max
np.mean(d2, axis=0)         # average down columns (over runs)
np.mean(d2, axis=1)         # average across rows
```

## Accumulation and joining

```python
np.cumsum(a)                            # running total
np.concatenate(([0], np.cumsum(dx)))    # prepend the origin
np.clip(a, low, high)                   # limit to a range
```

## Fitting and integrating

```python
m, c = np.polyfit(x, y, 1)      # least-squares straight line
np.trapezoid(y, x)              # trapezium-rule integral (was np.trapz)
np.gradient(y, x)               # numerical derivative
```

## Random numbers

```python
np.random.uniform(0, 2*np.pi, N)
np.random.normal(mean, sd, N)
np.random.binomial(n, p)

rng = np.random.default_rng(seed)       # preferred, reproducible
rng.uniform(...)   rng.normal(...)   rng.integers(0, 2, N)
```

## Special values

```python
np.nan          # "not a number" - matplotlib draws nothing there
np.inf
np.isnan(a)
```

## Gotchas

| Trap | Fix |
|---|---|
| `and`/`or` on arrays | use `&` / `\|` with brackets |
| `a == b` for floats | `np.allclose(a, b)` |
| `np.arange` end point excluded | use `linspace` for plots |
| Looping over thousands of elements | vectorise |
| `a = b` shares data | `b = a.copy()` |
| Integer division surprises | `/` gives float, `//` floors |
