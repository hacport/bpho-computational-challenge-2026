# BPhO 2026 screencast — FINAL fused script
# Physics story + computational method, balanced. Spoken ≈ 2:48.
# Layout: launcher + figures LEFT, VS Code terminal RIGHT (launch
# quantum_lab.py from the terminal so prints appear there).
# [PAUSE] = pause OBS, close windows, open next task, resume.

## SEG 0 — 0:00 (11s)
SHOW: launcher, cursor drifting over cards
SAY: "Hi, I'm Hakeem. Ten quantum mechanics tasks, all in Python, all
launched from this app I built. My rule for the project: every model
must include a computation that could prove it wrong. Let me show you."
[PAUSE]

## SEG 1 — 0:11 (19s)
SHOW: Task 1 — single walk, then Rayleigh histogram
SAY: "I started with the random walk — three lines of vectorised numpy:
a thousand random angles, sine and cosine, and a cumulative sum turns
steps into a path. One walk looks like chaos, so I ran five thousand.
Order appears: the endpoints land on the Rayleigh distribution with
about one percent error."
[PAUSE]

## SEG 2 — 0:30 (23s)
SHOW: Task 2 animation with live MSD panel, then extension figure
SAY: "Then I asked where random walks come from. Two hundred molecules
batter a large particle — a boolean mask finds every collision, and
each one transfers momentum. Nobody programmed the red particle to
move; its jiggle emerges. Mine originally glided unphysically, so I
added fluid drag, which makes this a proper Langevin model. Averaged
over thirty runs, the squared displacement grows in a straight line —
Einstein's law, the result that proved atoms exist."
[PAUSE]

## SEG 3 — 0:53 (14s)
SHOW: Task 3 Planck figure with glow swatches
SAY: "Black body radiation: the dashed Wien law threads every peak, and
the dotted curve is classical physics blowing up — the catastrophe that
forced Planck to invent the quantum. The glow colours aren't chosen,
they're computed — each spectrum integrated against the CIE colour-
matching functions."
[PAUSE]

## SEG 4 — 1:07 (22s)
SHOW: Task 4 graph briefly, then simulator: raise retarding voltage
SAY: "For the photoelectric effect I recreated Millikan's experiment in
code: I generated noisy data on purpose, fitted it with least-squares
regression, and the gradient handed back Planck's constant to a tenth
of a percent. Then I built this simulator — and because it obeys the
same equation, watch: raising the retarding voltage kills the current
at exactly the stopping voltage the graph predicts."
[PAUSE]

## SEG 5 — 1:29 (13s)
SHOW: Task 5 figure, true-colour strip, terminal
SAY: "Hydrogen: I compute the ground state from raw constants — no
Rydberg value typed in — and generate every transition with two nested
loops. My Balmer lines match laboratory data to a twentieth of a
percent, shown here in their true colours."
[PAUSE]

## SEG 6 — 1:42 (15s)
SHOW: Task 6 rings, straight-line plot, terminal
SAY: "Electron diffraction: rings shrink as voltage rises, because
faster electrons have shorter de Broglie wavelengths. I did the
required straight-line check with a least-squares fit — then ran it
backwards: the gradients return both graphite atomic spacings exactly.
Measuring atoms from a simulated screen."
[PAUSE]

## SEG 7 — 1:57 (16s)
SHOW: Task 7 figures, terminal table
SAY: "Particle in a box: energies grow as n squared. For the extension
I tested Heisenberg's uncertainty principle by numerical integration —
trapezoidal rule on twenty thousand points — and every state sits above
half h-bar, with the ground state matching the exact analytic value to
four significant figures."
[PAUSE]

## SEG 8 — 2:13 (14s)
SHOW: Task 8 GUI, drag Bob through 45°
SAY: "Quantum cryptography, using the Malus-law model from the pack,
live sliders recomputing both predictions. Here's the punchline: with
Alice at forty-five degrees, classical physics is trapped at one half —
but the quantum mismatch drops to zero when the detectors align. That
impossible correlation is how you catch an eavesdropper."
[PAUSE]

## SEG 9 — 2:27 (8s)
SHOW: Task 9 three panels
SAY: "Compton scattering, fully relativistic — with a built-in unit
test: energy conservation closes to machine precision at all five
hundred angles."
[PAUSE]

## SEG 10 — 2:35 (17s)
SHOW: Task 10 gallery, 3D cloud, LCAO slider
SAY: "Finally, the hydrogen atom itself. I implemented the polynomials
from their recurrence relations — no libraries — and the terminal shows
every orbital integrating to exactly one, with the 1s peak at the Bohr
radius. The 3D clouds are Monte Carlo samples of the wavefunction. And
combining two atoms shows the covalent bond forming — bonding and
antibonding orbitals from my own code."

## SEG 11 — 2:52 (5s)
SHOW: back to launcher
SAY: "All the code is linked below. Thanks for watching."

# ---- rules ----
# Pause between segments: fine. Speeding footage: disqualified.
# Hard cap 3:00. One full timed practice before recording.
