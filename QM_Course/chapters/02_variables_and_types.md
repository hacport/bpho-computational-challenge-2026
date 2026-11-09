# Chapter 2 — Variables, numbers and types

**Goal:** store values, do arithmetic reliably, and understand why
`0.1 + 0.2 != 0.3` — which matters more in physics code than anywhere else.

---

## 2.1 A variable is a label, not a box

```python
speed = 3.0
```

Most books say "a variable is a box that holds a value". That's a useful lie.
More accurately: `speed` is a **label stuck onto a value**. The `=` sign is not
maths — it does not mean "is equal to". It means **"make this name refer to this
value"**.

Which is why this makes sense in Python but not in algebra:

```python
n = 5
n = n + 1     # read: "new n is old n plus one"   -> n is now 6
```

You used this constantly in the project:

```python
x = x + s*np.cos(angles)     # new positions = old positions + this step
bvx = drag * bvx             # new velocity = old velocity, reduced
```

That pattern — `state = f(state)` — is the heartbeat of every simulation you will
ever write. A simulation is nothing more than that line, repeated.

### Naming rules and manners

- Letters, digits, underscores. Cannot start with a digit.
- Case matters: `Speed` and `speed` are different labels.
- Convention: lowercase with underscores — `step_size`, `ring_radius`.
- In physics code it is *good* practice to name variables after the symbols in
  the equation: `lam` for λ, `theta` for θ, `E0`, `bvx`. Someone reading your
  code with the textbook open should recognise it.

---

## 2.2 Types: what kind of value is it?

Every value in Python has a **type**. Four matter to you now:

| Type | Name | Example | Used in the project for |
|---|---|---|---|
| Integer | `int` | `n = 3` | quantum numbers, counts, loop indices |
| Decimal | `float` | `s = 0.5` | every physical quantity |
| Text | `str` | `name = "sodium"` | labels, titles |
| True/False | `bool` | `hit = True` | collision tests, masks |

Ask Python at any time:

```python
print(type(3))        # <class 'int'>
print(type(3.0))      # <class 'float'>
print(type("3"))      # <class 'str'>
print(type(3 > 2))    # <class 'bool'>
```

`3` and `3.0` and `"3"` are three different things. The last one is *text that
looks like a number* — you cannot do arithmetic with it:

```python
print("3" + 4)     # TypeError: can only concatenate str (not "int") to str
```

That error will bite you eventually. It means: you have a string where you
wanted a number. Fix with `int("3")` or `float("3.0")`.

---

## 2.3 Arithmetic

```python
7 + 2      # 9    addition
7 - 2      # 5    subtraction
7 * 2      # 14   multiplication
7 / 2      # 3.5  division — ALWAYS gives a float
7 // 2     # 3    floor division — throws away the remainder
7 % 2      # 1    modulo — the remainder itself
7 ** 2     # 49   power (NOT ^ — in Python ^ means something else entirely)
```

Two of these look obscure but earn their place:

**`//` floor division** — used in the orbital morphing animation to work out
which pair of states we're between:

```python
k = (frame // seg) % len(ms)
```

**`%` modulo** — "the remainder", perfect for anything cyclic. `frame % seg`
counts 0,1,2,...,seg-1,0,1,2,... forever. That's how an animation loops.

**Order of operations** is standard BIDMAS, and brackets are free. Use them:

```python
E = h*c / (lam*kB*T)      # correct
E = h*c / lam*kB*T        # WRONG - this is (h*c/lam)*kB*T
```

That single missing bracket is the most common physics-code bug in existence.
When a formula has a product on the bottom of a fraction, bracket it. Always.

---

## 2.4 Floats are approximations — and physicists must care

Run this:

```python
print(0.1 + 0.2)          # 0.30000000000000004
print(0.1 + 0.2 == 0.3)   # False
```

This is not a Python bug. Computers store decimals in **binary**, and just as
1/3 cannot be written exactly in decimal (0.3333...), 0.1 cannot be written
exactly in binary. Every float carries a tiny error, around 1 part in 10¹⁶.

Three consequences you must internalise:

**1. Never test floats with `==`.** Test whether the difference is small:

```python
if abs(a - b) < 1e-9:     # "close enough"
```

**2. Small errors accumulate over many operations.** In the Compton task the
printed "energy conservation residual" was `0.00e+00` — that's remarkable; more
often you'd see `1e-19`, which is *zero* in any physical sense.

**3. Subtracting two nearly-equal numbers is dangerous** (called *catastrophic
cancellation*). It's why the project uses `np.expm1(x)` instead of `np.exp(x)-1`
in Planck's law: when x is small, `exp(x)` is very close to 1, and subtracting
loses most of your significant figures. `expm1` computes the same thing
accurately. That single choice is a mark of code written by someone who knows
what they're doing.

---

## 2.5 Scientific notation and constants

Physics numbers are enormous or minuscule, so Python has scientific notation:

```python
h  = 6.62607015e-34     # 6.62607015 × 10⁻³⁴
c  = 2.99792458e8       # 2.99792458 × 10⁸
kB = 1.380649e-23
```

`e-34` means ×10⁻³⁴. No spaces allowed around the `e`.

**Style rule for physics code:** define constants once at the top of the file, in
SI units, with their symbol as the name. Never bury a raw number in a formula.
Compare:

```python
E = 6.626e-34 * 3e8 / lam            # what are these numbers?
E = h*c / lam                        # obviously the photon energy
```

The second version can be checked against a textbook at a glance. The first
can't. Every task file in your project follows this rule.

---

## 2.6 Printing values usefully: f-strings

Putting a variable inside a message:

```python
T = 5778
print(f"The Sun's surface is at {T} K")
```

The `f` before the quote makes it a **formatted string**; anything in `{ }` is
evaluated as code and inserted. You can format numbers too:

```python
lam = 0.000000502
print(f"peak at {lam*1e9:.0f} nm")        # peak at 502 nm
print(f"h = {6.62607015e-34:.4e} J s")    # h = 6.6261e-34 J s
print(f"error = {0.0006123*100:.2f} %")   # error = 0.06 %
```

The bit after the colon is the format spec:

| Spec | Meaning | Example output |
|---|---|---|
| `.0f` | fixed point, 0 decimals | `502` |
| `.3f` | fixed point, 3 decimals | `1.500` |
| `.4e` | scientific, 4 decimals | `6.6261e-34` |
| `>8` | right-align in 8 characters | `      42` |
| `.6f` | 6 decimals | `1.000000` |

Alignment is how the project's terminal tables line up neatly:

```python
print(f'{n:>3} {dx:>12.3e} {dp:>13.3e}')
```

Neat output is not vanity. Judges, markers and collaborators read your terminal
before they read your code.

---

## Exercises

Create `ch02_exercises.py`.

1. Store the electron mass, elementary charge and Planck's constant as
   variables with sensible names. Print each with 4 significant figures in
   scientific notation.
2. A photon has wavelength 486.1 nm. Compute its energy in joules, then in
   electronvolts (divide by e). Print both, formatted nicely. Check: you should
   get about 2.55 eV.
3. Predict, then check: what does `10 % 3` give? `10 // 3`? `-7 // 2`?
4. Write `0.1 + 0.2 == 0.3` and then write a version using `abs()` that
   correctly reports `True`.
5. **Break it:** compute `h*c/(lam*kB*T)` correctly, then delete the brackets
   and print both. By what factor do they differ, and why?
6. Using an f-string, print a line that reads exactly:
   `lambda = 656.3 nm  |  E = 1.89 eV` using variables, not typed text.

---

## What you now know

- `=` binds a name to a value; `state = f(state)` is the simulation heartbeat.
- Types: int, float, str, bool — and `"3"` is not `3`.
- `/`, `//`, `%`, `**`; bracket the denominators of fractions.
- Floats are approximate: never `==` them, and prefer `expm1` where it matters.
- Constants live at the top of the file, named after their symbols.
- f-strings with format specs give you clean, aligned scientific output.

Next: [Chapter 3 — Decisions and loops](03_decisions_and_loops.md)
