import numpy as np
import matplotlib.pyplot as plt

Np, s, L, m, M, R = 200, 0.5, 50, 1.0, 25.0, 5.0
drag = 0.97
frames, runs = 2000, 30


d2 = np.zeros((runs, frames))

for run in range(runs):

    x = np.random.uniform(-L, L, Np)
    y = np.random.uniform(-L, L, Np)
    bx, by  = 0.0, 0.0
    bvx, bvy = 0.0, 0.0
    for t in range(frames):

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

        bvx = drag * bvx
        bvy = drag * bvy
        bx = bx + bvx
        by = by + bvy
        bx = np.clip(bx, -L+R, L-R)
        by = np.clip(by, -L+R, L-R)

        d2[run, t] = bx**2 + by**2

msd = np.mean(d2, axis=0)

plt.plot(msd, label='simulation')
plt.xlabel('time (frames)'); plt.ylabel('mean squared displacement')
plt.title(f'Einstein diffusion: MSD vs time ({runs} runs)')
plt.legend()
plt.show()
