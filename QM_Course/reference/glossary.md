# Glossary

## Programming

**argument** — a value passed into a function call.

**array** — numpy's block of same-type numbers; supports element-wise maths.

**artist** — any drawable matplotlib object (line, patch, text) you can keep a
handle to and modify.

**boolean mask** — an array of True/False used to select or modify elements.

**broadcasting** — applying an operation between arrays of different shapes, e.g.
array × single number.

**callback** — a function you register to be run when an event happens.

**closure (late binding)** — a lambda looks up variables when *called*, not when
created; fixed with default arguments.

**docstring** — the string at the top of a function documenting it.

**event loop** — the waiting loop that dispatches user events (`plt.show()`,
`root.mainloop()`).

**f-string** — `f"{value:.2f}"`, a string with embedded expressions.

**float** — a decimal number, stored approximately.

**global** — keyword letting a function modify a variable defined outside it.

**index** — position in a sequence, counting from 0.

**interpreter** — the program that executes your Python.

**iterable** — anything you can loop over.

**lambda** — a small anonymous inline function.

**library / module / package** — reusable code you import.

**list** — an ordered, growable collection.

**local variable** — a name that exists only inside a function call.

**mutable** — changeable in place (lists, arrays are; tuples, strings aren't).

**return** — hands a value back from a function and ends it immediately.

**scope** — the region of code where a name is visible.

**shape** — an array's dimensions, e.g. `(30, 2000)`.

**slice** — a subsection, `a[2:5]`; the stop index is excluded.

**string** — text.

**tuple** — a fixed, unchangeable ordered group.

**unpacking** — `x, y = f()`, assigning several names at once.

**vectorisation** — expressing element-wise work as whole-array operations
instead of loops.

---

## Numerical methods

**convergence check** — repeating a calculation at higher resolution to confirm
the answer has stopped changing.

**floating-point error** — the ~10⁻¹⁶ relative error inherent in decimal storage.

**catastrophic cancellation** — loss of precision when subtracting nearly-equal
numbers; why `expm1` exists.

**least squares** — fitting by minimising the sum of squared residuals
(`np.polyfit`).

**linearisation** — transforming variables so theory predicts a straight line.

**Monte Carlo** — using random sampling to compute a result.

**rejection sampling** — keeping random candidates with probability proportional
to a target distribution.

**seed** — the number fixing a pseudo-random sequence, making runs reproducible.

**trapezium rule** — numerical integration by joining points with straight lines;
error O(Δx²).

**recurrence relation** — computing term n from earlier terms; how special
polynomials are generated.

---

## Physics

**antibonding orbital** — LCAO combination with a node between nuclei; higher
energy.

**Bohr radius (a₀)** — 5.29 × 10⁻¹¹ m; where the 1s radial probability peaks.

**bonding orbital** — LCAO combination with density piled between nuclei; the
covalent bond.

**Bragg's law** — 2d sin θ = nλ; condition for constructive scattering off
crystal planes.

**Brownian motion** — random motion of a suspended particle from molecular
bombardment.

**Compton wavelength** — h/mₑc = 2.426 pm; scale of the Compton shift.

**correspondence principle** — quantum results approach classical ones for large
quantum numbers.

**de Broglie wavelength** — λ = h/p; every particle's wave nature.

**degeneracy** — different states sharing the same energy.

**diffusion coefficient (D)** — constant in ⟨R²⟩ = 4Dt (2D).

**Dulong–Petit limit** — classical molar heat capacity 3R ≈ 24.9 J K⁻¹ mol⁻¹.

**Einstein temperature (θ_E)** — hf/k_B for a solid's characteristic vibration.

**entanglement** — a joint state of two particles not decomposable into
independent states; correlations depend only on the relative measurement angle.

**expectation value** — ⟨f⟩ = ∫ψ*fψ dV, the mean of many measurements.

**Langevin equation** — damping plus random forcing; the standard model of
Brownian motion.

**LCAO** — Linear Combination of Atomic Orbitals; building molecular orbitals by
adding atomic ones.

**Malus's law** — transmitted intensity ∝ cos²α; as a photon probability.

**metamerism** — different spectra that look identical.

**node** — where the wavefunction is exactly zero.

**normalisation** — scaling ψ so total probability is 1.

**photoelectric effect** — electron emission by photons; KE = hf − W.

**Planckian locus** — the path of black-body colours through colour space.

**quantum numbers** — n (energy/size), l (shape), m (orientation).

**Rayleigh distribution** — the distribution of 2D random-walk displacements.

**Rayleigh–Jeans law** — classical black-body formula; diverges at short λ.

**reduced mass** — μ = m₁m₂/(m₁+m₂); corrects for finite nuclear mass.

**rejection of local realism** — experiments (Aspect et al.) confirming quantum
correlations that no local hidden-variable theory can produce.

**spherical harmonics (Y_l^m)** — the angular part of hydrogenic wavefunctions.

**stopping voltage** — the reverse voltage that just prevents photoelectrons
reaching the anode; V_s = (hf − W)/e.

**tristimulus values (XYZ)** — the three numbers that define a colour.

**ultraviolet catastrophe** — the classical prediction of infinite short-λ
emission.

**uncertainty principle** — Δx·Δp ≥ ħ/2.

**wavefunction (ψ)** — the quantum state; |ψ|² is a probability density.

**Wien's displacement law** — λ_max T = 2.898 × 10⁻³ m K.

**work function (W)** — minimum energy to remove an electron from a metal.

**zero-point energy** — the non-zero minimum energy of a confined quantum system.
