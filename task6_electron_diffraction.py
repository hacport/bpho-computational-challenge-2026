import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

h = 6.62607015e-34
e = 1.602176634e-19
me = 9.1093837015e-31

r_tube = 65e-3
d1, d2 = 0.213e-9, 0.123e-9

def ring_radius(V, d):
    lam = h / np.sqrt(2 * me * e * V)
    theta = np.arcsin(lam / (2 * d))
    return r_tube * np.sin(2 * theta)

fig, axes = plt.subplots(1, 3, figsize=(12, 4.2))
for ax, V in zip(axes, [1000, 3000, 5000]):
    for d, colour in [(d1, 'lime'), (d2, 'cyan')]:
        x = ring_radius(V, d)
        ax.add_patch(Circle((0, 0), x*1e3, fill=False, color=colour, lw=2))
    ax.add_patch(Circle((0, 0), 1.5, color='white'))
    ax.set_facecolor('darkgreen')
    ax.set_xlim(-40, 40); ax.set_ylim(-40, 40)
    ax.set_aspect('equal')
    ax.set_title(f'V = {V/1000:.0f} kV')
    ax.set_xlabel('screen position (mm)')
axes[0].set_ylabel('screen position (mm)')
fig.suptitle('Electron diffraction rings on phosphor screen '
             '(inner ring: d=0.213 nm, outer ring: d=0.123 nm)')
plt.tight_layout()

V = np.linspace(1000, 5000, 30)
inv_sqrtV = 1 / np.sqrt(V)

plt.figure(figsize=(8, 5))
print('straight-line check  1/sqrt(V) vs sin(theta):')
for d, name in [(d1, 'd = 0.213 nm'), (d2, 'd = 0.123 nm')]:
    lam = h / np.sqrt(2 * me * e * V)
    sin_theta = lam / (2 * d)
    m_fit, c_fit = np.polyfit(sin_theta, inv_sqrtV, 1)
    d_recovered = m_fit * h / (2 * np.sqrt(2 * me * e))
    plt.plot(sin_theta, inv_sqrtV, 'o', ms=4, label=f'{name}')
    plt.plot(sin_theta, m_fit*sin_theta + c_fit, '-', lw=0.8)
    print(f'  {name}:  gradient = {m_fit:.4f},  intercept = {c_fit:.2e}')
    print(f'  atomic spacing recovered from gradient: {d_recovered*1e9:.3f} nm\n')

plt.xlabel('$\\sin\\theta$')
plt.ylabel('$1/\\sqrt{V}$  (V$^{-1/2}$)')
plt.title('Model check: $1/\\sqrt{V}$ vs $\\sin\\theta$ is a straight line '
          'through the origin')
plt.legend()
plt.show()
