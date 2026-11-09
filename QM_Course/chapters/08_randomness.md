# Chapter 8 — Randomness, simulation and statistics

**Goal:** understand what a computer's "random" numbers really are, how to use
them honestly, and the statistical reasoning that makes a simulation *evidence*.

---

## 8.1 Pseudo-random numbers

Computers are deterministic machines; they cannot be random. They run a
*generator*: a formula that produces a sequence so irregular it passes
statistical tests for randomness. Hence **pseudo-random**.

```python
import numpy as np

np.random.uniform(0, 1)              # one number in [0, 1)
np.random.uniform(0, 2*np.pi, 200)   # 200 angles at once
np.random.uniform(-50, 50, (100, 3)) # a 100x3 grid of positions
```

Uniform means every value in the range is equally likely. That is a **physical
assumption** when you use it for step directions: no direction is preferred,
i.e. no external field, no current, no gravity in the plane. If your walk should
drift, you would *not* use a uniform distribution — and saying that out loud is
what separates modelling from copying.

Other distributions you'll meet:

```python
np.random.normal(0, 0.05, 12)     # Gaussian noise: mean 0, sd 0.05
np.random.binomial(n, p)          # number of successes out of n trials
```

`normal` generated the fake experimental scatter in Task 4; `binomial` decides
how many photons eject electrons per frame in the simulator.

---

## 8.2 Reproducibility: seeds

Two runs give different numbers — usually good, sometimes disastrous (you can't
reproduce a figure or debug a specific case). A **seed** fixes the starting point
of the generator:

```python
rng = np.random.default_rng(1)      # modern style, seed = 1
noise = rng.normal(0, 0.05, 12)     # same 12 numbers every run
```

Your Task 4 uses `default_rng(1)` so the simulated experiment is identical each
time you run it — the h you recover is stable, and the figure in your report
matches the figure on your screen. Task 10's Monte Carlo uses `default_rng(0)`
for the same reason.

**Scientific standard:** publish your seed. Anyone can then reproduce your exact
figure. Unseeded randomness in a results figure is a small scientific sin.

Two styles exist:

```python
np.random.uniform(...)              # older global generator
rng = np.random.default_rng(seed)   # newer, self-contained generator object
rng.uniform(...)
```

Both are fine; the second is preferred in new code because the generator is an
object you can pass around, not hidden global state.

---

## 8.3 One run proves nothing

This is the heart of computational physics.

A single random walk ends *somewhere*. It tells you nothing about the law
governing walks, just as one coin flip tells you nothing about fairness. The
information lives in the **distribution over many runs**.

So every random experiment in this project has the same skeleton:

```python
results = []
for trial in range(many):
    result = run_one_experiment()
    results.append(result)

summary = np.mean(results)      # or std, or a histogram
```

Repeating and averaging is not a formality — it *is* the measurement.

---

## 8.4 How error shrinks: the 1/√N law

Averaging N independent trials reduces the random error in the mean by a factor
of **√N**:

  error ∝ σ / √N

Practical consequences:

- 100 trials → error ~10% of the spread
- 10,000 trials → error ~1%
- To halve your error you need **four times** the trials.

That's why your RMS came out 10.07 rather than exactly 10.00 with 1000 walks,
and why the honest answer to "how do I improve it?" is "more trials" — with the
quantitative rider that ten times more trials gives only about three times less
error. Diminishing returns are a real design constraint: at some point you
accept 1% and move on.

---

## 8.5 Mean, RMS and why we square

Three different "average distances", and they are not equal:

```python
mean_d  = np.mean(d)                    # average distance
rms_d   = np.sqrt(np.mean(d**2))        # root-mean-square distance
msd     = np.mean(d**2)                 # mean squared displacement
```

For a 2D random walk of N steps of size s, theory gives exactly:

  ⟨R²⟩ = N s²  →  R_rms = s√N

but the *mean* distance is ⟨R⟩ = (√π/2)·s√N/… ≈ 0.886 s√N — noticeably smaller.
Both appeared in the competitor's terminal output (mean 76.2, RMS 86.6 for the
same walks) precisely because they differ.

**Why physics prefers the squared quantity:** the mean squared displacement is
exactly linear in N with no awkward constant, because squared contributions from
independent steps simply add. Take the square root at the end if you want a
distance. Squaring also kills sign cancellation — the mean *displacement vector*
of many walks is zero, but the mean squared displacement is not.

**Derivation, since you should be able to give it.** After N steps,
**R** = Σᵢ **sᵢ**, so

  R² = Σᵢ Σⱼ **sᵢ**·**sⱼ** = Σᵢ |**sᵢ**|² + Σ(i≠j) **sᵢ**·**sⱼ**

Each step has |**sᵢ**|² = s², giving Ns². The cross terms average to zero because
independent random directions have ⟨cos(θᵢ−θⱼ)⟩ = 0. Therefore ⟨R²⟩ = Ns². ∎

Two lines of algebra, and it's the reason for a headline result in your project.

---

## 8.6 Distributions: what shape should the answer have?

Verifying a mean is good; verifying the whole **distribution** is better. For a
2D random walk, the final displacement R follows the **Rayleigh distribution**:

  P(R) = (R/σ²)·exp(−R²/2σ²),  with σ² = Ns²/2

Your Task 1 histogram overlays the simulated distribution on this curve. If only
the mean matched but the shape didn't, something would be wrong with the model —
so this test is strictly stronger.

Plotting a histogram as a probability density:

```python
plt.hist(finals, bins=40, density=True, alpha=0.7, label='simulation')
plt.plot(Rr, (Rr/sigma2)*np.exp(-Rr**2/(2*sigma2)), 'r', label='theory')
```

`density=True` normalises the histogram so its area is 1 — essential, otherwise
it can't be compared with a probability density function.

---

## 8.7 Monte Carlo methods

"Monte Carlo" = using random sampling to compute something.

**Rejection sampling**, used for the 3D orbitals, is the clearest example:

```python
pts = rng.uniform(-extent, extent, (400000, 3))    # candidate points
dens = psi(n, l, m, pts[:,0], pts[:,1], pts[:,2])**2
keep = rng.uniform(0, dens.max(), 400000) < dens   # accept with prob ∝ density
P = pts[keep]
```

Logic: scatter points uniformly through a box; for each, roll a number between 0
and the maximum density; keep the point if the roll lands under the local
density. Dense regions keep more points. The surviving cloud is a genuine sample
of |ψ|² — every dot is a *possible electron position*, weighted correctly.

That is philosophically the honest picture of an orbital: quantum mechanics gives
a probability distribution, and this shows samples from it, rather than an
arbitrary surface drawn at some threshold.

---

## 8.8 Simulation hygiene — a checklist

Before believing your own simulation:

1. **Reset state between runs.** (Your `for run in range(runs)` loop resets x, y,
   bx, bvx first — forget it and later runs inherit earlier ones.)
2. **Check a known limit.** Does it give the right answer where theory is exact?
3. **Vary a parameter and check the trend** (more steps → larger spread; higher
   voltage → smaller rings).
4. **Vary the resolution.** If halving the time step changes the answer, your
   result depends on your numerics, not physics.
5. **Fix a seed for the final figures.**
6. **State assumptions.** Uniform angles, ignoring molecule–molecule collisions,
   drag as a simple factor — say them out loud; they are the model.

Point 4 deserves emphasis: a result that changes when you change the grid size
is not yet a result. Your Task 7 integration used 20,000 points and matched the
analytic answer to four significant figures — that's a convergence check passed.

---

## Exercises

Create `ch08_exercises.py`.

1. Generate 10,000 uniform numbers in [0,1). Print mean and standard deviation.
   What should they be theoretically? (Exact answers: 0.5 and 1/√12 ≈ 0.2887.)
2. Simulate 1000 coin flips with `rng.integers(0, 2, 1000)`; print the fraction
   of heads. Repeat for 10 and for 100,000 flips. Relate what you see to §8.4.
3. Run a 400-step 2D walk 2000 times. Print the mean distance and the RMS
   distance. Confirm the ratio is about 0.886 and explain why they differ.
4. Show the 1/√N law numerically: for N = 10, 100, 1000, 10000 trials, estimate
   the RMS distance of a 100-step walk and print the deviation from 10.
   Does the error roughly quarter when trials rise 16-fold?
5. Use rejection sampling to fill a circle uniformly: sample points in a square,
   keep those with x²+y² < 1, plot them. What fraction survive, and what
   famous constant is 4× that fraction?
6. **Break it:** in a repeated-experiment loop, deliberately move the reset lines
   *outside* the loop. Plot the results and describe what goes wrong.

---

## What you now know

- Pseudo-random generators; uniform sampling encodes a physical assumption.
- Seeds make results reproducible — publish them.
- One run proves nothing; the distribution over many runs is the measurement.
- Error falls as 1/√N: four times the work for half the error.
- Mean ≠ RMS; squaring gives the clean linear law, and you can derive ⟨R²⟩ = Ns².
- Verify distributions, not just means (Rayleigh test).
- Monte Carlo rejection sampling produces honest samples of |ψ|².
- Simulation hygiene: reset, check limits, vary resolution, seed, state assumptions.

**End of Part 2.** You now have every tool the physics chapters use.

Next: [Chapter 9 — Task 1: Random walks](09_task1_random_walk.md)
