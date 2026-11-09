import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle

Np = 200
s  = 0.5
L  = 50
m  = 1.0
M  = 25.0
R  = 5.0

x = np.random.uniform(-L, L, Np)
y = np.random.uniform(-L, L, Np)
bx, by  = 0.0, 0.0
bvx, bvy = 0.0, 0.0


fig, (ax, ax_msd) = plt.subplots(1, 2, figsize=(11, 5.2),
                                 gridspec_kw={'width_ratios': [1.15, 1]})
msd_t, msd_v = [], []
msd_line, = ax_msd.plot([], [], 'b')
ax_msd.set_xlabel('time (frames)')
ax_msd.set_ylabel('$|R(t)-R(0)|^2$')
ax_msd.set_title('squared displacement of large particle (live)')
dots, = ax.plot(x, y, 'b.', ms=3)
big = Circle((bx, by), R, fill=False, color='r', lw=2)
ax.add_patch(big)
ax.set_xlim(-L, L); ax.set_ylim(-L, L)
ax.set_aspect('equal')

trail_x, trail_y = [], []
trail, = ax.plot([], [], 'r-', lw=0.8)
ax.plot(0, 0, 'go', ms=3, label='Start')
ax.legend(loc='upper right')


def update(frame):
    global x, y, bx, by, bvx, bvy


    angles = np.random.uniform(0, 2*np.pi, Np)
    x = x + s*np.cos(angles)
    y = y + s*np.sin(angles)


    x = np.clip(x, -L, L)
    y = np.clip(y, -L, L)


    dist = np.sqrt((x - bx)**2 + (y - by)**2)
    hit = dist < R


    if np.any(hit):
        ux = (x[hit] - bx) / dist[hit]
        uy = (y[hit] - by) / dist[hit]
        bvx = bvx - (m/M) * s * np.sum(ux)
        bvy = bvy - (m/M) * s * np.sum(uy)
        x[hit] = bx + R*ux
        y[hit] = by + R*uy


    bvx = 0.97 * bvx
    bvy = 0.97 * bvy
    bx = bx + bvx
    by = by + bvy
    bx = np.clip(bx, -L+R, L-R)
    by = np.clip(by, -L+R, L-R)

    trail_x.append(bx)
    trail_y.append(by)
    trail.set_data(trail_x, trail_y)
    ax.set_title(f'Brownian motion: frame {frame}')


    msd_t.append(frame)
    msd_v.append(bx**2 + by**2)
    msd_line.set_data(msd_t, msd_v)
    ax_msd.relim(); ax_msd.autoscale_view()

    dots.set_data(x, y)
    big.center = (bx, by)
    return dots, big, trail, msd_line


anim = FuncAnimation(fig, update, frames=300, interval=30)
plt.show()
