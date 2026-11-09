import numpy as np
import matplotlib.pyplot as plt


def random_walk(N, s):
    angles = np.random.uniform(0, 2*np.pi, N)
    dx = s*np.cos(angles)
    dy = s*np.sin(angles)
    x = np.concatenate(([0], np.cumsum(dx)))
    y = np.concatenate(([0], np.cumsum(dy)))
    return x, y


x, y = random_walk(1000, 1)
plt.figure()
plt.plot(x, y, lw=0.8)
plt.plot(0, 0, 'go', label='Start')
plt.plot(x[-1], y[-1], 'ro', label='End')
plt.title('2D Random Walk: N=1000, s=1')
plt.xlabel('x'); plt.ylabel('y')
plt.legend()
plt.axis('equal')


for N in [100, 400, 900, 1600]:
    d_squared = []
    for trial in range(1000):
        x, y = random_walk(N, 1)
        d_squared.append(x[-1]**2 + y[-1]**2)
    rms = np.sqrt(np.mean(d_squared))
    print(f"N={N}:  RMS = {rms:.2f},  theory = {np.sqrt(N):.1f}")

plt.figure()
for i in range(50):
    x, y = random_walk(1000, 1)
    plt.plot(x, y, lw=0.5)
plt.plot(0, 0, 'ko', label='Common origin')   
plt.title('50 random walks, N=1000, s=1')
plt.xlabel('x'); plt.ylabel('y')
plt.axis('equal')

plt.show()