# Python cheat sheet

Everything from Part 1, on one page.

## Running

```
python file.py          run a script
python                  interactive mode  (exit() to leave)
pip install numpy       install a library
Ctrl+C                  stop a runaway program
```

## Variables and types

```python
n = 5                # int
s = 0.5              # float
name = "sodium"      # str
flag = True          # bool
type(x)              # ask what something is
int("3"), float("3.0"), str(3)     # convert
```

## Arithmetic

```python
+  -  *  /           / always gives a float
//                   floor division  (7//2 = 3)
%                    remainder       (7%2 = 1)
**                   power           (NOT ^)
abs(x), round(x, 3), min(a,b), max(a,b)
6.626e-34            scientific notation
```

## Strings and f-strings

```python
f"lambda = {lam:.1f} nm"        # 1 decimal place
f"{h:.4e}"                      # scientific, 4 dp
f"{name:>10}"                   # right-align in 10 chars
f"{x:.2f} %"                    # percentage
'single' or "double"            # both fine
"""triple for
multiple lines"""
```

## Comparison and logic

```python
==  !=  <  >  <=  >=
and  or  not
380 < lam < 740                 # chained, like maths
abs(a - b) < 1e-9               # how to compare floats
```

## Control flow

```python
if condition:
    ...
elif other:
    ...
else:
    ...

for item in collection:
    ...
for i in range(5):              # 0,1,2,3,4
for i in range(2, 10, 2):       # 2,4,6,8
for i, v in enumerate(lst):     # index and value
for k, v in d.items():          # dict key and value
for a, b in zip(list1, list2):  # two lists in step

while condition:
    ...

break        # leave the loop
continue     # skip to next iteration
```

## Lists

```python
lst = [1, 2, 3]
lst[0]      lst[-1]      lst[1:3]     lst[::2]
lst.append(x)
len(lst)  sum(lst)  max(lst)  min(lst)  sorted(lst)
x in lst
lst.copy()                      # a real copy, not a second label
```

## Tuples and unpacking

```python
point = (3.0, 4.5)
x, y = point
a, b = b, a                     # simultaneous swap
dots, = ax.plot(...)            # unpack a one-item list
```

## Dictionaries

```python
d = {'sodium': 2.28, 'zinc': 4.31}
d['sodium']
d['copper'] = 4.70
for k, v in d.items(): ...
```

## Functions

```python
def name(arg1, arg2, optional=default):
    """Docstring: what it returns, in what units."""
    return value

def two():
    return a, b
x, y = two()

f(1, 2)                # positional
f(1, 2, lw=0.8)        # keyword
```

## Scope

```python
global x, y            # modify outer variables from inside a function
```

## Modules

```python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from mymodule import myfunction

if __name__ == '__main__':
    ...                # only runs when executed directly
```

## Files and processes

```python
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
os.path.join(HERE, 'file.py')
subprocess.Popen([sys.executable, script], cwd=HERE)
```

## Style rules for physics code

1. Constants at the top, SI units, named after their symbols.
2. Bracket the denominators of fractions.
3. Convert units at the boundary (eV→J, deg→rad), then work in SI.
4. Name variables after the equation's symbols.
5. One file per experiment; separate the model from the plotting.
6. Docstrings state units.
7. Print results with formatted alignment.
