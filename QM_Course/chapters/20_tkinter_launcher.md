# Chapter 20 — Building the launcher with tkinter

**Goal:** build a real desktop application window — the dark-themed launcher that
ties the whole project together — using only what ships with Python.

---

## 20.1 Why tkinter

`tkinter` is Python's built-in GUI toolkit. It is not the prettiest, but:

- **Zero installation.** It ships with Python. On a deadline, that matters more
  than beauty.
- It makes genuine native windows with buttons, labels and layouts.
- It's enough to build something that looks deliberate and professional if you
  control the colours and spacing yourself.

The alternative, PyQt, is more powerful and much heavier. For a launcher that
opens fourteen scripts, tkinter is the right engineering choice — and being able
to explain *why you chose the simpler tool* is a mark of judgement.

---

## 20.2 The smallest possible window

```python
import tkinter as tk

root = tk.Tk()
root.title('Hello')
root.geometry('400x200')

label = tk.Label(root, text='My first window')
label.pack(pady=20)

root.mainloop()
```

Four concepts:

- **`tk.Tk()`** — creates the main window (conventionally called `root`).
- **Widgets** — `Label`, `Button`, `Frame`, etc. The first argument is always the
  **parent** they live inside.
- **Geometry managers** — `.pack()`, `.grid()` or `.place()` decide where a widget
  goes. A widget you never place is invisible.
- **`root.mainloop()`** — starts the event loop and waits. Like `plt.show()`,
  nothing after it runs until the window closes.

---

## 20.3 The three geometry managers

**`pack()`** — stack things in order:

```python
widget.pack(side='left', fill='x', expand=True, padx=10, pady=5)
```

Simple; ideal for headers and vertical stacks.

**`grid()`** — rows and columns:

```python
card.grid(row=2, column=1, sticky='nsew', padx=6, pady=5)
frame.grid_columnconfigure(0, weight=1)
```

`sticky='nsew'` makes the widget expand to fill its cell (north/south/east/west).
`grid_columnconfigure(..., weight=1)` lets a column grow when the window is
resized. This is how the launcher's two-column card layout works.

**`place()`** — exact pixel positions. Avoid; it breaks on resize.

**Never mix pack and grid inside the same parent** — tkinter will hang. (Different
parents can use different managers, which is why the launcher packs frames and
grids the cards inside them.)

---

## 20.4 Styling: making tkinter look intentional

Default tkinter looks like 1995. The fix is a consistent palette and generous
spacing:

```python
BG, CARD, FG, ACCENT = '#0d1117', '#161b22', '#e6edf3', '#58a6ff'

root.configure(bg=BG)
tk.Label(root, text='ψ  QUANTUM MECHANICS', bg=BG, fg=ACCENT,
         font=('Segoe UI', 22, 'bold')).pack(pady=(18, 0))
```

Practical rules:

- **Set `bg` on every widget.** Any widget you forget shows up as a grey patch.
- **Two or three colours only** — background, card, accent — plus a muted grey
  for secondary text (`#8b949e`).
- **Font tuples** `(family, size, style)`; 'Segoe UI' on Windows, 'Helvetica'
  cross-platform.
- **`pady=(18, 0)`** — a tuple gives different padding above and below.
- Borders via `highlightbackground` and `highlightthickness` on a Frame.

Those hex colours are GitHub's dark theme, chosen because they're already
carefully balanced. Borrowing a professional palette is legitimate design.

---

## 20.5 Building the cards

Each module is a `Frame` containing a number badge and two labels:

```python
for i, (num, name, script, desc) in enumerate(TASKS):
    card = tk.Frame(frame, bg=CARD, highlightbackground='#30363d',
                    highlightthickness=1)
    card.grid(row=i // 2, column=i % 2, sticky='nsew', padx=6, pady=5)
    frame.grid_columnconfigure(i % 2, weight=1)

    btn = tk.Label(card, text=f'  {num}  ', bg=ACCENT, fg=BG,
                   font=('Segoe UI', 13, 'bold'))
    btn.pack(side='left', padx=10, pady=10)

    body = tk.Frame(card, bg=CARD)
    body.pack(side='left', fill='x', expand=True, pady=6)
    tk.Label(body, text=name, bg=CARD, fg=FG, anchor='w',
             font=('Segoe UI', 11, 'bold')).pack(fill='x')
    tk.Label(body, text=desc, bg=CARD, fg='#8b949e', anchor='w',
             wraplength=290, justify='left', font=('Segoe UI', 8)).pack(fill='x')
```

The two-column trick: `row = i // 2, column = i % 2` (§2.3). Integer division
gives the row, modulo gives the column. Item 0 → (0,0), item 1 → (0,1), item 2 →
(1,0)… Elegant, and a nice demonstration that those operators earn their keep.

`wraplength=290` wraps description text at 290 pixels; `anchor='w'` left-aligns.

---

## 20.6 Making the whole card clickable

A `Label` has no click behaviour, so bind one:

```python
def launch(script, name):
    subprocess.Popen([sys.executable, os.path.join(HERE, script)], cwd=HERE)
    status.set(f'running: {name}   (close its window to return)')

for w in (card, btn, body) + tuple(body.winfo_children()):
    w.bind('<Button-1>', lambda e, s=script, n=name: launch(s, n))
```

Three things worth understanding here:

**`bind('<Button-1>', func)`** attaches a handler to left-click. Other events:
`<Button-3>` right-click, `<Enter>`/`<Leave>` hover, `<Key>` keypress.

**Every child must be bound**, or clicking the text does nothing while clicking
the card works. `winfo_children()` lists a widget's children so you can bind them
all in one loop.

**`lambda e, s=script, n=name:`** — the crucial subtlety. A `lambda` is a small
inline function; `e` is the event object tkinter passes. The **default arguments
`s=script, n=name` capture the current values** at the moment the lambda is
created. Without them, all fourteen cards would end up launching the *last*
script, because the lambda would look up `script` when clicked — by which time
the loop has finished and it holds its final value.

This is the "late binding closure" trap, and it catches experienced programmers.
The default-argument trick is the standard fix.

---

## 20.7 Launching other programs

```python
import subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
subprocess.Popen([sys.executable, os.path.join(HERE, script)], cwd=HERE)
```

- **`sys.executable`** is the path to the Python interpreter currently running —
  guaranteeing the child uses the same Python (and the same installed numpy) as
  the launcher. Hard-coding `"python"` would break on machines with several
  versions.
- **`subprocess.Popen`** starts a program and *returns immediately*, so the
  launcher stays responsive while the task runs. (`subprocess.run` would block
  until it finished.)
- **`os.path.dirname(os.path.abspath(__file__))`** is the folder containing the
  launcher — so it works no matter which directory you start it from.
- **`cwd=HERE`** makes the child run in that folder, so its imports and file
  saves land in the right place.

Because each task runs as a **separate process**, a crash in one cannot take down
the launcher, and several can be open at once. That's a real architectural
advantage, not just convenience.

---

## 20.8 Live status text with StringVar

```python
status = tk.StringVar(value='click any module to launch it')
tk.Label(root, textvariable=status, bg=BG, fg=ACCENT,
         font=('Consolas', 10)).pack(pady=10)
...
status.set('running: Random walk')
```

A `StringVar` is a *watched* string: bind it to a label with `textvariable=` and
any `.set()` updates the display automatically. The tkinter equivalent of
`set_data`.

---

## 20.9 A checklist for a launcher that looks professional

- [ ] Window title states what the program is
- [ ] Sensible fixed starting size (`geometry`)
- [ ] Consistent palette; `bg` set on every widget
- [ ] Clear heading and subheading
- [ ] Each item has a name *and* a one-line description of what it demonstrates
- [ ] Whole card clickable, not just a small button
- [ ] Status line that responds
- [ ] Launches in separate processes so nothing blocks

---

## Exercises

1. Build a three-button window: each button prints a different message.
2. Recreate the card layout with four of your own scripts.
3. Add hover highlighting: bind `<Enter>` and `<Leave>` to change the card's
   background. (Remember to bind the children too.)
4. **Break it:** remove the `s=script, n=name` defaults from the lambda and click
   several cards. Explain what happens using §20.6.
5. Add a "Run all" button that launches three scripts in sequence.
6. Add a text panel that shows a longer description when a card is hovered.
7. **Stretch:** rebuild the launcher with `tkinter.ttk` themed widgets, or embed
   a matplotlib figure inside a tkinter window using
   `FigureCanvasTkAgg` — that's the bridge to fully custom scientific apps.

Solutions: `solutions/ch20_solutions.py`

---

## What you now know

- tkinter basics: root, widgets, parents, geometry managers, mainloop.
- pack vs grid vs place, and never mixing the first two in one parent.
- Styling with a consistent palette and font tuples.
- `i // 2, i % 2` for a two-column grid.
- Binding events to whole cards, and the late-binding closure trap.
- `subprocess.Popen` with `sys.executable` for robust, non-blocking launching.
- `StringVar` for live-updating text.

Next: [Chapter 21 — Colour science](21_colour_science.md)
