"""
Solutions: Chapters 6-8 (numpy, matplotlib, randomness)
Figures are shown at the end; close each window to continue.
"""
import numpy as np
import matplotlib.pyplot as plt
import time

print("=" * 60)
print("CHAPTER 6 - numpy")
print("=" * 60)

# 6.1
a = np.linspace(0, 2*np.pi, 9)
print("sin values:", np.round(np.sin(a), 20)[:5])
print("sin(pi) =", np.sin(np.pi))
print("-> NOT exactly zero: pi itself is stored approximately (Ch2 2.4)\n")

# 6.2
angles = np.random.uniform(0, 2*np.pi, 1000)
dx, dy = 2*np.cos(angles), 2*np.sin(angles)
x = np.concatenate(([0], np.cumsum(dx)))
y = np.concatenate(([0], np.cumsum(dy)))
print(f"final position = ({x[-1]:.2f}, {y[-1]:.2f})")
print(f"distance = {np.sqrt(x[-1]**2 + y[-1]**2):.2f}   (typical: s*sqrt(N) = "
      f"{2*np.sqrt(1000):.1f})\n")

# 6.3
d = np.array([3.0, 7.0, 1.0, 9.0, 5.0])
mask = d < 6
print("values below 6:", d[mask], " count:", np.sum(mask))
d[mask] = 0
print("after zeroing:", d, "\n")

# 6.4
grid = np.zeros((4, 6))
for i in range(4):
    for j in range(6):
        grid[i, j] = i*j
print("row means (axis=1):", np.mean(grid, axis=1))
print("col means (axis=0):", np.mean(grid, axis=0), "\n")

# 6.5
b = np.array([5, 2, 9, 4])
print(f"np.max = {np.max(b)} (the VALUE), np.argmax = {np.argmax(b)} "
      f"(the POSITION)\n")

# 6.6
xs = 1e-12
print(f"exp(x)-1 = {np.exp(xs)-1:.20e}")
print(f"expm1(x) = {np.expm1(xs):.20e}")
print("expm1 is right. exp(x) is ~1.000000000001; subtracting 1 destroys")
print("almost all significant figures. Matters for Planck at long lambda.\n")

# 6.7  speed test
n = 2_000_000
arr = np.random.uniform(0, 1, n)
t0 = time.time()
total = 0.0
for v in arr:
    total += v*2
t1 = time.time()
t2 = time.time()
total2 = np.sum(arr*2)
t3 = time.time()
print(f"loop {t1-t0:.3f}s  numpy {t3-t2:.4f}s  speedup {(t1-t0)/(t3-t2):.0f}x\n")


print("=" * 60)
print("CHAPTER 8 - Randomness")
print("=" * 60)

rng = np.random.default_rng(42)

# 8.1
u = rng.uniform(0, 1, 10000)
print(f"mean {np.mean(u):.4f} (theory 0.5), sd {np.std(u):.4f} "
      f"(theory {1/np.sqrt(12):.4f})\n")

# 8.2
for n_flips in [10, 1000, 100000]:
    flips = rng.integers(0, 2, n_flips)
    print(f"{n_flips:>6} flips: heads fraction = {np.mean(flips):.4f}")
print("-> deviation from 0.5 shrinks as 1/sqrt(N)\n")

def random_walk(N, s=1.0, gen=rng):
    ang = gen.uniform(0, 2*np.pi, N)
    x = np.concatenate(([0], np.cumsum(s*np.cos(ang))))
    y = np.concatenate(([0], np.cumsum(s*np.sin(ang))))
    return x, y

# 8.3
N = 400
dists = np.array([np.hypot(*[arr[-1] for arr in random_walk(N)])
                  for _ in range(2000)])
mean_d, rms_d = np.mean(dists), np.sqrt(np.mean(dists**2))
print(f"mean {mean_d:.2f}, rms {rms_d:.2f}, ratio {mean_d/rms_d:.4f} "
      f"(theory {np.sqrt(np.pi)/2:.4f})")
print("They differ because squaring weights large excursions more heavily.\n")

# 8.4
print("1/sqrt(N) law (100-step walk, true RMS = 10):")
for trials in [10, 100, 1000, 10000]:
    d2 = [random_walk(100)[0][-1]**2 + random_walk(100)[1][-1]**2
          for _ in range(trials)]
    est = np.sqrt(np.mean(d2))
    print(f"  {trials:>6} trials: RMS = {est:6.3f}, deviation = {abs(est-10):.3f}")
print()

# 8.5  rejection sampling for pi
pts = rng.uniform(-1, 1, (100000, 2))
inside = np.sum(pts[:, 0]**2 + pts[:, 1]**2 < 1)
frac = inside/100000
print(f"fraction inside circle = {frac:.4f}, 4x = {4*frac:.4f} (pi = {np.pi:.4f})")
print("The circle's area is pi, the square's is 4, so the ratio is pi/4.\n")

# 8.6  the reset bug
print("Reset bug demo: if state isn't reset between runs, each run continues")
print("the previous one, so MSD keeps climbing and the runs aren't independent.")

# Figures for chapter 7 exercises
xx = np.linspace(0, 4*np.pi, 400)
plt.figure(figsize=(8, 4))
plt.plot(xx, np.sin(xx), label='sin(x)')
plt.plot(xx, np.cos(xx), label='cos(x)')
plt.xlabel('x (rad)'); plt.ylabel('value')
plt.title('Ch7 Ex1: sine and cosine')
plt.legend(); plt.grid(alpha=0.3)

fig, axes = plt.subplots(2, 2, figsize=(8, 6))
for ax, p in zip(axes.flat, [1, 2, 3, 4]):
    t = np.linspace(0, 2, 100)
    ax.plot(t, t**p)
    ax.set_title(f'y = x^{p}')
plt.tight_layout()

plt.figure(figsize=(8, 5))
plt.hist(dists, bins=40, density=True, alpha=0.7, label='simulation')
Rr = np.linspace(0, dists.max(), 300)
sig2 = N/2
plt.plot(Rr, (Rr/sig2)*np.exp(-Rr**2/(2*sig2)), 'r', lw=2, label='Rayleigh')
plt.xlabel('final displacement'); plt.ylabel('probability density')
plt.title('Ch8 Ex3: displacement distribution')
plt.legend()

plt.show()
