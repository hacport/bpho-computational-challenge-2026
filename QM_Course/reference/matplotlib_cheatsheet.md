# matplotlib cheat sheet

## Basic figure

```python
import matplotlib.pyplot as plt

plt.figure(figsize=(9, 5))
plt.plot(x, y, lw=0.8, color='red', label='data')
plt.xlabel('wavelength (nm)')
plt.ylabel('intensity')
plt.title('What this figure shows')
plt.legend()
plt.grid(alpha=0.3)
plt.show()               # LAST line; pauses until closed
```

## Format shorthand

```
colours   b g r c m y k w
markers   . o s x + v ^ D
lines     -  --  -.  :
'ro'      red circles
'k--'     black dashed
'b.'      small blue dots
```

Keywords: `lw` (line width), `ms` (marker size), `alpha` (transparency),
`color`, `ls`, `label`, `zorder` (draw order).

## Reference lines and regions

```python
plt.axhline(24.9, color='k', ls='--')
plt.axvline(656.3, color='r')
plt.axvspan(380, 700, color='yellow', alpha=0.15)
plt.axhspan(0, 1, color='grey', alpha=0.1)
```

## Axes control

```python
plt.xlim(0, 3000)      plt.ylim(0, 5e13)
plt.xscale('log')      plt.yscale('log')
plt.axis('equal')                        # equal unit scaling
plt.gca().set_aspect('equal', adjustable='datalim')
plt.xticks([]);  plt.yticks([])           # hide ticks
```

## Text

```python
plt.text(x, y, 'note', fontsize=9, ha='center')
plt.annotate('0.38 eV', (n, E), textcoords='offset points', xytext=(8, -3))
plt.annotate('', xy=(x2,y2), xytext=(x1,y1), arrowprops=dict(color='g', width=2))
```

LaTeX in labels: `'$\\lambda_{max}$'`, `'$\\Delta x\\,\\Delta p/\\hbar$'`

## Subplots

```python
fig, ax = plt.subplots()
fig, axes = plt.subplots(1, 3, figsize=(13, 4.4))
fig, axes = plt.subplots(3, 3, figsize=(11, 11))
for ax in axes.flat: ...
fig, (a1, a2) = plt.subplots(1, 2, gridspec_kw={'width_ratios': [1.15, 1]})
fig.suptitle('Overall title')
plt.tight_layout()
```

`ax.` versions: `set_xlabel`, `set_title`, `set_xlim`, `set_aspect`, `set_xticks`.

## Custom layout (for apps)

```python
fig = plt.figure(figsize=(11, 6))
ax = fig.add_axes([left, bottom, width, height])   # fractions 0-1
fig.text(0.03, 0.9, 'label', fontsize=9)
```

## Artists — keep the handle, move it later

```python
line, = ax.plot(x, y)
line.set_data(newx, newy)
line.set_ydata(newy)
line.set_color('red')

from matplotlib.patches import Circle, Rectangle, Polygon, FancyBboxPatch
c = Circle((0, 0), R, fill=False, color='r', lw=2)
ax.add_patch(c)
c.center = (bx, by)
```

Patches use **data** coordinates; markers use **screen points**.

## 2D data

```python
plt.pcolormesh(X, Y, Z, cmap='inferno', vmin=0, vmax=1)
plt.imshow(Z, cmap='viridis', origin='lower', extent=[x0,x1,y0,y1])
plt.colorbar(label='density')
norm=plt.matplotlib.colors.PowerNorm(0.4)      # compress dynamic range
norm=plt.matplotlib.colors.LogNorm()
```

Colormaps: `viridis` (default, safe), `inferno`/`magma` (densities),
`coolwarm` (diverging), avoid `jet`.

## Histograms

```python
plt.hist(values, bins=40, density=True, alpha=0.7, label='simulation')
```

`density=True` normalises the area to 1 — required to compare with a theory
curve.

## 3D

```python
ax = fig.add_subplot(1, 2, 1, projection='3d')
ax.scatter(x, y, z, s=1, alpha=0.25, c=z, cmap='coolwarm')
ax.set_xlim(...); ax.set_ylim(...); ax.set_zlim(...)
```

## Animation

```python
from matplotlib.animation import FuncAnimation

def update(frame):
    global state
    ...
    artist.set_data(...)
    return artist,

anim = FuncAnimation(fig, update, frames=300, interval=30)   # KEEP the handle
anim.save('out.gif', writer='pillow', fps=30)                # slow; before show
plt.show()
```

`blit=True` is faster but conflicts with changing titles.

## Widgets

```python
from matplotlib.widgets import Slider, Button, RadioButtons

s = Slider(ax_s, 'label', vmin, vmax, valinit=1.0, valstep=0.1)
s.val    s.reset()    s.set_val(x)    s.valtext.set_visible(False)
s.on_changed(callback)

b = Button(ax_b, 'Go');            b.on_clicked(callback)
r = RadioButtons(ax_r, ['a','b']); r.on_clicked(callback);  r.value_selected

fig.canvas.draw_idle()
```

Pass the function, don't call it: `on_changed(update)` not `update()`.

## Saving

```python
plt.savefig('fig.png', dpi=300, bbox_inches='tight')     # before show()
```

## Figure checklist

- [ ] axis labels with units
- [ ] legend where needed
- [ ] title stating the finding
- [ ] sensible limits
- [ ] equal aspect if axes share dimensions
- [ ] theory/limit reference lines
