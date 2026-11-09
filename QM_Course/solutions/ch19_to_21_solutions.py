"""
Solutions: Chapters 19-21 (widgets, tkinter, colour science)

Run this file directly. It opens two interactive windows in turn:
  1. a wave explorer  (sliders + radio buttons + reset)
  2. a particle-in-a-box explorer
then prints the colour-science answers.

The tkinter exercises are described at the bottom - see ch20_launcher_demo.py.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

h = 6.62607015e-34
c = 2.99792458e8
kB = 1.380649e-23
e = 1.602176634e-19
me = 9.1093837015e-31

# ---------------------------------------------------------------
# Ch19 Ex 1-3: wave explorer with two sliders, radio buttons, reset
# ---------------------------------------------------------------
x = np.linspace(0, 10, 800)

fig = plt.figure(figsize=(9, 5.5))
ax = fig.add_axes([0.1, 0.35, 0.85, 0.55])
line, = ax.plot(x, np.sin(x))
ax.set_ylim(-3.2, 3.2)
ax.set_xlabel('x')
ax.set_title('Ch19: wave explorer')

ax_f = fig.add_axes([0.15, 0.20, 0.6, 0.03])
ax_a = fig.add_axes([0.15, 0.14, 0.6, 0.03])
ax_r = fig.add_axes([0.80, 0.05, 0.17, 0.18])
ax_b = fig.add_axes([0.15, 0.04, 0.12, 0.05])

s_f = Slider(ax_f, 'frequency', 0.1, 5.0, valinit=1.0)
s_a = Slider(ax_a, 'amplitude', 0.1, 3.0, valinit=1.0)
r_mode = RadioButtons(ax_r, ['sine', 'cosine', 'damped'])
b_reset = Button(ax_b, 'Reset')

def redraw(_=None):
    f, A = s_f.val, s_a.val
    mode = r_mode.value_selected
    if mode == 'sine':
        y = A*np.sin(f*x)
    elif mode == 'cosine':
        y = A*np.cos(f*x)
    else:
        y = A*np.exp(-0.3*x)*np.sin(f*x)
    line.set_ydata(y)
    fig.canvas.draw_idle()

def do_reset(_):
    s_f.reset()
    s_a.reset()

s_f.on_changed(redraw)          # pass the function, do NOT call it
s_a.on_changed(redraw)
r_mode.on_clicked(redraw)
b_reset.on_clicked(do_reset)
redraw()

# ---------------------------------------------------------------
# Ch19 Ex 4: particle in a box explorer
# ---------------------------------------------------------------
fig2 = plt.figure(figsize=(9, 5.5))
axb = fig2.add_axes([0.12, 0.32, 0.83, 0.58])
ax_n = fig2.add_axes([0.15, 0.16, 0.6, 0.03])
ax_L = fig2.add_axes([0.15, 0.08, 0.6, 0.03])
s_n = Slider(ax_n, 'quantum number n', 1, 10, valinit=1, valstep=1)
s_L = Slider(ax_L, 'box width (nm)', 0.5, 5.0, valinit=1.0)

box_line, = axb.plot([], [], lw=2)
fill = [None]

def redraw_box(_=None):
    n = int(s_n.val)
    a = s_L.val*1e-9
    xg = np.linspace(0, a, 1000)
    psi2 = (2/a)*np.sin(n*np.pi*xg/a)**2
    E = n**2*h**2/(8*me*a**2)/e
    box_line.set_data(xg*1e9, psi2/1e9)
    if fill[0] is not None:
        fill[0].remove()
    fill[0] = axb.fill_between(xg*1e9, psi2/1e9, alpha=0.3)
    axb.set_xlim(0, s_L.val)
    axb.set_ylim(0, 2.2/s_L.val)
    axb.set_xlabel('x (nm)')
    axb.set_ylabel(r'$|\psi|^2$ (nm$^{-1}$)')
    axb.set_title(f'n = {n}, a = {s_L.val:.2f} nm,  E = {E:.3f} eV,  '
                  f'{n-1} nodes')
    fig2.canvas.draw_idle()

s_n.on_changed(redraw_box)
s_L.on_changed(redraw_box)
redraw_box()

# ---------------------------------------------------------------
# Ch21: colour science answers
# ---------------------------------------------------------------
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
try:
    from cie_color import wavelength_to_rgb, spectrum_to_rgb, cie_xyz_bar

    print("=" * 60)
    print("CHAPTER 21 - Colour science")
    print("=" * 60)

    print("Ex 2: named colours")
    for lam in [400, 450, 500, 550, 600, 650, 700]:
        rgb = wavelength_to_rgb(lam)
        print(f"  {lam} nm -> R={rgb[0]:.2f} G={rgb[1]:.2f} B={rgb[2]:.2f}")

    def planck(lam, T):
        return (2*h*c**2/lam**5)/np.expm1(h*c/(lam*kB*T))

    print("\nEx 3: black-body colours")
    lam_vis = np.linspace(380e-9, 740e-9, 400)
    for T in [1000, 2000, 3000, 4000, 5778, 8000, 12000]:
        B = planck(lam_vis, T)
        rgb = spectrum_to_rgb(lam_vis*1e9, B/B.max())
        white = np.std(rgb)
        print(f"  {T:>5} K -> ({rgb[0]:.2f}, {rgb[1]:.2f}, {rgb[2]:.2f})  "
              f"deviation from white = {white:.3f}")
    print("  Closest to white around 5500-6500 K - daylight, as expected.")

    print("\nEx 5: metamerism test (sodium D lines)")
    single = wavelength_to_rgb(589.3)
    lam_pair = np.array([589.0, 589.6])
    mix = spectrum_to_rgb(lam_pair, np.array([1.0, 1.0]))
    print(f"  589.3 nm alone : ({single[0]:.3f}, {single[1]:.3f}, {single[2]:.3f})")
    print(f"  589.0 + 589.6  : ({mix[0]:.3f}, {mix[1]:.3f}, {mix[2]:.3f})")
    print("  Indistinguishable: different spectra, identical colour = metamerism.")

    print("\nEx 6: flat white spectrum")
    lam_flat = np.linspace(380, 740, 400)
    flat = spectrum_to_rgb(lam_flat, np.ones_like(lam_flat))
    print(f"  equal-energy spectrum -> ({flat[0]:.3f}, {flat[1]:.3f}, {flat[2]:.3f})")
    print("  Close to but not exactly (1,1,1): sRGB white is defined by the")
    print("  D65 daylight illuminant, not by an equal-energy spectrum.")

    # Ex 7: chromaticity diagram
    lams = np.linspace(380, 740, 400)
    xb, yb, zb = cie_xyz_bar(lams)
    tot = xb + yb + zb
    fig3, ax3 = plt.subplots(figsize=(6, 6))
    ax3.plot(xb/tot, yb/tot, 'k-', lw=1, label='spectral locus')
    Ts = np.linspace(1000, 15000, 60)
    px, py = [], []
    for T in Ts:
        B = planck(lam_vis, T)
        X = np.trapezoid(B*cie_xyz_bar(lam_vis*1e9)[0], lam_vis*1e9)
        Y = np.trapezoid(B*cie_xyz_bar(lam_vis*1e9)[1], lam_vis*1e9)
        Z = np.trapezoid(B*cie_xyz_bar(lam_vis*1e9)[2], lam_vis*1e9)
        px.append(X/(X+Y+Z)); py.append(Y/(X+Y+Z))
    ax3.plot(px, py, 'r-', lw=2, label='Planckian locus')
    ax3.set_xlabel('x'); ax3.set_ylabel('y')
    ax3.set_title('Ch21 Ex7: CIE chromaticity diagram')
    ax3.legend()
except ImportError:
    print("(cie_color.py not found - run this from inside the course folder)")

print("\nCh20 tkinter exercises: see ch20_launcher_demo.py in this folder.")
plt.show()
