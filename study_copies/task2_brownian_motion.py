import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle  

Np = 200          # how many gas molecules
s  = 0.5           # how far a molecule moves each frame ("speed")
L  = 50           # box goes from -L to +L
m  = 1.0          # molecule mass
M  = 25.0         # big particle mass (25x heavier — tuned so kicks are visible)
R  = 5.0          # big particle radius

x = np.random.uniform(-L, L, Np)     # 200 random start positions
y = np.random.uniform(-L, L, Np)
bx, by  = 0.0, 0.0                   # big particle at centre...
bvx, bvy = 0.0, 0.0                  # ...not moving yet


fig, ax = plt.subplots()
dots, = ax.plot(x, y, 'b.', ms=3)    # the molecules (blue dots)
big = Circle((bx, by), R, fill=False, color='r', lw=2)
ax.add_patch(big)
ax.set_xlim(-L, L); ax.set_ylim(-L, L)
ax.set_aspect('equal')

trail_x, trail_y = [], []                     # plain Python lists
trail, = ax.plot([], [], 'r-', lw=0.8)        # empty red line for now
ax.plot(0, 0, 'go', ms=3, label='Start')      # green dot: big particle's origin
ax.legend(loc='upper right')

# ============ ZONE 2: ONE TICK OF TIME ============
def update(frame):
    global x, y, bx, by, bvx, bvy

    # 1. every molecule takes one random step
    angles = np.random.uniform(0, 2*np.pi, Np)
    x = x + s*np.cos(angles)
    y = y + s*np.sin(angles)
    
    # walls: keep molecules inside the box
    x = np.clip(x, -L, L)      # clip = anything past the wall gets put ON the wall
    y = np.clip(y, -L, L)
    
    # 2. which molecules are touching the big particle?
    dist = np.sqrt((x - bx)**2 + (y - by)**2)
    hit = dist < R

    # 3. collisions: kick the big particle (Newton's 3rd law)
    if np.any(hit):
        ux = (x[hit] - bx) / dist[hit]
        uy = (y[hit] - by) / dist[hit]
        bvx = bvx - (m/M) * s * np.sum(ux)
        bvy = bvy - (m/M) * s * np.sum(uy)
        x[hit] = bx + R*ux               # place hitters back on the rim
        y[hit] = by + R*uy

    # 4. big particle drifts with its velocity
    bvx = 0.97 * bvx      # viscous drag: lose 3% of velocity per frame (tuned)
    bvy = 0.97 * bvy
    bx = bx + bvx
    by = by + bvy
    bx = np.clip(bx, -L+R, L-R)
    by = np.clip(by, -L+R, L-R)
    
    trail_x.append(bx)
    trail_y.append(by)
    trail.set_data(trail_x, trail_y)
    ax.set_title(f'Brownian motion: frame {frame}')

    # 5. redraw everything
    dots.set_data(x, y)
    big.center = (bx, by)
    return dots, big, trail                    # LAST line — nothing after this

# ================= ZONE 3: RUN =================
anim = FuncAnimation(fig, update, frames=300, interval=30)
anim.save('task2_brownian.gif', writer='pillow', fps=30)
plt.show()