# All exercises — printable worksheet

Every exercise from the course, collected. Solutions are in `solutions/`.

Work in a file per chapter, e.g. `ch06_exercises.py`.


---


## Chapter 1 — Setup and your first program

Create `ch01_exercises.py` and solve these. Answers in
`solutions/ch01_solutions.py` — genuinely try first.

1. Print your name, then on a separate line print the year.
2. Make Python print exactly this, quote marks included: `He said "quantum"`.
   (Hint: there are two kinds of quote mark in Python.)
3. Print the result of `7 / 2`, then `7 // 2`, then `7 % 2`. Work out from the
   output what `//` and `%` do.
4. **Break it:** write a working `print` line, then delete just the closing
   bracket. Run it. Read the error. What line number does Python blame, and why
   might that be different from where you deleted the bracket?
5. In interactive mode, type `2 ** 10`. What operation is `**`?

---


---


## Chapter 2 — Variables, numbers and types

Create `ch02_exercises.py`.

1. Store the electron mass, elementary charge and Planck's constant as
   variables with sensible names. Print each with 4 significant figures in
   scientific notation.
2. A photon has wavelength 486.1 nm. Compute its energy in joules, then in
   electronvolts (divide by e). Print both, formatted nicely. Check: you should
   get about 2.55 eV.
3. Predict, then check: what does `10 % 3` give? `10 // 3`? `-7 // 2`?
4. Write `0.1 + 0.2 == 0.3` and then write a version using `abs()` that
   correctly reports `True`.
5. **Break it:** compute `h*c/(lam*kB*T)` correctly, then delete the brackets
   and print both. By what factor do they differ, and why?
6. Using an f-string, print a line that reads exactly:
   `lambda = 656.3 nm  |  E = 1.89 eV` using variables, not typed text.

---


---


## Chapter 3 — Decisions and loops

Create `ch03_exercises.py`.

1. Print the first 10 square numbers using a `for` loop.
2. For each metal below, print whether visible light (take 500 nm) can eject an
   electron. Work functions in eV: caesium 2.10, sodium 2.28, zinc 4.31,
   copper 4.70. (Photon energy at 500 nm ≈ 2.48 eV.)
3. Use a nested loop to print a 5×5 multiplication table, aligned neatly with
   f-string width formatting.
4. Hydrogen: loop over `n1` from 1 to 3, and inside, `n2` from `n1+1` to `n1+4`,
   printing the photon energy `13.6 * (1/n1**2 - 1/n2**2)` eV for each
   transition.
5. **Break it:** take exercise 4 and remove the indentation on the print line so
   it sits at the outer level. What changes about the output, and why?
6. Write a `while` loop that starts at n=1 and finds the smallest n where
   `n**2 > 10000`.

---


---


## Chapter 4 — Lists and collections

Create `ch04_exercises.py`.

1. Make a list of the first six Balmer wavelengths (656.3, 486.1, 434.0, 410.2,
   397.0, 388.9). Print the first, the last, and the middle two using slicing.
2. Build the list `[1, 4, 9, 16, 25]` using an empty list and `.append()` in a
   loop.
3. Make a dictionary of four metals and their work functions. Loop over it and
   print, for each, the cutoff wavelength in nm using `1240 / W_eV`.
4. Given `data = [3, 8, 2, 9, 4]`, print its length, sum, mean (sum/len), max
   and min — without numpy.
5. Predict, then test: what does this print?
   ```python
   a = [1, 2, 3]
   b = a
   b[0] = 99
   print(a[0])
   ```
   Then fix it so `a` is unaffected.
6. Store three orbitals as tuples in a list, loop over them unpacking into
   `n, l, m`, and print `n + l + m` for each.

---


---


## Chapter 5 — Functions

Create `ch05_exercises.py`.

1. Write `de_broglie(V)` returning the electron wavelength for accelerating
   voltage V, using λ = h/√(2mₑeV). Test with V=1000 (expect ≈ 3.9e-11 m).
2. Write `bohr_energy(n)` returning −13.6/n² eV, then use it in a loop to print
   the first five levels.
3. Write `transition(n1, n2)` that returns *two* values: photon energy in eV and
   wavelength in nm. Call it for (2,3) — expect ≈1.89 eV, ≈656 nm.
4. **Break it:** write a function that ends with `return result`, then add a
   `print("done")` line *after* the return. Run it. Explain the output.
5. Write a function with a default argument `def escape_velocity(M, R,
   G=6.674e-11)` and call it both with and without G.
6. Copy the `count` example from §5.3, watch it fail, then fix it with `global`.
   Then fix it a *second* way — by returning the new value instead. Which is
   cleaner?

---


---


## Chapter 6 — numpy: arrays and vectorised thinking

Create `ch06_exercises.py`.

1. Make `np.linspace(0, 2*np.pi, 9)` and print its sine. Which entries should be
   zero? Are they *exactly* zero? Explain (Chapter 2 §2.4).
2. Create 1000 random angles, convert to dx, dy with step size 2, and use cumsum
   to build a path. Print the final position and the distance from the origin.
3. Make `d = np.array([3.0, 7.0, 1.0, 9.0, 5.0])`. Using a mask, print only the
   values below 6, count how many there are, and set them all to zero.
4. Build a 4×6 array of zeros. Fill row `i`, column `j` with `i*j` using nested
   loops. Then print the mean of each row (`axis=1`) and each column (`axis=0`).
5. Verify `np.argmax` behaviour: for `np.array([5, 2, 9, 4])`, print both
   `np.max` and `np.argmax` and state the difference in one sentence.
6. **Break it:** compute `np.exp(x) - 1` and `np.expm1(x)` for
   `x = 1e-12`. Print both with `.20e` formatting. Which is right, and why does
   it matter for Planck's law at long wavelengths?
7. Run the speed test in §6.10 and write the speedup factor in a comment.

---


---


## Chapter 7 — matplotlib: drawing graphs properly

Create `ch07_exercises.py`.

1. Plot sin(x) and cos(x) on one figure over 0 to 4π with labels, legend, title,
   grid, and axis labels.
2. Recreate the "two figures" pattern: figure 1 with a decaying exponential,
   figure 2 with its logarithm, one `plt.show()` at the end.
3. Make a 2×2 subplot grid showing y = x, x², x³, x⁴ over 0 to 2, each titled.
   Use `axes.flat` and `tight_layout`.
4. Draw a circle of radius 3 using `Circle` *and* a marker with `ms=30` on the
   same axes with `axis('equal')`. Resize the window and note which one changes
   physical size. Write one sentence explaining which you'd use for a collision
   radius.
5. Plot `np.random.uniform(0, 1, (50, 50))` with `pcolormesh` using three
   different colormaps and a colorbar. Which shows structure best?
6. Take any figure from exercises 1–3, save it at `dpi=300` with tight bounding
   box, and open the PNG to confirm.

---


---


## Chapter 8 — Randomness, simulation and statistics

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


---


## Chapter 9 — Task 1: Random walks

1. Run the RMS test with 100 trials instead of 1000. How much worse is the
   agreement? Relate to §8.4.
2. Change the step size to s = 5 and re-run the RMS test. Does the theory line
   need updating? (It should read s√N — check your code uses `s`, not 1.)
3. Plot RMS distance against √N for N = 100 … 2500 and fit a straight line with
   `np.polyfit`. What should the gradient be? What do you get?
4. Modify `random_walk` to take a `bias` argument that adds a small constant to
   every angle... then think: does that produce drift? Try instead adding a
   constant `bias` to `dx` only. Plot 50 such walks. What physical situation
   does this represent?
5. Write a 3D random walk (hint: you need two angles, θ and φ, and the correct
   way to sample uniformly on a sphere is `cos θ` uniform in [−1,1]). Verify the
   RMS law still gives s√N.
6. **Stretch:** compute the *fractal dimension* of a long walk using the
   box-counting method, and compare with the theoretical value of 2 for a random
   walk.

Solutions: `solutions/ch09_solutions.py`

---


---


## Chapter 10 — Task 2: Brownian motion and animation

1. Set `drag = 1.0` (no damping) and watch. Describe what happens and explain it
   in terms of accumulated momentum.
2. Set `M = 200`. What happens to the trail, and why? Predict before running.
3. Add a counter of total collisions and display it in the title using
   `np.sum(hit)` accumulated over frames.
4. Change `s` (molecule speed) and observe the effect on the MSD gradient. What
   physical quantity is `s` standing in for?
5. Fit a straight line to the linear part of your MSD curve with `np.polyfit`
   and extract the diffusion coefficient D from gradient = 4D.
6. **Harder:** implement proper elastic hard-disc collisions — reflect the
   molecule's velocity about the line of centres as well as kicking the disc.
   Does the qualitative behaviour change?
7. **Break it:** move the reset lines outside the `for run` loop in the
   measurement file. Plot the MSD and explain the shape you get.

Solutions: `solutions/ch10_solutions.py`

---


---


## Chapter 11 — Task 3: Planck's law and Einstein's heat capacity

1. Verify Stefan–Boltzmann numerically: integrate `planck(lam, T)` over
   wavelength with `np.trapezoid` for several T, and check the total is
   proportional to T⁴. (Fit `log(total)` against `log(T)` — the gradient should
   be 4.)
2. Verify Wien's law numerically: for each T, find the peak with `np.argmax` and
   check λ_max·T is constant. How close to 2.898e-3 do you get, and what limits
   the accuracy?
3. Show the Rayleigh–Jeans limit: plot the ratio of Planck to Rayleigh–Jeans
   against λ for T = 5778 K. At what wavelength does the classical formula
   become 10% wrong?
4. Add tungsten (θ_E ≈ 240 K) and aluminium (θ_E ≈ 290 K) to the heat-capacity
   plot. At 300 K, what fraction of the classical value has each metal reached?
5. Derive Wien's law yourself: differentiate B with respect to λ, set to zero,
   and show you get the transcendental equation x = 5(1 − e^(−x)) with
   x = hc/λk_BT. Solve it numerically (a `while` loop or `np.linspace` search)
   and recover b = 2.898e-3.
6. **Break it:** replace `np.expm1(u)` with `np.exp(u) - 1` and plot the ratio of
   the two versions at very long wavelengths (say 1 mm). Where do they diverge?

Solutions: `solutions/ch11_solutions.py`

---


---


## Chapter 12 — Task 4: The photoelectric effect

1. Add three metals (potassium 2.30 eV, silver 4.26 eV, gold 5.10 eV) and print
   their cutoff wavelengths. Which respond to visible light?
2. Change the noise level to 0.2 V and re-fit. How does the error in h change?
   Now increase to 50 data points at the same noise — quantify the improvement
   and relate it to §8.4.
3. Fit *every* metal's simulated data and print the mean and standard deviation
   of the eight h values you obtain.
4. Plot stopping voltage against **wavelength** instead of frequency. Why is the
   frequency version preferred for extracting h?
5. Implement least squares yourself with the closed-form equations in §12.3 and
   check against `np.polyfit` on the same data.
6. In the app, add a readout showing the *predicted* stopping voltage, then
   verify by hand that the current dies exactly there for three different
   metal/wavelength combinations.
7. **Break it:** delete the `V[f < f0] = np.nan` line. What does the graph now
   claim, and why is it false?

Solutions: `solutions/ch12_solutions.py`

---


---


## Chapter 13 — Task 5: The hydrogen spectrum and Bohr's model

1. Print the wavelength of the first four Lyman lines. Which part of the spectrum
   are they in? Why can't you see hydrogen's strongest transition?
2. Compute the ionisation energy of hydrogen from the ground state (n=1 → ∞) and
   compare with the accepted 13.598 eV.
3. Redo the Balmer comparison using the reduced mass μ = mₑm_p/(mₑ+m_p) with
   m_p = 1.6726219e-27 kg. By how much do the errors improve?
4. Add the Pfund series (n₁ = 5) to the plot with its limit.
5. Hydrogenic ions: energies scale as Z². Compute the Balmer-equivalent lines for
   He⁺ (Z = 2) and state where they fall.
6. Deuterium has a heavier nucleus (m ≈ 2m_p). Compute the *isotope shift* of the
   H-alpha line — the wavelength difference between hydrogen and deuterium. (This
   is how deuterium was discovered in 1931.)
7. **Break it:** replace `E0` with a hard-coded 13.6 eV and see how the printed
   comparison changes. Which digits move?

Solutions: `solutions/ch13_solutions.py`

---


---


## Chapter 14 — Task 6: Electron diffraction

1. Print λ at 1, 3 and 5 kV in picometres. Verify the shortcut λ(nm) = 1.226/√V.
2. Compute both ring radii at V = 2.5 kV in mm. Which is outer, and why?
3. Plot ring radius against V from 1–5 kV for both spacings on one graph. Is the
   relationship linear? What does the shape tell you?
4. **Best extension:** replace the thin circles with a realistic glow. Build a
   2D grid with `np.meshgrid`, compute the radial distance of every pixel, and
   set brightness with `exp(-(rad - x_ring)²/2σ²)` for each ring. Display with
   `pcolormesh` and a green colormap.
5. Add second-order diffraction (n = 2 in Bragg's law) and show where those rings
   fall. Are they inside or outside the first-order ones?
6. At what voltage would λ/2d exceed 1 for the 0.123 nm spacing, making
   diffraction impossible? What does `np.arcsin` return there, and how should
   the code handle it?
7. Add realistic noise to `sin_theta`, re-fit, and see how well d is still
   recovered. This mimics a real experimenter's uncertainty.

Solutions: `solutions/ch14_solutions.py`

---


---


## Chapter 15 — Task 7: Particle in a box and the uncertainty principle

1. Compute E₁ for an electron in boxes of 0.5, 1 and 2 nm. How does E scale with
   a? Explain physically why smaller boxes mean higher energies.
2. Compute the photon wavelength emitted for the n=2 → n=1 transition in a 1 nm
   box. Which part of the spectrum is that?
3. Verify normalisation numerically: integrate |ψₙ|² over the box for n = 1…5 and
   confirm each gives 1.000000.
4. **Convergence study:** compute Δx·Δp for n = 1 using 50, 200, 1000, 5000 and
   20000 grid points. Plot the error against the number of points on log axes.
   What power law do you get, and does it match the O(Δx²) claim?
5. Derive ⟨x²⟩ for the box analytically (integrate x²·(2/a)sin²(nπx/a)) and
   confirm your numerical value.
6. Compute ⟨p⟩ numerically using the momentum operator −iħ d/dx with
   `np.gradient` and confirm it is zero. Why must it be?
7. **Stretch:** solve the box numerically as a matrix eigenvalue problem —
   discretise the second derivative and use `np.linalg.eigh` — and compare the
   first five eigenvalues with n²E₁. This is how real quantum problems are
   solved when no analytic answer exists.

Solutions: `solutions/ch15_solutions.py`

---


---


## Chapter 16 — Task 8: Quantum cryptography

1. Find, by scanning with `np.meshgrid`, the (θ,φ) pair where |classical −
   quantum| is largest. What are the two probabilities there?
2. Verify θ = φ gives exactly zero quantum mismatch for ten random angles.
3. Extend the sliders to 0–180°. Does anything new appear? What symmetry do you
   observe, and why does sin² produce it?
4. Model Eve: assume she intercepts a fraction f of photons, measuring each in a
   random basis and re-sending. Derive (or reason out) the resulting mismatch
   and plot it against f. At what f could Alice and Bob detect her with 100
   sample bits?
5. Compute the CHSH quantity S = |E(a,b) − E(a,b′) + E(a′,b) + E(a′,b′)| where
   E = 1 − 2·P(mismatch), at the classic angles (0°, 22.5°, 45°, 67.5°). Local
   realism requires S ≤ 2; quantum mechanics allows up to 2√2 ≈ 2.83. Which do
   you get from each model?
6. Add a third panel showing the *difference* between the two heat maps with a
   diverging colormap.

Solutions: `solutions/ch16_solutions.py`

---


---


## Chapter 17 — Task 9: Compton scattering

1. Verify Δλ at θ = 90° equals λ_C exactly (2.426 pm) for all three beams. Why
   is it independent of λ₀?
2. Compute the fractional shift for **visible** light (500 nm) at 180°. Express
   it in parts per million. Why is Compton scattering irrelevant in optics?
3. Add a fourth beam at 100 keV and find the angle at which the electron takes
   half the photon's energy.
4. Plot the *scattered photon energy* against θ for all three beams and identify
   the "Compton edge" — the maximum energy transferred to the electron. This
   feature is directly visible in real gamma-ray spectra.
5. Verify momentum conservation numerically as a second self-test: compute the
   total x and y momentum before and after for every angle and print the largest
   residual.
6. Show that the non-relativistic formula v = √(2K/mₑ) exceeds c for the 1.24 MeV
   beam beyond some angle. At which angle does it break down?
7. **Stretch:** implement the Klein–Nishina formula for the *probability* of
   scattering at each angle and plot the angular distribution. This is what
   determines how often each θ actually occurs.

Solutions: `solutions/ch17_solutions.py`

---


---


## Chapter 18 — Task 10: Hydrogenic orbitals

1. Verify normalisation for n = 4, l = 0…3. Does it hold to six decimals?
2. Count radial nodes in the 3s, 3p and 3d radial functions by finding sign
   changes in `radial(...)`. Do they match n−l−1?
3. Plot the 1s density along a line through the nucleus *and* the radial
   probability r²|R|² on the same figure. Explain to someone why one peaks at 0
   and the other at a₀.
4. Set Z = 2 (He⁺). By what factor should ⟨r⟩ shrink? Verify numerically.
5. Add the y–z and x–y slice planes as options and confirm that the m = 1 and
   m = 2 orbitals look different in each.
6. Extend the LCAO to **H₃⁺**: three 1s orbitals at the corners of an equilateral
   triangle. Plot the fully symmetric combination. (Normalisation can be
   approximate here — state that you've approximated it.)
7. Build a p_x + p_z hybrid ("sp hybrid") and plot it. Which way does it point?
8. **Stretch:** compute the LCAO bonding energy as a function of R by evaluating
   the relevant integrals numerically, and find the equilibrium bond length.
   Compare with the true H₂⁺ value of 2.00 a₀.

Solutions: `solutions/ch18_solutions.py`

---


---


## Chapter 19 — Widgets: sliders, buttons and callbacks

1. Build the sine slider from §19.2 and add a second slider for amplitude.
2. Add a `Button` labelled "Reset" that returns both sliders to their initial
   values.
3. Add `RadioButtons` to switch between sine, cosine and a damped sine.
4. Make a "particle in a box" explorer: sliders for n (1–10, `valstep=1`) and box
   width, showing |ψ|² and printing the energy in the title. You have all the
   physics from Chapter 15.
5. **Break it:** register a callback as `on_changed(update())` with brackets. What
   happens, and what does the error tell you?
6. Build a Planck explorer: one temperature slider, the spectrum, a marker at the
   Wien peak, and a swatch showing the CIE glow colour (Chapter 21).

Solutions: `solutions/ch19_solutions.py`

---


---


## Chapter 20 — Building the launcher with tkinter

1. Build a three-button window: each button prints a different message.
2. Recreate the card layout with four of your own scripts.
3. Add hover highlighting: bind `<Enter>` and `<Leave>` to change the card's
   background. (Remember to bind the children too.)
4. **Break it:** remove the `s=script, n=name` defaults from the lambda and click
   several cards. Explain what happens using §20.6.
5. Add a "Run all" button that launches three scripts in sequence.
6. Add a text panel that shows a longer description when a card is hovered.
7. **Stretch:** rebuild the launcher with `tkinter.ttk` themed widgets, or embed
   a matplotlib figure inside a tkinter window using
   `FigureCanvasTkAgg` — that's the bridge to fully custom scientific apps.

Solutions: `solutions/ch20_solutions.py`

---


---


## Chapter 21 — Colour science: turning wavelengths into pixels

1. Run `cie_color.py` directly to see the spectrum strip. Compare it with a
   photograph of a real spectrum online.
2. Print the RGB for 400, 450, 500, 550, 600, 650, 700 nm and check each against
   what you'd expect by name.
3. Compute and plot the colours of black bodies from 1000 K to 12000 K as a strip
   of swatches. Where does it pass closest to white?
4. **Break it:** remove the gamma correction (return the linear rgb directly) and
   redraw the spectrum strip. Describe the difference precisely.
5. Sodium's D lines are at 589.0 and 589.6 nm. Compute the colour of an equal
   mixture and compare with the colour of 589.3 nm alone. Are they the same? What
   does this demonstrate about metamerism?
6. Compute the colour of a "flat" white spectrum (equal intensity at all
   wavelengths). Is it exactly (1,1,1)? Should it be?
7. **Stretch:** plot the CIE chromaticity diagram — compute x = X/(X+Y+Z),
   y = Y/(X+Y+Z) for every wavelength and draw the horseshoe curve, with your
   Planckian locus overlaid on it.

Solutions: `solutions/ch21_solutions.py`

---


---
