# Error messages decoded

Read the **last line first** — that's the actual message. Everything above is the
trail showing how Python got there.

---

## SyntaxError

**`SyntaxError: invalid syntax`**
Python can't parse the line. Look at the line *before* the one reported — a
missing closing bracket makes Python blame the next line.

**`unterminated string literal`** — a quote was opened and never closed.

**`unexpected EOF while parsing`** — a bracket or block was left open at the end
of the file.

**`expected ':'`** — you forgot the colon after `if`, `for`, `def`, `while`.

---

## IndentationError / TabError

**`expected an indented block`** — a line ending in `:` must be followed by
indented lines.

**`unexpected indent`** — a line has spaces it shouldn't.

**`unindent does not match any outer indentation level`** — inconsistent depths.
*You hit this with 9 spaces instead of 8.* Fix: select all, use VS Code's
"Convert indentation to spaces", indent 4 per level.

**`TabError`** — tabs mixed with spaces. Never use tabs.

---

## NameError

**`name 'x' is not defined`**
Causes, in order of likelihood:
1. Typo (`lenght` vs `length`)
2. Used before it was created — check the order of your lines
3. Defined inside a function, used outside (local scope, Ch 5 §5.3)
4. Forgot to catch a return value: `random_walk(1000, 1)` without `x, y =`

**`UnboundLocalError: local variable 'x' referenced before assignment`**
You assigned to a global variable inside a function without declaring `global x`.
This is the animation bug from Chapter 5 §5.4.

---

## TypeError

**`can only concatenate str (not "int") to str`** — `"3" + 4`. Convert with
`int()`/`float()`, or use an f-string.

**`'float' object is not subscriptable`** — you wrote `x[0]` where x is a single
number, not an array. Usually means a function returned a scalar when you
expected an array.

**`'numpy.ndarray' object is not callable`** — you wrote `f(x)` where `f` is an
array. Often a name collision: a variable overwrote a function name.

**`unsupported operand type(s)`** — check the types of both sides with `type()`.

**`missing 1 required positional argument`** — a function call is short an
argument. Also happens if you forget `self` in a class method.

---

## ValueError

**`operands could not be broadcast together with shapes (200,) (50,)`**
Two arrays of incompatible sizes in one operation. Print `a.shape` and `b.shape`
to find which. Very common when a mask and an array have got out of step.

**`x and y must have same first dimension`** (matplotlib)
Your x and y arrays are different lengths. Classic cause: forgetting that
`concatenate(([0], cumsum(dx)))` gives N+1 points while another array has N.

**`The truth value of an array with more than one element is ambiguous`**
You used `if some_array:`. Python doesn't know what a whole array of True/False
means as one condition. Use `np.any(...)`, `np.all(...)`, or a scalar test.

**`math domain error`** — `sqrt` of a negative, `log` of ≤ 0, `arcsin` of >1.
Check your physics: it usually means an unphysical intermediate value.

---

## IndexError

**`index 200 is out of bounds for axis 0 with size 200`**
Valid indices are 0…199. Off-by-one: remember `range(200)` stops at 199, and
`a[-1]` is the safe way to get the last item.

---

## ZeroDivisionError / warnings

**`divide by zero encountered`** (a numpy *warning*, not an error — it returns
`inf` and carries on)
Something in a denominator hit zero. Typical: r = 0 at the origin (fixed with
`+ 1e-12`), or T = 0 in a heat-capacity formula (start the range at 1).

**`invalid value encountered`** — produced a NaN, usually 0/0 or sqrt of a
negative. NaN then spreads through every subsequent calculation, so trace it to
its source.

---

## ImportError / ModuleNotFoundError

**`No module named 'numpy'`** — run `pip install numpy`. If it's installed but
still missing, you have several Pythons; check with `python -c "import sys;
print(sys.executable)"`.

**`cannot import name 'psi' from ...`** — the name doesn't exist in that file
(check spelling), or a circular import.

---

## AttributeError

**`'list' object has no attribute 'set_data'`**
You forgot the trailing comma: `dots, = ax.plot(...)` (Ch 4 §4.3).

**`module 'numpy' has no attribute 'trapz'`**
Renamed to `np.trapezoid` in recent numpy.

---

## Silent failures (no error, wrong result)

The dangerous ones. Symptoms and causes:

| Symptom | Likely cause |
|---|---|
| Plot is flat at zero | Physics wrapped in a `def` that's never called (Ch 5 §5.1) |
| Animation window opens but nothing moves | Missing `global`, or you didn't keep `anim = ...` |
| Every repeat gives identical results | Seeded inside the loop |
| Results drift across runs | Forgot to reset state at the start of each run |
| All buttons do the same thing | Late-binding closure in a lambda (Ch 20 §20.6) |
| Answer off by a large factor | Missing brackets in a fraction denominator |
| Answer off by exactly 10^n | Unit conversion (eV vs J, nm vs m) |
| Angles nonsense | Degrees where radians were needed |
| Curve looks the right shape but the wrong height | Normalisation missing |

---

## A debugging method that always works

1. **Read the last line** of the traceback.
2. **Print the shapes and types** of everything involved:
   `print(type(x), np.shape(x))`
3. **Print intermediate values.** Where does it stop being what you expect?
4. **Shrink the problem.** N = 3 instead of 2000; one metal instead of five.
5. **Check the physics by hand** for one case with a calculator.
6. **Comment out half.** Binary search until the culprit is isolated.
7. **Explain the code out loud, line by line.** You will find it yourself —
   this genuinely works and has a name: rubber-duck debugging.
