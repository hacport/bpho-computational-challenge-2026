# Chapter 3 — Decisions and loops

**Goal:** make code choose and repeat. By the end you can write the nested loop
structure that powers the Einstein diffusion experiment.

---

## 3.1 Indentation is the grammar

Most languages use `{ }` to group lines. Python uses **indentation** — spaces at
the start of the line. This is not decoration; it is the syntax.

```python
if temperature > 5000:
    print("hot star")          # inside the if  (4 spaces)
    print("probably white")    # also inside
print("done")                  # outside - always runs
```

Rules:

- The line introducing a block ends with a colon `:`.
- Everything indented under it belongs to that block.
- Use **4 spaces** per level. VS Code does it when you press Tab.
- Be consistent — mixing tabs and spaces gives `IndentationError`.

You met this the hard way: in the Einstein diffusion file, one line had 9 spaces
instead of 8 and Python refused to run. Indentation *is* meaning.

---

## 3.2 if / elif / else

```python
KE = photon_energy - work_function

if KE > 0:
    print("electron emitted")
elif KE == 0:
    print("exactly at threshold")
else:
    print("no emission")
```

- `if` — test first condition
- `elif` — "else if", test another (as many as you like)
- `else` — everything not caught above (optional)

Only **one** branch ever runs.

### Comparison operators

| Operator | Means |
|---|---|
| `==` | equal to (two equals! one is assignment) |
| `!=` | not equal to |
| `<` `>` | less / greater than |
| `<=` `>=` | less than or equal / greater than or equal |

### Combining conditions

```python
if lam > 380 and lam < 740:
    print("visible")

if metal == "zinc" or metal == "copper":
    print("needs UV")

if not emitted:
    print("nothing happened")
```

`and` needs both true; `or` needs at least one; `not` flips it.

Python also allows the beautiful mathematical form:

```python
if 380 < lam < 740:      # exactly like the maths notation
```

---

## 3.3 The `for` loop

A `for` loop repeats once for each item in a collection.

```python
for T in [3000, 4000, 5000, 5778]:
    print(f"T = {T} K, peak at {2.898e-3/T*1e9:.0f} nm")
```

Read it as: "for each value in this list, call it T, and do the block."

### `range()` — counting loops

```python
for i in range(5):
    print(i)          # 0 1 2 3 4
```

`range(5)` gives 0,1,2,3,4 — **five numbers, starting at zero, stopping before
five**. This zero-start trips up every beginner. Variants:

```python
range(5)          # 0 1 2 3 4
range(2, 6)       # 2 3 4 5        (start, stop)
range(1, 10, 2)   # 1 3 5 7 9      (start, stop, step)
```

In the project:

```python
for n2 in range(n1+1, n1+15):    # transitions from level n1+1 upwards
for run in range(runs):          # repeat the whole experiment
for i in range(50):              # 50 random walks
```

### When you need both position and value

```python
for i, T in enumerate([3000, 4000, 5000]):
    print(i, T)      # 0 3000 / 1 4000 / 2 5000
```

`enumerate` hands you the index alongside the item — used in the project to
stack plots at different vertical offsets.

### Looping over pairs

```python
metals = {'sodium': 2.28, 'zinc': 4.31}
for name, W in metals.items():
    print(f"{name} has work function {W} eV")
```

A **dictionary** (`{key: value}`) is covered next chapter; `.items()` gives you
both parts at once. This exact pattern draws every metal line in Task 4.

---

## 3.4 The `while` loop

Repeats as long as a condition holds:

```python
n = 1
while 2**n < 1000:
    n = n + 1
print(f"2^{n} is the first power of two above 1000")
```

Use `for` when you know how many repeats; `while` when you don't. **Danger:** if
the condition never becomes false, the program hangs forever. Press `Ctrl+C` in
the terminal to stop a runaway program.

You'll notice the project uses almost no `while` loops. Physics simulations
usually run for a known number of steps.

---

## 3.5 Nested loops — the structure of an experiment

A loop inside a loop. This is the shape of the Einstein diffusion study:

```python
for run in range(30):              # OUTER: repeat the experiment 30 times
    reset_everything()
    for t in range(2000):          # INNER: 2000 ticks of time
        do_one_tick_of_physics()
        record(run, t)
```

The inner loop runs **completely** for each single pass of the outer loop:
30 × 2000 = 60,000 ticks total.

Understanding which loop does what is understanding the experiment:

- **inner loop** = time passing within one experiment
- **outer loop** = repeating the whole experiment to average out randomness

Get these the wrong way round and your data is meaningless. Note also the
`reset_everything()` at the top of the outer loop — the clean test tube. Forget
it and run 2 secretly continues run 1.

---

## 3.6 break and continue

```python
for i in range(100):
    if i*i > 500:
        break        # leave the loop entirely
    if i % 2 == 0:
        continue     # skip to the next iteration
    print(i)
```

Useful, but in numerical work you rarely need them. Prefer clear conditions.

---

## 3.7 Loops you should NOT write

Here is the most important sentence in Part 1:

> In scientific Python, a loop over thousands of numbers is usually a mistake.

This works but is slow:

```python
dx = []
for angle in angles:
    dx.append(0.5 * math.cos(angle))
```

This does the same thing about 100 times faster, in one line:

```python
dx = 0.5 * np.cos(angles)
```

That's **vectorisation**, and it's the whole subject of Chapter 6. Loops are for
*experiments* (repeat this simulation 30 times); numpy is for *numbers* (do this
maths to 200 particles at once). Knowing which to use is the difference between
a program that runs in 3 seconds and one that runs in 5 minutes.

---

## Exercises

Create `ch03_exercises.py`.

1. Print the first 10 square numbers using a `for` loop.
2. For each metal below, print whether visible light (take 500 nm) can eject an
   electron. Work functions in eV: caesium 2.10, sodium 2.28, zinc 4.31,
   copper 4.70. (Photon energy at 500 nm ≈ 2.48 eV.)
3. Use a nested loop to print a 5×5 multiplication table, aligned neatly with
   f-string width formatting.
4. Hydrogen: loop over `n1` from 1 to 3, and inside, `n2` from `n1+1` to `n1+4`,
   printing the photon energy `13.6 * (1/n1**2 - 1/n2**2)` eV for each
   transition.
5. **Break it:** take exercise 4 and remove the indentation on the print line so
   it sits at the outer level. What changes about the output, and why?
6. Write a `while` loop that starts at n=1 and finds the smallest n where
   `n**2 > 10000`.

---

## What you now know

- Indentation defines blocks; the colon opens them.
- `if / elif / else` with comparison and logical operators.
- `for` with lists, `range`, `enumerate` and `.items()`.
- `while` for unknown repeat counts (and `Ctrl+C` to escape).
- Nested loops = inner is time, outer is repetition; reset inside the outer loop.
- Loops are for experiments; numpy is for numbers.

Next: [Chapter 4 — Lists and collections](04_lists_and_collections.md)
