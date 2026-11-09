# Chapter 22 — Capstone: rebuild everything from scratch

**Goal:** prove to yourself that the project is yours. You will rebuild it in an
empty folder, without copying, in graded stages.

---

## How to use this chapter

Make a folder called `rebuild/` **outside** the project. Do not open the original
files. Use only:

- your own memory
- the reference sheets in `reference/`
- the physics sections of the chapters (formulas are fair game — memorising
  constants is not the skill)
- official documentation (numpy/matplotlib docs are what professionals use)

When you get stuck for more than 20 minutes, read the relevant chapter *section*,
close it, and type from understanding rather than sight.

Tick each stage off as you pass its acceptance test.

---

## Level 1 — Foundations (aim: 1 hour)

**1.1** Write `warmup.py` that prints the photon energy in eV for wavelengths
400, 500, 600 and 700 nm, using constants defined at the top, formatted to 2
decimal places, in a loop.
*Accept when:* 400 nm gives 3.10 eV and 700 nm gives 1.77 eV.

**1.2** Write a function `de_broglie(V)` and print electron wavelengths at 1, 3
and 5 kV in picometres.
*Accept when:* 1 kV gives 38.8 pm.

**1.3** Write `rms_of(values)` that returns the root-mean-square of a list,
**without** numpy. Test it against `np.sqrt(np.mean(np.array(v)**2))`.
*Accept when:* they agree to 10 decimal places.

---

## Level 2 — Task 1, unaided (aim: 1 hour)

**2.1** Write `random_walk(N, s)` returning x and y arrays that start at the
origin.
*Accept when:* `len(x) == N+1` and `x[0] == 0`.

**2.2** Plot one walk with start/end markers, labels, title, equal aspect.

**2.3** Verify the RMS law for N = 100, 400, 900, 1600 over 1000 trials each.
*Accept when:* each RMS is within 3% of √N.

**2.4** Plot the 5000-walk displacement histogram against the Rayleigh curve, with
the fractional error in ⟨R²⟩ computed and printed in the title.
*Accept when:* the error is under 2% and the curve visibly fits.

**2.5** The 50-walk overlay.

---

## Level 3 — Animation (aim: 2 hours)

**3.1** Animate 200 molecules doing random walks in a box with reflecting walls.
*Accept when:* it runs at a smooth frame rate and nothing escapes.

**3.2** Add a large particle drawn as a `Circle` patch with the true radius R,
detect collisions with a boolean mask, and apply momentum kicks along the line of
centres.
*Accept when:* the particle moves only as a result of collisions, and molecules
never end up inside the circle.

**3.3** Add viscous drag and tune it until the trail is jagged and wandering
rather than gliding or frozen. Record which values fail in each direction.

**3.4** Add the growing trail and a live squared-displacement panel.

**3.5** In a *separate* file with no plotting inside the loops, run 30 experiments
× 2000 steps and plot the mean squared displacement.
*Accept when:* the curve rises roughly linearly. If it is flat at zero, re-read
Chapter 5 §5.1.

---

## Level 4 — The plotting tasks (aim: 3 hours)

**4.1 Planck.** Curves for five temperatures, Wien locus through the peaks,
Rayleigh–Jeans divergence, visible band shaded, peak wavelengths printed.
*Accept when:* the dashed locus passes through every peak and 5778 K peaks at
502 nm.

**4.2 Einstein heat capacity.** Four metals, Dulong–Petit line.
*Accept when:* every curve approaches 24.9 from below and none crosses it.

**4.3 Photoelectric.** Five metals, NaN below cutoff, printed cutoff table,
simulated noisy data fitted to recover h.
*Accept when:* your recovered h is within 0.5% of the true value.

**4.4 Hydrogen.** E₀ computed from constants, four series with limits, log
x-axis, Balmer comparison table against lab values.
*Accept when:* every Balmer line matches to better than 0.05%.

**4.5 Electron diffraction.** Three screen views, straight-line check, spacings
recovered from the gradients.
*Accept when:* both recovered spacings round to 0.213 and 0.123 nm.

**4.6 Compton.** Three beams, three panels, energy-conservation self-test.
*Accept when:* the 511 keV beam gives max fractional shift 2.0000 and max recoil
speed 0.8000c.

---

## Level 5 — Quantum mechanics (aim: 3 hours)

**5.1 Particle in a box.** Energies with the n² curve, stacked probability
densities, and the uncertainty table by numerical integration for n = 1…10.
*Accept when:* n=1 gives 0.5679 and every state exceeds 0.5.

**5.2** Add a convergence check: the same calculation at 50, 500 and 20000 grid
points, printed together.
*Accept when:* you can state how many points are needed for 4 significant figures.

**5.3 Quantum cryptography.** Both mismatch functions, a two-slider GUI with a
live bar chart and detector schematic, plus the two heat maps.
*Accept when:* θ = φ gives exactly zero quantum mismatch at any angle.

**5.4 Orbitals.** Laguerre and Legendre from recurrences, ψ assembled, the
verification table, a nine-panel gallery, and a Monte Carlo 3D cloud.
*Accept when:* all norms print as 1.000000 and every ⟨r⟩ matches
(a₀/2)[3n²−l(l+1)].

**5.5 LCAO.** Bonding and antibonding H₂⁺ orbitals with a bond-length slider.
*Accept when:* the antibonding orbital shows a clear nodal plane at the midpoint
at every R.

---

## Level 6 — Integration (aim: 2 hours)

**6.1** Write `cie_color.py` with the Gaussian-fit colour-matching functions,
XYZ→sRGB with gamma, and both public functions.
*Accept when:* 486 nm returns approximately (0, 0.75, 1) and 656 nm returns
(1, 0, 0).

**6.2** Use it in the hydrogen spectroscope view and the black-body glow swatches.

**6.3** Build the tkinter launcher with cards for everything, whole-card clicking,
`subprocess.Popen` launching, and a status line.
*Accept when:* every card opens the right script and the launcher stays
responsive.

**6.4** Build the photoelectric virtual lab: drawn apparatus, three sliders,
metal selection, pause/reset, animated photons and electrons, current meter, and
a status banner.
*Accept when:* raising the retarding voltage past V_s drives the current to
exactly zero, and red light on sodium emits nothing at any intensity.

---

## Level 7 — Go beyond (choose two)

Now build something that was never in the original project.

- **Debye heat capacity** — implement the T³ law and plot it against Einstein's
  model and real data for copper.
- **Realistic diffraction rings** — Gaussian ring profiles, second-order rings,
  intensity falloff, rendered as an image.
- **2D Schrödinger solver** — solve the particle in a box numerically via matrix
  eigenvalues, then try a harmonic well and a double well. Compare with analytic
  results.
- **Bell/CHSH analysis** — compute S for both models at the optimal angles and
  show the quantum value exceeds the classical bound.
- **H₃⁺ molecular orbitals** — three centres, triangular geometry.
- **Klein–Nishina** — the angular probability distribution for Compton scattering.
- **Full Langevin thermostat** — sample molecule speeds from Maxwell–Boltzmann,
  derive drag from Stokes' law, and check the fluctuation–dissipation relation.
- **Rewrite Task 2 as a class** — `class BrownianSystem` with `step()` and
  `run()` methods, eliminating every `global`.

---

## Final self-assessment

Answer these out loud, without notes. If any answer is shaky, you know which
chapter to revisit.

1. Why does `cumsum` turn steps into positions?
2. What does a boolean mask do, and why is it faster than a loop?
3. Why does an animation callback need `global`, and how would a class avoid it?
4. Why `expm1` instead of `exp(x) - 1`?
5. Why does the photoelectric graph use `np.nan` below the cutoff?
6. What does `polyfit(x, y, 1)` compute, and how did you get h out of it?
7. Why is the straight-line diffraction check better evidence than the ring
   picture?
8. What exactly does the trapezium rule do, and how do you know 20000 points is
   enough?
9. What is the physical difference between |ψ|² and r²|R|²?
10. Why does the quantum mismatch depend only on φ − θ?
11. What is rejection sampling, and why is it an honest way to draw an orbital?
12. Why is gamma correction needed to display a spectrum?
13. In your Brownian model, name three simplifying assumptions and their
    consequences.
14. Give one result in the project you could defend to a sceptical examiner, and
    explain the evidence.

---

## After the capstone

You will have built, twice, a piece of computational physics that verifies its
own results. That is the actual job — not writing code, but building models you
have reason to trust.

Where to go next:

- **scipy** — integration, optimisation, differential equations, special
  functions (now that you can implement them yourself, using the library is a
  choice rather than a crutch)
- **Numerical methods** — Runge–Kutta, finite differences, eigenvalue solvers
- **A real quantum course** — Griffiths' *Introduction to Quantum Mechanics* is
  the standard, and everything in Part 3 will now look familiar
- **Version control** — learn `git` properly; it is how all real code is written
- **Your own question** — the best projects start from something you genuinely
  want to know

Good luck. You have everything you need.
