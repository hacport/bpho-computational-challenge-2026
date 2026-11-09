# Computational Quantum Physics — course folder

A complete, offline, self-paced course that teaches you to build the BPhO 2026
Quantum Mechanics entry from an empty file. Copy this whole folder to a flash
drive and it works anywhere, with no internet and no subscription.

## Start here

**Reading in a browser (recommended):** open `site/index.html`.
**Reading in VS Code:** open `START_HERE.md`.

Both contain identical content; the site is nicer to navigate, the markdown is
easier to search and copy from.

## What's in the folder

```
QM_Course/
├── START_HERE.md          the course map and how to use it
├── site/                  the offline website (open index.html)
├── chapters/              22 chapters as markdown
├── reference/             6 cheat sheets and lookups
├── exercises/             all exercises collected for printing
├── solutions/             worked solutions as runnable Python
└── build_site.py          regenerates site/ after editing any chapter
```

## The 22 chapters

**Part 1 — Python from zero (ch 1–5).** Setup, variables and types, decisions
and loops, lists and collections, functions and scope. Assumes nothing.

**Part 2 — Scientific Python (ch 6–8).** numpy arrays and vectorisation,
matplotlib, randomness and the statistics that make a simulation evidence.

**Part 3 — The ten tasks (ch 9–18).** Every physics model rebuilt from scratch,
each with its derivation, a line-by-line code build, and the verification that
proves it right.

**Part 4 — Interactivity (ch 19–21).** Widgets and callbacks, the tkinter
launcher, and CIE 1931 colour science.

**Part 5 — Capstone (ch 22).** Rebuild the entire project unaided, in seven
graded levels with acceptance tests.

## Using the solutions

Each file runs on its own and prints its answers with explanations:

```
cd solutions
python ch01_to_05_solutions.py
python ch06_to_08_solutions.py
python ch09_to_10_solutions.py
python ch11_to_14_solutions.py
python ch15_to_18_solutions.py
python ch19_to_21_solutions.py      # opens interactive windows
python ch20_launcher_demo.py        # a tkinter launcher for all of the above
```

Requirements: Python 3.8+, `numpy`, `matplotlib`. Install with
`pip install numpy matplotlib`.

## Editing the course

The markdown files are the source. After editing any chapter, run:

```
python build_site.py
```

to rebuild `site/`. (`pip install markdown` gives slightly better output, but the
script has a built-in fallback converter so it works either way.)

## A note on how to work

Read → type → break → fix. Reading teaches almost nothing; typing teaches a
little; deliberately breaking code and fixing it teaches nearly everything.
Every chapter has "Break it" exercises. Do them, and don't copy-paste.
