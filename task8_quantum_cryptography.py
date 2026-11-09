import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def classical_mismatch(th, ph):
    return 1 - np.cos(th)**2*np.cos(ph)**2 - np.sin(th)**2*np.sin(ph)**2

def quantum_mismatch(th, ph):
    return np.sin(ph - th)**2

fig = plt.figure(figsize=(11, 6))
fig.suptitle('Quantum cryptography: polarization mismatch calculator '
             '(entangled photons, Malus law model)')

ax_arrows = fig.add_axes([0.06, 0.35, 0.36, 0.52])
ax_bars = fig.add_axes([0.52, 0.35, 0.20, 0.52])
ax_curve = fig.add_axes([0.78, 0.35, 0.20, 0.52])
ax_sth = fig.add_axes([0.15, 0.16, 0.6, 0.04])
ax_sph = fig.add_axes([0.15, 0.08, 0.6, 0.04])

s_th = Slider(ax_sth, 'Alice angle $\\theta$ (deg)', 0, 90, valinit=0)
s_ph = Slider(ax_sph, 'Bob angle $\\phi$ (deg)', 0, 90, valinit=30)

ph_sweep = np.linspace(0, np.pi/2, 200)
th_fix = np.pi/4
ax_curve.plot(np.degrees(ph_sweep), quantum_mismatch(th_fix, ph_sweep), 'b',
              label='QM $\\sin^2(\\phi-45°)$')
ax_curve.plot(np.degrees(ph_sweep), classical_mismatch(th_fix, ph_sweep), 'r',
              label='classical (flat 0.5!)')
marker_q, = ax_curve.plot([], [], 'bo', ms=8)
marker_c, = ax_curve.plot([], [], 'ro', ms=8)
ax_curve.set_xlabel('Bob angle $\\phi$ (deg)')
ax_curve.set_title('$\\theta=45°$: QM dips to 0,\nclassical cannot', fontsize=9)
ax_curve.legend(fontsize=6)

def draw(_=None):
    th = np.radians(s_th.val)
    ph = np.radians(s_ph.val)
    pc = classical_mismatch(th, ph)
    pq = quantum_mismatch(th, ph)

    ax_arrows.clear()
    for ang, colour, name in [(th, 'green', 'Alice'), (ph, 'blue', 'Bob')]:
        ax_arrows.annotate('', xy=(np.sin(ang), np.cos(ang)), xytext=(0, 0),
                           arrowprops=dict(color=colour, width=2))
        ax_arrows.annotate('', xy=(np.cos(ang), -np.sin(ang)), xytext=(0, 0),
                           arrowprops=dict(color=colour, width=1, alpha=0.4))
        ax_arrows.text(1.05*np.sin(ang), 1.05*np.cos(ang), f'$Y_{{{name[0]}}}$',
                       color=colour)
    ax_arrows.plot([0, 0], [0, 1.1], 'k--', lw=0.5)
    ax_arrows.set_xlim(-0.2, 1.3); ax_arrows.set_ylim(-0.4, 1.3)
    ax_arrows.set_aspect('equal')
    ax_arrows.set_title('detector orientations (solid Y, faint X)', fontsize=9)

    ax_bars.clear()
    bars = ax_bars.bar(['classical', 'quantum'], [pc, pq], color=['red', 'blue'])
    for bar, val in zip(bars, [pc, pq]):
        ax_bars.text(bar.get_x() + bar.get_width()/2, val + 0.02,
                     f'{val:.3f}', ha='center')
    ax_bars.set_ylim(0, 1.1)
    ax_bars.set_title('P(mismatch)', fontsize=9)

    marker_q.set_data([s_ph.val], [quantum_mismatch(np.pi/4, ph)])
    marker_c.set_data([s_ph.val], [classical_mismatch(np.pi/4, ph)])
    fig.canvas.draw_idle()

s_th.on_changed(draw)
s_ph.on_changed(draw)
draw()

fig2, (axc, axq) = plt.subplots(1, 2, figsize=(11, 4.5))
th_g, ph_g = np.meshgrid(np.linspace(0, np.pi/2, 200),
                         np.linspace(0, np.pi/2, 200))
for ax, Z, name in [(axc, classical_mismatch(th_g, ph_g), 'Classical'),
                    (axq, quantum_mismatch(th_g, ph_g), 'Quantum')]:
    im = ax.pcolormesh(np.degrees(th_g), np.degrees(ph_g), Z,
                       cmap='inferno', vmin=0, vmax=1)
    ax.set_xlabel('$\\theta$ (deg)'); ax.set_ylabel('$\\phi$ (deg)')
    ax.set_title(f'{name} P(mismatch)')
    ax.set_aspect('equal')
fig2.colorbar(im, ax=[axc, axq], label='P(mismatch)')

print('Where classical and quantum predictions split:')
for th_d, ph_d in [(45, 45), (30, 60), (45, 90), (30, 30)]:
    th, ph = np.radians(th_d), np.radians(ph_d)
    print(f'  theta={th_d:>2} deg, phi={ph_d:>2} deg:  '
          f'classical {classical_mismatch(th, ph):.4f},  '
          f'quantum {quantum_mismatch(th, ph):.4f}')
print('\nAligned detectors (theta=phi): QM predicts ZERO mismatch always;')
print('classical cannot - this correlation is the entanglement signature')
print('confirmed by Aspect (1982), Nobel Prize 2022.')

plt.show()
