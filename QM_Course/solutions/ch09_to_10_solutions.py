"""
Solutions: Chapters 9-10 (random walks, Brownian motion)
"""
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(7)

def random_walk(N, s=1.0):
    ang = rng.uniform(0, 2*np.pi, N)
    x = np.concatenate(([0], np.cumsum(s*np.cos(ang))))
    y = np.concatenate(([0], np.cumsum(s*np.sin(ang))))
    return x, y

print("=" * 60)
print("CHAPTER 9 - Random walks")
print("=" * 60)

# 9.1 - fewer trials means worse agreement
print("Ex 1: effect of trial count (N=400, true RMS = 20)")
for trials in [100, 1000]:
    d2 = [(lambda p: p[0][-1]**2 + p[1][-1]**2)(random_walk(400))
          for _ in range(trials)]
    print(f"  {trials:>5} trials: RMS = {np.sqrt(np.mean(d2)):.3f}")

# 9.2 - step size scaling
print("\nEx 2: step size s=5 (theory = s*sqrt(N))")
for N in [100, 400]:
    d2 = [(lambda p: p[0][-1]**2 + p[1][-1]**2)(random_walk(N, 5))
          for _ in range(1000)]
    print(f"  N={N}: RMS = {np.sqrt(np.mean(d2)):.2f}, theory = {5*np.sqrt(N):.1f}")

# 9.3 - fit RMS against sqrt(N)
print("\nEx 3: fitting RMS against sqrt(N)")
Ns = np.array([100, 400, 900, 1600, 2500])
rms = []
for N in Ns:
    d2 = [(lambda p: p[0][-1]**2 + p[1][-1]**2)(random_walk(N))
          for _ in range(800)]
    rms.append(np.sqrt(np.mean(d2)))
grad, intc = np.polyfit(np.sqrt(Ns), rms, 1)
print(f"  gradient = {grad:.4f} (theory = s = 1.0), intercept = {intc:.4f}")

# 9.4 - biased walk = drift, i.e. diffusion plus a current
print("\nEx 4: adding a constant to dx produces systematic DRIFT.")
print("  Physically: diffusion in a flowing medium, or a charged particle")
print("  in an electric field. The cloud's centre moves; it no longer")
print("  stays at the origin. Adding a constant to the ANGLE does nothing")
print("  new, because a uniform distribution shifted is still uniform.")

# 9.5 - 3D walk, correct sphere sampling
print("\nEx 5: 3D random walk")
def walk3d(N, s=1.0):
    cos_th = rng.uniform(-1, 1, N)          # correct: cos(theta) uniform
    th = np.arccos(cos_th)
    ph = rng.uniform(0, 2*np.pi, N)
    x = np.cumsum(s*np.sin(th)*np.cos(ph))
    y = np.cumsum(s*np.sin(th)*np.sin(ph))
    z = np.cumsum(s*np.cos(th))
    return x, y, z

for N in [100, 900]:
    d2 = []
    for _ in range(1000):
        x, y, z = walk3d(N)
        d2.append(x[-1]**2 + y[-1]**2 + z[-1]**2)
    print(f"  N={N}: RMS = {np.sqrt(np.mean(d2)):.2f}, theory = {np.sqrt(N):.1f}")
print("  The law is dimension-independent: <R^2> = N s^2 in any dimension.")

print("\n" + "=" * 60)
print("CHAPTER 10 - Brownian motion")
print("=" * 60)

Np, s, L, m, M, R = 200, 0.5, 50, 1.0, 25.0, 5.0

def run_brownian(frames, drag, M_val=M, s_val=s, record=True):
    """Headless Brownian run. Returns array of squared displacements."""
    x = rng.uniform(-L, L, Np)
    y = rng.uniform(-L, L, Np)
    bx = by = bvx = bvy = 0.0
    out = np.zeros(frames)
    for t in range(frames):
        ang = rng.uniform(0, 2*np.pi, Np)
        x = np.clip(x + s_val*np.cos(ang), -L, L)
        y = np.clip(y + s_val*np.sin(ang), -L, L)
        dist = np.sqrt((x - bx)**2 + (y - by)**2)
        hit = dist < R
        if np.any(hit):
            ux = (x[hit] - bx) / dist[hit]
            uy = (y[hit] - by) / dist[hit]
            bvx -= (m/M_val) * s_val * np.sum(ux)
            bvy -= (m/M_val) * s_val * np.sum(uy)
            x[hit] = bx + R*ux
            y[hit] = by + R*uy
        bvx *= drag
        bvy *= drag
        bx = np.clip(bx + bvx, -L+R, L-R)
        by = np.clip(by + bvy, -L+R, L-R)
        out[t] = bx**2 + by**2
    return out

# 10.1 - no damping
print("Ex 1: drag = 1.0 (no damping)")
d_none = run_brownian(500, 1.0)
d_damp = run_brownian(500, 0.97)
print(f"  final displacement^2 without drag: {d_none[-1]:.1f}")
print(f"  final displacement^2 with drag:    {d_damp[-1]:.1f}")
print("  Without damping the velocity accumulates and never decays, so the")
print("  particle glides ballistically - unphysical for a particle in fluid.")

# 10.2 - heavier particle
print("\nEx 2: M = 200 (8x heavier)")
d_heavy = run_brownian(500, 0.97, M_val=200)
print(f"  displacement^2 with M=25:  {d_damp[-1]:.1f}")
print(f"  displacement^2 with M=200: {d_heavy[-1]:.1f}")
print("  Each kick changes velocity by (m/M)s, so 8x the mass gives 8x")
print("  smaller kicks and roughly 64x smaller squared displacement.")

# 10.4 / 10.5 - MSD gradient gives the diffusion coefficient
print("\nEx 4-5: MSD gradient and diffusion coefficient")
for s_val in [0.3, 0.5, 0.8]:
    runs = 15
    frames = 1500
    d2 = np.zeros((runs, frames))
    for r in range(runs):
        d2[r] = run_brownian(frames, 0.97, s_val=s_val)
    msd = np.mean(d2, axis=0)
    t = np.arange(frames)
    fit_range = slice(200, 1000)          # skip the ballistic start
    grad, _ = np.polyfit(t[fit_range], msd[fit_range], 1)
    print(f"  s={s_val}: MSD gradient = {grad:.4f}, D = grad/4 = {grad/4:.4f}")
print("  s stands in for molecular speed, i.e. TEMPERATURE. Hotter gas")
print("  gives faster diffusion, as Einstein's D = kT/gamma predicts.")

# Figure: MSD curves
plt.figure(figsize=(8, 5))
for s_val, colour in [(0.3, 'b'), (0.5, 'g'), (0.8, 'r')]:
    runs, frames = 15, 1500
    d2 = np.zeros((runs, frames))
    for r in range(runs):
        d2[r] = run_brownian(frames, 0.97, s_val=s_val)
    plt.plot(np.mean(d2, axis=0), colour, label=f's = {s_val}')
plt.xlabel('time (frames)')
plt.ylabel('mean squared displacement')
plt.title('Ch10: MSD grows linearly; gradient rises with molecular speed')
plt.legend()
plt.show()
