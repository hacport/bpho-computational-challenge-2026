import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from task10_hydrogenic_orbitals import psi

fig = plt.figure(figsize=(12, 6.5))
fig.suptitle('LCAO extension: molecular orbitals of H$_2^+$ '
             '$\\;\\psi_\\pm = \\psi_{1s}(r_1) \\pm \\psi_{1s}(r_2)$')

ax_bond = fig.add_axes([0.05, 0.32, 0.28, 0.55])
ax_anti = fig.add_axes([0.36, 0.32, 0.28, 0.55])
ax_line = fig.add_axes([0.72, 0.32, 0.26, 0.55])
ax_slider = fig.add_axes([0.25, 0.12, 0.5, 0.04])

s_R = Slider(ax_slider, 'internuclear distance R ($a_0$)', 0.5, 8, valinit=2.0)

ext = 8
g = np.linspace(-ext, ext, 300)
X, Z = np.meshgrid(g, g)

def draw(_=None):
    R = s_R.val
    p1 = psi(1, 0, 0, X, 0*X, Z - R/2)
    p2 = psi(1, 0, 0, X, 0*X, Z + R/2)
    norm_p = 1/np.sqrt(2 + 2*np.exp(-R)*(1 + R + R**2/3))
    norm_m = 1/np.sqrt(2 - 2*np.exp(-R)*(1 + R + R**2/3))
    bond = (norm_p*(p1 + p2))**2
    anti = (norm_m*(p1 - p2))**2

    for ax, dens, name in [(ax_bond, bond, 'bonding $\\sigma_g$ (sum)'),
                           (ax_anti, anti, 'antibonding $\\sigma_u^*$ (difference)')]:
        ax.clear()
        ax.pcolormesh(X, Z, dens, cmap='inferno',
                      norm=plt.matplotlib.colors.PowerNorm(0.5))
        ax.plot([0, 0], [R/2, -R/2], 'w+', ms=10)
        ax.set_title(name, fontsize=10)
        ax.set_aspect('equal')
        ax.set_xticks([]); ax.set_yticks([])

    ax_line.clear()
    zline = np.linspace(-ext, ext, 500)
    zero = np.zeros_like(zline)
    b = (norm_p*(psi(1, 0, 0, zero, zero, zline - R/2)
                 + psi(1, 0, 0, zero, zero, zline + R/2)))**2
    a = (norm_m*(psi(1, 0, 0, zero, zero, zline - R/2)
                 - psi(1, 0, 0, zero, zero, zline + R/2)))**2
    ax_line.plot(zline, b, 'c', label='bonding')
    ax_line.plot(zline, a, 'm', label='antibonding')
    ax_line.axvline(R/2, color='w', ls=':', lw=0.7)
    ax_line.axvline(-R/2, color='w', ls=':', lw=0.7)
    ax_line.set_facecolor('black')
    ax_line.set_xlabel('z along bond axis ($a_0$)')
    ax_line.set_title('density along the bond:\nbonding piles charge '
                      'BETWEEN nuclei', fontsize=9)
    ax_line.legend(fontsize=8)
    fig.canvas.draw_idle()

s_R.on_changed(draw)
draw()
plt.show()
