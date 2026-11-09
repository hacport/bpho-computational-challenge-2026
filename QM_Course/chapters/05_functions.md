# Chapter 5 — Functions

**Goal:** package code into reusable machines, understand `return` and scope, and
finally settle what `global` was doing in your Brownian motion file.

---

## 5.1 A function is a named machine

```python
def photon_energy(lam):
    return 6.62607015e-34 * 2.99792458e8 / lam
```

Anatomy:

- `def` — "I am defining a machine"
- `photon_energy` — its name
- `(lam)` — its **parameter**: the input it expects
- `:` and indentation — the body
- `return` — the value it hands back

**Defining is not running.** That block does nothing until you *call* it:

```python
E = photon_energy(500e-9)
print(E)
```

This is the single most important idea in the chapter, and it caused the
"flat zero" bug in your diffusion file: you wrapped 2000 ticks of physics inside
`def update(...)` and never called it. Python dutifully filed the recipe away
and did nothing. **A recipe on the shelf never cooks.**

---

## 5.2 Arguments and returns

Multiple inputs, comma separated:

```python
def kinetic_energy(m, v):
    return 0.5 * m * v**2

print(kinetic_energy(9.11e-31, 2.2e6))
```

**Returning several values** — this is how `random_walk` handed back a whole
path:

```python
def random_walk(N, s):
    ...
    return x, y          # returns a tuple

x, y = random_walk(1000, 1)   # unpacked into two names
```

**No return statement?** The function returns `None` — Python's word for
nothing. A function that only draws a graph or prints text legitimately returns
nothing.

**`return` ends the function immediately.** Anything after it in the same block
never runs. That's why `return` must be the *last* line of your animation
`update()` function.

### Default arguments

```python
def radial(n, l, r, Z=1):
    ...
```

`Z=1` means "if the caller doesn't say, use 1". So `radial(2, 1, r)` works
(hydrogen), and `radial(2, 1, r, Z=2)` works too (helium ion). Defaults let one
function serve many cases without extra code — this is exactly how your orbital
code supports any hydrogenic atom for free.

### Keyword arguments

```python
plt.plot(x, y, lw=0.8, color='red', label='walk')
```

`lw=`, `color=`, `label=` are **keyword arguments**: named, order-independent,
usually optional. Every matplotlib call you write uses them.

---

## 5.3 Scope: what a function can see

Variables created inside a function are **local** — they exist only during the
call and vanish afterwards:

```python
def f():
    secret = 42
    print(secret)     # fine

f()
print(secret)         # NameError: name 'secret' is not defined
```

Functions *can read* variables from outside:

```python
h = 6.626e-34

def energy(f):
    return h * f      # reads the global h - fine
```

But **assigning** to a name inside a function creates a *new local* variable,
shadowing the outside one:

```python
count = 0

def increment():
    count = count + 1      # UnboundLocalError!

increment()
```

Python sees the assignment, decides `count` is local, then finds you're reading
it before it exists. Hence the error.

---

## 5.4 `global` — and why animations need it

To genuinely modify an outside variable from inside a function:

```python
count = 0

def increment():
    global count
    count = count + 1     # now it works
```

Which brings us to this line from Task 2:

```python
def update(frame):
    global x, y, bx, by, bvx, bvy
```

`FuncAnimation` calls `update` once per frame. Each call must *change the world*
— molecule positions, particle velocity — and those changes must **survive to
the next frame**. Without `global`, every frame would edit private copies that
are thrown away, and nothing would ever move. That's the whole story.

**Style note:** professionals avoid `global` in large programs (it makes it hard
to know who changed what). For a small simulation script it's the clearest tool
available, and it is what nearly all matplotlib animation examples use. The
grown-up alternative is a class — mentioned in §5.7.

---

## 5.5 Docstrings

A string on the first line of a function documents it:

```python
def planck(lam, T):
    """Spectral radiance B(lambda, T) in W sr^-1 m^-3."""
    return (2*h*c**2 / lam**5) / np.expm1(h*c / (lam*kB*T))
```

Triple quotes allow multiple lines. `help(planck)` prints it. For physics code,
say what the function returns **and in what units** — units are where real
scientific bugs hide.

---

## 5.6 Why functions matter more than they look

Three reasons, all visible in your project:

**1. Reuse.** `random_walk` is called once for the single-walk figure, 4000 times
for the RMS study, and 50 times for the overlay. One definition, three
experiments.

**2. Naming.** `psi(n, l, m, x, y, z)` says what it is. The same maths inline
would be an unreadable smear.

**3. Testability.** A function you can call in isolation is a function you can
*check*. That's how the orbital verification works: call `radial()`, integrate
it, compare with the analytic value. Code buried inside a loop can't be tested
like that.

### The `__main__` guard

At the bottom of `task10_hydrogenic_orbitals.py`:

```python
if __name__ == '__main__':
    ...all the plotting...
```

Meaning: "only run this part if the file is being executed *directly*". When
another file does `from task10_hydrogenic_orbitals import psi`, Python runs the
file to learn the definitions — and this guard stops it also drawing nine
orbital plots you didn't ask for. Without it, the molecular-orbital file would
open the whole gallery every time it imported one function.

---

## 5.7 A glimpse of classes (optional)

A **class** bundles data and functions together:

```python
class Walker:
    def __init__(self, s):
        self.s = s
        self.x = 0.0
        self.y = 0.0

    def step(self):
        angle = np.random.uniform(0, 2*np.pi)
        self.x += self.s*np.cos(angle)
        self.y += self.s*np.sin(angle)

w = Walker(0.5)
w.step()
print(w.x, w.y)
```

`self` refers to the particular object. Classes are how you'd avoid `global`
entirely in a bigger program. You don't need them for this project, but you
should recognise them — and Chapter 22 offers a class-based rewrite as a
stretch challenge.

---

## Exercises

Create `ch05_exercises.py`.

1. Write `de_broglie(V)` returning the electron wavelength for accelerating
   voltage V, using λ = h/√(2mₑeV). Test with V=1000 (expect ≈ 3.9e-11 m).
2. Write `bohr_energy(n)` returning −13.6/n² eV, then use it in a loop to print
   the first five levels.
3. Write `transition(n1, n2)` that returns *two* values: photon energy in eV and
   wavelength in nm. Call it for (2,3) — expect ≈1.89 eV, ≈656 nm.
4. **Break it:** write a function that ends with `return result`, then add a
   `print("done")` line *after* the return. Run it. Explain the output.
5. Write a function with a default argument `def escape_velocity(M, R,
   G=6.674e-11)` and call it both with and without G.
6. Copy the `count` example from §5.3, watch it fail, then fix it with `global`.
   Then fix it a *second* way — by returning the new value instead. Which is
   cleaner?

---

## What you now know

- `def` files a recipe; calling it runs it. Defining ≠ running.
- Parameters, multiple returns via tuples, defaults, keyword arguments.
- Local scope, reading globals, and why assignment creates locals.
- `global` lets animation state survive between frames — that's why Task 2 needs it.
- Docstrings state purpose *and units*.
- Functions give reuse, naming and testability; `__main__` guards make files importable.

**End of Part 1.** You can now read every non-numpy line in your project.

Next: [Chapter 6 — numpy](06_numpy.md)
