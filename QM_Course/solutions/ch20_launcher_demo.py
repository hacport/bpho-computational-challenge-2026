"""
Solutions: Chapter 20 (tkinter)

A minimal launcher demonstrating every technique from the chapter:
  - dark themed cards in a two-column grid  (i//2, i%2)
  - whole-card clicking with bound children
  - the late-binding fix (s=script defaults in the lambda)
  - hover highlighting  (Ex 3)
  - a description panel  (Ex 6)
  - a "Run all" button   (Ex 5)
  - subprocess launching with sys.executable
  - StringVar status line

Run:  python ch20_launcher_demo.py
"""
import tkinter as tk
import subprocess
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# (label, title, script, short description, longer description)
ITEMS = [
    ('1', 'Chapters 1-5', 'ch01_to_05_solutions.py',
     'Python fundamentals',
     'Variables, types, loops, lists, functions and scope. Prints every '
     'answer with an explanation of why it is the answer.'),
    ('2', 'Chapters 6-8', 'ch06_to_08_solutions.py',
     'numpy, plotting, randomness',
     'Vectorisation, masks, the speed test, and the statistics behind '
     'simulation: seeds, averaging, and the 1/sqrt(N) law.'),
    ('3', 'Chapters 9-10', 'ch09_to_10_solutions.py',
     'random walks and Brownian motion',
     'The sqrt(N) law in 2D and 3D, plus headless Brownian runs showing '
     'how drag and mass ratio change the diffusion coefficient.'),
    ('4', 'Chapters 11-14', 'ch11_to_14_solutions.py',
     'black body to diffraction',
     'Stefan-Boltzmann verified numerically, Wien solved from scratch, '
     'h recovered from noisy data, and the air-vs-vacuum lesson.'),
    ('5', 'Chapters 15-18', 'ch15_to_18_solutions.py',
     'quantum mechanics',
     'Convergence studies, the matrix eigenvalue solver, the CHSH test, '
     'Compton self-checks, and orbital verification.'),
    ('6', 'Chapters 19-21', 'ch19_to_21_solutions.py',
     'widgets and colour',
     'Interactive wave and particle-in-a-box explorers, plus the CIE '
     'chromaticity diagram and a metamerism demonstration.'),
]

BG, CARD, HOVER, FG, MUTED, ACCENT = ('#0d1117', '#161b22', '#21262d',
                                      '#e6edf3', '#8b949e', '#58a6ff')

root = tk.Tk()
root.title('Course solutions')
root.configure(bg=BG)
root.geometry('760x620')

tk.Label(root, text='COURSE SOLUTIONS', bg=BG, fg=ACCENT,
         font=('Segoe UI', 20, 'bold')).pack(pady=(16, 0))
tk.Label(root, text='click any card to run it  |  hover for detail',
         bg=BG, fg=MUTED, font=('Segoe UI', 9)).pack(pady=(2, 10))

grid = tk.Frame(root, bg=BG)
grid.pack(fill='both', expand=True, padx=20)

detail = tk.StringVar(value='Hover over a card to see what it covers.')
status = tk.StringVar(value='ready')

def launch(script, title):
    """Start a script as a separate process so the launcher stays alive."""
    subprocess.Popen([sys.executable, os.path.join(HERE, script)], cwd=HERE)
    status.set(f'launched: {title}')

def run_all(_=None):
    for item in ITEMS[:3]:
        launch(item[2], item[1])
    status.set('launched the first three')

for i, (num, title, script, short, long) in enumerate(ITEMS):
    card = tk.Frame(grid, bg=CARD, highlightbackground='#30363d',
                    highlightthickness=1)
    card.grid(row=i // 2, column=i % 2, sticky='nsew', padx=6, pady=6)
    grid.grid_columnconfigure(i % 2, weight=1)

    badge = tk.Label(card, text=f'  {num}  ', bg=ACCENT, fg=BG,
                     font=('Segoe UI', 13, 'bold'))
    badge.pack(side='left', padx=10, pady=12)

    body = tk.Frame(card, bg=CARD)
    body.pack(side='left', fill='x', expand=True, pady=8)
    tk.Label(body, text=title, bg=CARD, fg=FG, anchor='w',
             font=('Segoe UI', 11, 'bold')).pack(fill='x')
    tk.Label(body, text=short, bg=CARD, fg=MUTED, anchor='w',
             wraplength=250, justify='left',
             font=('Segoe UI', 8)).pack(fill='x')

    widgets = (card, badge, body) + tuple(body.winfo_children())

    # The s=script, t=title defaults capture the CURRENT values.
    # Without them every card would launch the last script (late binding).
    for w in widgets:
        w.bind('<Button-1>', lambda ev, s=script, t=title: launch(s, t))
        w.bind('<Enter>', lambda ev, ws=widgets, d=long:
               (detail.set(d), [x.configure(bg=HOVER) for x in ws
                                if x is not badge]))
        w.bind('<Leave>', lambda ev, ws=widgets:
               [x.configure(bg=CARD) for x in ws if x is not badge])

panel = tk.Label(root, textvariable=detail, bg=CARD, fg=FG, wraplength=700,
                 justify='left', anchor='w', font=('Segoe UI', 9),
                 padx=12, pady=10)
panel.pack(fill='x', padx=20, pady=(10, 4))

btn_row = tk.Frame(root, bg=BG)
btn_row.pack(pady=4)
run_btn = tk.Label(btn_row, text='  Run first three  ', bg=ACCENT, fg=BG,
                   font=('Segoe UI', 10, 'bold'))
run_btn.pack()
run_btn.bind('<Button-1>', run_all)

tk.Label(root, textvariable=status, bg=BG, fg=ACCENT,
         font=('Consolas', 9)).pack(pady=8)

root.mainloop()
