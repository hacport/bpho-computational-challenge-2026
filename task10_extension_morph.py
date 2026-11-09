import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from task10_hydrogenic_orbitals import psi

n, l = 3, 2
ms = [0, 1, 2]
extent = 6*n
g = np.linspace(-extent, extent, 250)
X, Z = np.meshgrid(g, g)

densities = [psi(n, l, m, X, 0*X, Z)**2 for m in ms]
densities = [d/d.max() for d in densities]

fig, ax = plt.subplots(figsize=(6, 6))
im = ax.imshow(densities[0], cmap='inferno', origin='lower',
               extent=[-extent, extent, -extent, extent],
               norm=plt.matplotlib.colors.PowerNorm(0.5, vmax=1))
ax.set_xlabel('x ($a_0$)'); ax.set_ylabel('z ($a_0$)')

hold, blend = 25, 25
seg = hold + blend

def update(frame):
    k = (frame // seg) % len(ms)
    pos = frame % seg
    d1 = densities[k]
    d2 = densities[(k+1) % len(ms)]
    if pos < hold:
        d = d1
        title = f'n={n}, l={l}, m={ms[k]}'
    else:
        t = (pos - hold) / blend
        w = 0.5 - 0.5*np.cos(np.pi*t)
        d = (1-w)*d1 + w*d2
        title = f'morphing m={ms[k]} $\\to$ m={ms[(k+1) % len(ms)]}'
    im.set_data(d)
    ax.set_title(f'$|\\psi|^2$ morph:  {title}')
    return im,

anim = FuncAnimation(fig, update, frames=3*seg, interval=50)
plt.show()
