# Chapter 19 — Widgets: sliders, buttons and callbacks

**Goal:** turn a static figure into an instrument. This chapter explains the
event-driven pattern behind every interactive app in the project.

---

## 19.1 The mental shift: event-driven programming

Everything so far has been a **script**: start at the top, run to the bottom,
finish. Interactive programs work differently.

```
build the interface
    ↓
wait for the user to do something  ←─────┐
    ↓                                     │
run the function attached to that thing ──┘
```

The program spends almost all its time *waiting*. Your code no longer controls
the order of events — the user does. You write small functions ("callbacks") and
register them: "when this slider moves, call this function."

`plt.show()` is what starts the waiting loop. That's why nothing after it runs
until the window closes.

---

## 19.2 The minimal slider

```python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

x = np.linspace(0, 10, 500)

fig, ax = plt.subplots()
fig.subplots_adjust(bottom=0.25)          # make room underneath
line, = ax.plot(x, np.sin(x))             # keep the handle!

ax_freq = fig.add_axes([0.2, 0.1, 0.6, 0.03])
s_freq = Slider(ax_freq, 'frequency', 0.1, 5.0, valinit=1.0)

def update(val):
    line.set_ydata(np.sin(s_freq.val * x))
    fig.canvas.draw_idle()

s_freq.on_changed(update)
plt.show()
```

Type this and play with it. Then note the five essential moves:

1. **`fig.add_axes([left, bottom, width, height])`** — a slider needs its own
   little axes to live in. Coordinates are fractions of the figure (0 to 1).
2. **`Slider(ax, label, min, max, valinit=...)`** — creates it.
3. **Keep the artist handle** (`line,`) so you can update it (§7.6).
4. **The callback** reads `.val`, recomputes, updates the artist.
5. **`on_changed(update)`** registers it. Note: no brackets after `update` — you
   are passing the *function itself*, not calling it. `on_changed(update())`
   would call it once and register the result. This is a classic beginner bug.

`draw_idle()` asks matplotlib to refresh when convenient — smoother than forcing
an immediate redraw.

---

## 19.3 The three widgets used in this project

### Slider

```python
s_lam = Slider(ax_lam, 'wavelength (nm)', 160, 800, valinit=400,
               valstep=5, color='#0969da')
s_lam.val            # current value
s_lam.reset()        # back to valinit
s_lam.set_val(2.5)   # set programmatically
s_lam.valtext.set_visible(False)    # hide the built-in number display
```

`valstep` forces discrete steps — useful for integers like quantum numbers.
Hiding `valtext` is what let the app show values in its own styled boxes instead.

### RadioButtons

```python
from matplotlib.widgets import RadioButtons
r_metal = RadioButtons(ax_metal, ['Sodium', 'Caesium', 'Zinc'],
                       activecolor='#0969da')
r_metal.value_selected            # the current label, a string
r_metal.on_clicked(on_metal)      # callback receives the label
r_metal.set_active(1)             # select by index
```

Radio buttons are for **mutually exclusive** choices — exactly right for "which
metal is the cathode".

### Button

```python
from matplotlib.widgets import Button
b_pause = Button(ax_pause, 'Pause', color='#0969da', hovercolor='#0a5cc2')
b_pause.on_clicked(on_pause)
b_pause.label.set_text('Resume')      # change its text later
```

---

## 19.4 The callback pattern that scales

For anything with more than one control, don't write one callback per widget.
Write **one redraw function** and attach it to everything:

```python
def draw(_=None):
    th = np.radians(s_th.val)          # 1. read all controls
    ph = np.radians(s_ph.val)
    pc = classical_mismatch(th, ph)    # 2. compute the physics
    pq = quantum_mismatch(th, ph)
    ax_bars.clear()                    # 3. redraw the panels
    ax_bars.bar(['classical', 'quantum'], [pc, pq])
    fig.canvas.draw_idle()             # 4. refresh

s_th.on_changed(draw)
s_ph.on_changed(draw)
draw()                                 # draw once at startup
```

Why `_=None`? matplotlib passes the new value to the callback, but we don't need
it (we read `.val` directly). The underscore is the conventional name for "an
argument I'm ignoring", and the default lets you also call `draw()` with no
arguments at startup.

**Unit conversion belongs at the top of the callback.** Sliders are in degrees,
nanometres, kilovolts — whatever the user thinks in. Physics is in radians,
metres, volts. Convert once, immediately, then never think about it again.

### clear-and-redraw vs update-in-place

Two strategies:

```python
ax.clear(); ax.plot(...)      # simple, slower - fine for slider interaction
line.set_ydata(new_y)         # fast - required for animation
```

Sliders move at human speed; a full clear-and-redraw is fine and much easier to
write. Animations run at 30 fps and *must* update in place.

---

## 19.5 Combining widgets with animation

The photoelectric app does both: a `FuncAnimation` runs continuously while
sliders change parameters. The trick is that the animation reads the widget
values every frame:

```python
def update(frame):
    if state['paused']:
        return photons, electrons        # do nothing while paused
    W, E_ph, KE = physics()              # reads s_lam.val, r_metal.value_selected
    ...
```

Two useful patterns visible there:

**A state dictionary** instead of many globals:

```python
state = {'paused': False, 'frame': 0}
def on_pause(_):
    state['paused'] = not state['paused']
```

Because you're *modifying* the dictionary rather than rebinding the name, no
`global` is needed. Cleaner, and it scales to a dozen state variables.

**A separate `refresh_static()`** for things that only change when a control
moves (labels, colours, readouts), keeping the per-frame `update()` lean. Don't
recompute what hasn't changed 30 times a second.

---

## 19.6 Layout without pain

Sketch on paper first, in fractions of the window. The photoelectric app's plan:

```
0.0            0.28                                      1.0
 ┌──────────────┬────────────────────────────────────────┐ 1.0
 │  Controls    │                                        │
 │  (radio)     │        the vacuum chamber              │
 │  (sliders)   │        (main axes)                     │
 │  (buttons)   │                                        │
 │  (tip box)   │                                        │
 └──────────────┴────────────────────────────────────────┘ 0.0
```

Then translate to `add_axes` calls. Rules of thumb:

- Sliders: height ≈ 0.03, width 0.15–0.6
- Leave ≥0.06 vertical gap between stacked sliders or labels collide
- `fig.text(x, y, ...)` places free-floating labels anywhere
- Group related controls visually; put the thing being controlled next to them

For readouts styled like a real instrument:

```python
fig.text(0.225, 0.775, '2.28 eV', fontsize=8, ha='right', weight='bold',
         bbox=dict(boxstyle='round,pad=0.25', fc='white', ec='#d0d7de'))
```

`bbox` draws a rounded box behind the text — that's how the app's value chips are
made.

---

## 19.7 When to use something other than matplotlib

Matplotlib widgets are perfect for one-screen physics instruments: no extra
install, and the plot *is* the app. But if you ever need many windows, menus,
text entry or tabs, use a real GUI toolkit — `tkinter` (built in, next chapter),
or `PyQt` for professional desktop software.

For this project the split works out neatly: matplotlib for the instruments,
tkinter for the launcher that opens them.

---

## Exercises

1. Build the sine slider from §19.2 and add a second slider for amplitude.
2. Add a `Button` labelled "Reset" that returns both sliders to their initial
   values.
3. Add `RadioButtons` to switch between sine, cosine and a damped sine.
4. Make a "particle in a box" explorer: sliders for n (1–10, `valstep=1`) and box
   width, showing |ψ|² and printing the energy in the title. You have all the
   physics from Chapter 15.
5. **Break it:** register a callback as `on_changed(update())` with brackets. What
   happens, and what does the error tell you?
6. Build a Planck explorer: one temperature slider, the spectrum, a marker at the
   Wien peak, and a swatch showing the CIE glow colour (Chapter 21).

Solutions: `solutions/ch19_solutions.py`

---

## What you now know

- Event-driven programming: build, wait, respond.
- Slider, RadioButtons, Button — creation, properties, callbacks.
- Pass the function, don't call it: `on_changed(update)`.
- One redraw function for all controls; convert units at the top.
- Clear-and-redraw for sliders, update-in-place for animation.
- State dictionaries instead of scattered globals; separating static refresh from
  the animation loop.
- Layout in figure fractions, sketched before it's coded.

Next: [Chapter 20 — The tkinter launcher](20_tkinter_launcher.md)
