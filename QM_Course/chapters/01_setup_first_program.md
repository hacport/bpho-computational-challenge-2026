# Chapter 1 — Setup and your first program

**Goal:** understand what Python actually *is*, run a program, and read an error
message without panicking.

---

## 1.1 What is Python, really?

A computer only understands numbers. Python is a **translator**: you write
instructions in something close to English, and the Python *interpreter* turns
them into machine instructions, one line at a time, top to bottom.

Three things live on your computer:

| Thing | What it is |
|---|---|
| **The interpreter** (`python.exe`) | The translator program. It reads your file and does what it says. |
| **Your script** (`something.py`) | A plain text file with your instructions. |
| **The editor** (VS Code) | A text editor that colours your code and has a Run button. It does not run anything itself — it calls the interpreter. |

That distinction matters. When something says *"python is not recognised"*, that
is the computer failing to find the **interpreter**, not a problem with your code.

---

## 1.2 Checking your setup

Open VS Code. Open a terminal inside it: menu **Terminal → New Terminal**. A
panel appears at the bottom. Type this and press Enter:

```
python --version
```

You should see something like `Python 3.12.1`. Any version 3.8 or above is fine.

Now install the two libraries this whole course depends on:

```
pip install numpy matplotlib
```

`pip` is Python's package installer — it downloads code other people wrote so you
don't have to write it yourself. `numpy` does fast maths on lots of numbers;
`matplotlib` draws graphs. You'll meet both properly in Part 2.

---

## 1.3 Your first program

In VS Code: **File → New File**, then **File → Save As**, and call it
`hello.py`. The `.py` extension is what makes it a Python file.

Type this (type it — don't paste):

```python
print("Hello. I am going to learn quantum physics with this thing.")
```

Save with `Ctrl+S`. Run it by pressing the ▷ play button top-right, or by typing
in the terminal:

```
python hello.py
```

The text appears in the terminal. That's it — you've written a program.

### What just happened, precisely

- `print` is a **function**: a named machine that does a job.
- The **brackets** `( )` mean "run this function now".
- What's inside the brackets is the **argument** — the thing you're giving it.
- The **quote marks** mean "this is text, not code". Text in programming is
  called a **string** (a string of characters).

Remove the quote marks and run it again. You'll get an error — read the next
section before you fix it.

---

## 1.4 How to read an error message

Errors are not punishment. They are the interpreter telling you exactly where it
got confused. Beginners panic at red text; experienced programmers read it.

Try running this deliberately broken file:

```python
print("this line is fine")
print("this line is broken)
```

You'll see something like:

```
  File "hello.py", line 2
    print("this line is broken)
          ^
SyntaxError: unterminated string literal (detected at line 2)
```

Read it **bottom-up**:

1. `SyntaxError` — the *type* of problem. Syntax = grammar. You wrote something
   that isn't valid Python.
2. `unterminated string literal` — the *specific* problem: a string was opened
   with `"` and never closed.
3. `line 2` and the `^` marker — *where*.

Three questions answered: what kind, what exactly, where. Almost every Python
error gives you all three. **Always read the last line first** — that's the
actual message; everything above it is the trail of how it got there.

There is a chapter later ([errors decoded](../reference/errors_decoded.md))
listing every error you'll hit in this project and what it really means.

---

## 1.5 Comments

Anything after a `#` is ignored by Python. It's a note to humans.

```python
# this line does nothing at all
print("but this one runs")   # notes can go on the end of a line too
```

Use comments to explain **why**, not **what**. This is useless:

```python
x = x + 1   # add one to x
```

This is worth writing:

```python
x = x + 1   # advance to next frame; the animation clock is frame-based
```

---

## 1.6 The two ways to run Python

**Script mode** (what you just did): write a file, run the whole thing.

**Interactive mode**: type `python` on its own in the terminal and press Enter.
You get `>>>` and can type single lines that run immediately:

```
>>> 2 + 2
4
>>> print("hi")
hi
>>> exit()
```

Interactive mode is brilliant for testing one small thing: "what does this
function actually return?" Use it constantly. Real physicists use it all day.

---

## Exercises

Create `ch01_exercises.py` and solve these. Answers in
`solutions/ch01_solutions.py` — genuinely try first.

1. Print your name, then on a separate line print the year.
2. Make Python print exactly this, quote marks included: `He said "quantum"`.
   (Hint: there are two kinds of quote mark in Python.)
3. Print the result of `7 / 2`, then `7 // 2`, then `7 % 2`. Work out from the
   output what `//` and `%` do.
4. **Break it:** write a working `print` line, then delete just the closing
   bracket. Run it. Read the error. What line number does Python blame, and why
   might that be different from where you deleted the bracket?
5. In interactive mode, type `2 ** 10`. What operation is `**`?

---

## What you now know

- The interpreter, your script and your editor are three different things.
- `print()` displays things; brackets call a function; quotes make a string.
- Errors state kind, detail, and location — read the last line first.
- `#` makes a comment; interactive mode is for quick experiments.

Next: [Chapter 2 — Variables, numbers and types](02_variables_and_types.md)
