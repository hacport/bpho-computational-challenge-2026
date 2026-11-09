import subprocess
import sys
import os
import tkinter as tk

HERE = os.path.dirname(os.path.abspath(__file__))

TASKS = [
    ('1', 'Random walk', 'task1_random_walk.py',
     'N-step walk, RMS = s√N law verified over 4000 runs'),
    ('2', 'Brownian motion', 'task2_brownian_motion.py',
     'momentum-kick collisions, Langevin drag, live animation'),
    ('2+', 'Einstein diffusion MSD', 'task2_extension_diffusion.py',
     'mean squared displacement grows linearly - atoms are real'),
    ('3', 'Black body + heat capacity', 'task3_blackbody.py',
     'Planck curves, Wien locus, UV catastrophe, CIE glow colours'),
    ('4', 'Photoelectric effect', 'task4_photoelectric.py',
     'stopping voltage lines, h recovered from noisy fit to 0.06%'),
    ('4+', 'PhET-style simulator', 'task4_app_photoelectric.py',
     'animated photons & electrons, sliders, live readout'),
    ('5', 'Hydrogen spectrum', 'task5_hydrogen_spectrum.py',
     'Bohr model vs lab data (<0.04%), true-colour spectroscope'),
    ('6', 'Electron diffraction', 'task6_electron_diffraction.py',
     'Teltron rings, 1/√V straight line, spacings recovered'),
    ('7', 'Particle in a box', 'task7_particle_in_box.py',
     'E = n²E₁, nodes, uncertainty principle verified numerically'),
    ('8', 'Quantum cryptography', 'task8_quantum_cryptography.py',
     'classical vs quantum mismatch, sliders, entanglement signature'),
    ('9', 'Compton scattering', 'task9_compton.py',
     'wavelength shift, relativistic recoil, exact checks'),
    ('10', 'Hydrogenic orbitals', 'task10_hydrogenic_orbitals.py',
     'Laguerre/Legendre from scratch, 2D slices, 3D Monte Carlo'),
    ('10+', 'Orbital morphing', 'task10_extension_morph.py',
     'animated m-state morphing for n=3, l=2'),
    ('10++', 'H₂⁺ molecular orbitals', 'task10_extension_molecules.py',
     'LCAO bonding vs antibonding with bond-length slider'),
]

BG, CARD, FG, ACCENT = '#0d1117', '#161b22', '#e6edf3', '#58a6ff'

root = tk.Tk()
root.title('BPhO Computational Challenge 2026')
root.configure(bg=BG)
root.geometry('820x760')

tk.Label(root, text=' QUANTUM MECHANICS', bg=BG, fg=ACCENT,
         font=('Segoe UI', 22, 'bold')).pack(pady=(18, 0))
tk.Label(root, text='BPhO Computational Challenge 2026 ',
         bg=BG, fg=FG, font=('Segoe UI', 11)).pack(pady=(2, 12))

status = tk.StringVar(value='click any module to launch it')

frame = tk.Frame(root, bg=BG)
frame.pack(fill='both', expand=True, padx=24)

def launch(script, name):
    subprocess.Popen([sys.executable, os.path.join(HERE, script)], cwd=HERE)
    status.set(f'running: {name}   (close its window to return)')

for i, (num, name, script, desc) in enumerate(TASKS):
    card = tk.Frame(frame, bg=CARD, highlightbackground='#30363d',
                    highlightthickness=1)
    card.grid(row=i // 2, column=i % 2, sticky='nsew', padx=6, pady=5)
    frame.grid_columnconfigure(i % 2, weight=1)
    btn = tk.Label(card, text=f'  {num}  ', bg=ACCENT, fg=BG,
                   font=('Segoe UI', 13, 'bold'))
    btn.pack(side='left', padx=10, pady=10)
    body = tk.Frame(card, bg=CARD)
    body.pack(side='left', fill='x', expand=True, pady=6)
    tk.Label(body, text=name, bg=CARD, fg=FG, anchor='w',
             font=('Segoe UI', 11, 'bold')).pack(fill='x')
    tk.Label(body, text=desc, bg=CARD, fg='#8b949e', anchor='w',
             wraplength=290, justify='left',
             font=('Segoe UI', 8)).pack(fill='x')
    for w in (card, btn, body) + tuple(body.winfo_children()):
        w.bind('<Button-1>', lambda e, s=script, n=name: launch(s, n))

tk.Label(root, textvariable=status, bg=BG, fg=ACCENT,
         font=('Consolas', 10)).pack(pady=10)

root.mainloop()
