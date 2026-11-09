# Chapter 4 — Lists and collections

**Goal:** store many values at once, index them, and know when to reach for a
list, a dictionary or a tuple.

---

## 4.1 Lists

A list holds items in order, in square brackets:

```python
temperatures = [3000, 4000, 5000, 5778, 6000]
metals = ["caesium", "sodium", "zinc"]
mixed = [1, "two", 3.0, True]        # legal, but rarely a good idea
empty = []                           # start empty and fill later
```

### Indexing — counting from zero

```python
temperatures[0]     # 3000   FIRST item
temperatures[1]     # 4000
temperatures[-1]    # 6000   LAST item
temperatures[-2]    # 5778   second from the end
```

Two things to burn in:

1. **Indexing starts at 0.** The first item is item zero. This is universal in
   programming and it exists because an index is really "how far from the start".
2. **`[-1]` is the last item.** You used this constantly:
   `x[-1], y[-1]` was the walker's final position.

### Slicing — taking a section

```python
temperatures[1:4]    # [4000, 5000, 5778]   from 1 up to (not including) 4
temperatures[:3]     # [3000, 4000, 5000]   from the start
temperatures[2:]     # [5000, 5778, 6000]   to the end
temperatures[::2]    # [3000, 5000, 6000]   every second one
```

The "up to but not including" rule is consistent with `range()` — the stop value
is always excluded. Annoying for a week, then invisible forever.

### Growing a list

```python
trail_x = []
trail_x.append(3.7)       # add one item to the end
trail_x.append(4.1)
print(len(trail_x))       # 2      len() gives the number of items
```

`.append()` is how the Brownian particle's trail was recorded — one position per
frame, growing forever:

```python
trail_x.append(bx)
trail_y.append(by)
```

Other useful operations:

```python
values = [5, 3, 9, 1]
values.sort()             # [1, 3, 5, 9]   sorts in place
len(values)               # 4
sum(values)               # 18
max(values), min(values)  # 9, 1
9 in values               # True    membership test
```

---

## 4.2 Lists are mutable — and shared

This surprises everyone once:

```python
a = [1, 2, 3]
b = a
b.append(4)
print(a)        # [1, 2, 3, 4]   -- a changed too!
```

Because `b = a` doesn't copy the list; it sticks a *second label* on the *same*
list (remember Chapter 2: names are labels). To genuinely copy:

```python
b = a.copy()       # or  b = a[:]
```

This bites in simulations when you think you saved a snapshot but actually saved
a live reference to something that keeps changing.

---

## 4.3 Tuples — lists that can't change

Round brackets instead of square:

```python
point = (3.0, 4.5)
n, l, m = (3, 2, 1)        # "unpacking" - three names at once
```

You cannot append to or modify a tuple. That's the point: they're for fixed
groupings, like coordinates or quantum-number triples. In the project:

```python
orbitals = [(1, 0, 0), (2, 0, 0), (2, 1, 0), ...]   # list of tuples
for n, l, m in orbitals:                            # unpacked in the loop
```

That's a list of quantum-number triples, unpacked into three variables each
time round. Clean and readable.

**Unpacking works generally**, which explains a line that once confused you:

```python
bx, by = 0.0, 0.0            # two assignments at once
Lm1, L0 = L0, new_value      # swap/rotate values simultaneously
```

The second form is used in the Laguerre polynomial recurrence — it updates two
variables *at the same time*, so the old value of `L0` is still available on the
right-hand side. Writing it as two separate lines would break the maths.

### The lonely comma

```python
dots, = ax.plot(x, y, 'b.')
```

`ax.plot` returns a *list* of drawn lines (usually with one item). The trailing
comma unpacks that single item out of the list. Without it, `dots` would be a
list, not a line, and `dots.set_data(...)` would fail. Now you know.

---

## 4.4 Dictionaries — lookup by name

A dictionary stores **key → value** pairs in curly brackets:

```python
metals = {'caesium': 2.10, 'sodium': 2.28, 'zinc': 4.31, 'copper': 4.70}

print(metals['sodium'])          # 2.28
metals['platinum'] = 5.65        # add a new entry
print(len(metals))               # 5
```

Looping over one:

```python
for name, W in metals.items():       # both key and value
    print(name, W)

for name in metals:                  # keys only
    print(name)
```

Dictionaries are the right tool when data has *names* rather than positions.
Compare the two ways of storing the same physics:

```python
# with two lists - fragile, easy to misalign
names = ['caesium', 'sodium']
works = [2.10, 2.28]

# with a dictionary - impossible to misalign
metals = {'caesium': 2.10, 'sodium': 2.28}
```

Every metal, series and beam in your project is stored as a dictionary for
exactly this reason.

---

## 4.5 Choosing the right container

| Need | Use | Why |
|---|---|---|
| Ordered values, will grow | **list** | `.append()` works |
| Fixed group (x,y) or (n,l,m) | **tuple** | can't be corrupted |
| Values with names | **dict** | lookup by meaning |
| Thousands of numbers for maths | **numpy array** (Ch 6) | fast, vectorised |

That last row matters: a Python list of 200 particle positions is the *wrong*
tool. It cannot do maths on all items at once and it's slow. Chapter 6 is where
you meet the right one.

Notice the project mixes both deliberately:

```python
trail_x, trail_y = [], []       # lists - they GROW each frame
x = np.random.uniform(...)      # array - fixed size, needs fast maths
```

Growing needs a list; maths needs an array. That's a real engineering decision,
and you can now explain it.

---

## Exercises

Create `ch04_exercises.py`.

1. Make a list of the first six Balmer wavelengths (656.3, 486.1, 434.0, 410.2,
   397.0, 388.9). Print the first, the last, and the middle two using slicing.
2. Build the list `[1, 4, 9, 16, 25]` using an empty list and `.append()` in a
   loop.
3. Make a dictionary of four metals and their work functions. Loop over it and
   print, for each, the cutoff wavelength in nm using `1240 / W_eV`.
4. Given `data = [3, 8, 2, 9, 4]`, print its length, sum, mean (sum/len), max
   and min — without numpy.
5. Predict, then test: what does this print?
   ```python
   a = [1, 2, 3]
   b = a
   b[0] = 99
   print(a[0])
   ```
   Then fix it so `a` is unaffected.
6. Store three orbitals as tuples in a list, loop over them unpacking into
   `n, l, m`, and print `n + l + m` for each.

---

## What you now know

- Lists: ordered, indexed from 0, `[-1]` is last, slicing excludes the stop.
- `.append()` grows a list; `len()`, `sum()`, `max()`, `in` inspect it.
- Assignment shares rather than copies; use `.copy()` when you mean copy.
- Tuples are fixed groupings; unpacking assigns several names at once, and the
  simultaneous form powers the polynomial recurrences.
- Dictionaries map names to values and prevent misaligned data.
- Lists grow; numpy arrays compute. Use each for its job.

Next: [Chapter 5 — Functions](05_functions.md)
