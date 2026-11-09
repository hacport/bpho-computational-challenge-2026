import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons, Button
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Polygon
from matplotlib.animation import FuncAnimation
from cie_color import wavelength_to_rgb

h = 6.62607015e-34
e = 1.602176634e-19
c = 2.99792458e8

metals = {'Sodium': 2.28, 'Caesium': 2.10, 'Zinc': 4.31, 'Copper': 4.70}

PANEL, CHAMBER, PLATE = '#eef1f5', '#e8eef5', '#b8bfc9'
GOOD, WARN, BAD = '#1a7f37', '#b58105', '#c93c37'

fig = plt.figure(figsize=(12.5, 6.8), facecolor='white')
fig.canvas.manager.set_window_title('Photoelectric Effect - Virtual Lab')

ax = fig.add_axes([0.30, 0.13, 0.68, 0.80])
ax.set_xlim(0, 10); ax.set_ylim(0, 6)
ax.axis('off')
ax.set_title('Vacuum photocell  |  Live experiment', loc='left',
             fontsize=12, weight='bold')

fig.text(0.03, 0.90, 'Experiment setup', fontsize=9, color='#57606a')
fig.text(0.03, 0.86, 'Controls', fontsize=13, weight='bold')

ax_metal = fig.add_axes([0.03, 0.64, 0.20, 0.16], facecolor=PANEL)
ax_metal.set_title('Cathode metal', fontsize=9, loc='left', weight='bold')
r_metal = RadioButtons(ax_metal, list(metals.keys()), activecolor='#0969da')

ax_lam = fig.add_axes([0.05, 0.54, 0.17, 0.03])
s_lam = Slider(ax_lam, '', 160, 800, valinit=400, color='#0969da')
fig.text(0.03, 0.585, 'Wavelength (nm)', fontsize=9, weight='bold')
fig.text(0.03, 0.515, 'ultraviolet', fontsize=7, color='#57606a')
fig.text(0.20, 0.515, 'infrared', fontsize=7, color='#57606a')

ax_int = fig.add_axes([0.05, 0.43, 0.17, 0.03])
s_int = Slider(ax_int, '', 5, 100, valinit=55, valstep=5, color='#0969da')
fig.text(0.03, 0.475, 'Light intensity (%)', fontsize=9, weight='bold')

ax_ret = fig.add_axes([0.05, 0.32, 0.17, 0.03])
s_ret = Slider(ax_ret, '', 0, 6, valinit=0.0, color='#0969da')
fig.text(0.03, 0.365, 'Retarding voltage (V)', fontsize=9, weight='bold')

ax_pause = fig.add_axes([0.03, 0.22, 0.09, 0.05])
b_pause = Button(ax_pause, 'Pause', color='#0969da', hovercolor='#0a5cc2')
b_pause.label.set_color('white')
ax_reset = fig.add_axes([0.14, 0.22, 0.09, 0.05])
b_reset = Button(ax_reset, 'Reset', color=PANEL)


chamber = FancyBboxPatch((1.6, 1.2), 7.6, 4.2,
                         boxstyle='round,pad=0.25,rounding_size=0.6',
                         fc=CHAMBER, ec='#57606a', lw=1.5)
ax.add_patch(chamber)
ax.text(5.4, 5.15, 'EVACUATED CHAMBER', ha='center', fontsize=8,
        color='#57606a')

cath_x, an_x = 2.6, 8.4
ax.add_patch(Rectangle((cath_x-0.12, 1.8), 0.24, 3.0, fc=PLATE, ec='#57606a'))
ax.add_patch(Rectangle((an_x-0.12, 1.8), 0.24, 3.0, fc=PLATE, ec='#57606a'))
ax.text(cath_x, 1.45, 'CATHODE', ha='center', fontsize=9, weight='bold')
metal_label = ax.text(cath_x, 1.15, 'SODIUM', ha='center', fontsize=7,
                      color='#57606a')
ax.text(an_x, 1.45, 'ANODE', ha='center', fontsize=9, weight='bold')
ax.text(cath_x, 5.0, '+', fontsize=15, ha='center', weight='bold')
ax.text(an_x, 5.0, '−', fontsize=15, ha='center', weight='bold')

ax.add_patch(Polygon([[0.0, 2.8], [0.9, 2.5], [0.9, 3.9], [0.0, 3.6]],
                     fc='#8b949e', ec='#57606a'))
lamp = Circle((0.42, 3.2), 0.26, fc='violet', ec='#57606a', zorder=5)
ax.add_patch(lamp)
ax.text(0.45, 2.1, 'LIGHT', fontsize=9, weight='bold')

ax.plot([cath_x, cath_x, 4.6], [1.8, 0.55, 0.55], color='#57606a', lw=1.5)
ax.plot([an_x, an_x, 6.2], [1.8, 0.55, 0.55], color='#57606a', lw=1.5)
meter = Circle((5.4, 0.55), 0.52, fc='white', ec='#57606a', lw=1.5)
ax.add_patch(meter)
ax.text(5.4, 0.82, 'CURRENT', ha='center', fontsize=6, color='#57606a')
current_txt = ax.text(5.4, 0.42, '0.00', ha='center', fontsize=11,
                      weight='bold', color=GOOD)

banner = ax.text(5.2, -0.35, '', ha='center', fontsize=9, weight='bold')

for s in (s_lam, s_int, s_ret):
    s.valtext.set_visible(False)

readout = {}
for key, ypos in [('W', 0.775), ('lam', 0.585), ('int', 0.475), ('ret', 0.365)]:
    readout[key] = fig.text(0.225, ypos, '', fontsize=8,
                            ha='right', weight='bold',
                            bbox=dict(boxstyle='round,pad=0.25', fc='white',
                                      ec='#d0d7de'))

n_ph = 30
ph_x = np.random.uniform(0.9, cath_x, n_ph)
ph_y = np.random.uniform(2.4, 4.0, n_ph)
n_el = 80
el_x = np.full(n_el, -1.0)
el_y = np.full(n_el, -1.0)
el_v = np.zeros(n_el)
arrivals = []
state = {'paused': False, 'frame': 0}

photons, = ax.plot([], [], 'o', ms=5, color='violet', zorder=6)
electrons, = ax.plot([], [], 'o', ms=5, color='#39c5cf', zorder=6)

def physics():
    W = metals[r_metal.value_selected] * e
    E_ph = h*c/(s_lam.val*1e-9)
    KE = E_ph - W
    return W, E_ph, KE

def refresh_static(_=None):
    W, E_ph, KE = physics()
    colour = wavelength_to_rgb(s_lam.val) if s_lam.val >= 380 else (0.55, 0.2, 0.85)
    lamp.set_facecolor(colour)
    metal_label.set_text(r_metal.value_selected.upper())
    readout['W'].set_text(f'{metals[r_metal.value_selected]:.2f} eV')
    readout['lam'].set_text(f'{s_lam.val:.0f} nm')
    readout['int'].set_text(f'{s_int.val:.0f} %')
    readout['ret'].set_text(f'{s_ret.val:.2f} V')
    fig.canvas.draw_idle()

r_metal.on_clicked(refresh_static)
s_lam.on_changed(refresh_static)
s_int.on_changed(refresh_static)
s_ret.on_changed(refresh_static)

def on_pause(_):
    state['paused'] = not state['paused']
    b_pause.label.set_text('Resume' if state['paused'] else 'Pause')

def on_reset(_):
    s_lam.reset(); s_int.reset(); s_ret.reset()
    el_y[:] = -1

b_pause.on_clicked(on_pause)
b_reset.on_clicked(on_reset)

def update(frame):
    if state['paused']:
        return photons, electrons, current_txt, banner
    state['frame'] += 1
    W, E_ph, KE = physics()
    k = 0.26
    v0 = k*np.sqrt(max(KE, 0)/e)
    gap = an_x - cath_x
    decel = k**2 * s_ret.val / (2*gap)

    rate = s_int.val / 100
    ph_x[:] += 0.13
    hit = ph_x >= cath_x - 0.15
    n_hit = np.sum(hit)
    if n_hit and KE > 0:
        n_new = np.random.binomial(n_hit, min(rate, 1.0))
        free = np.where(el_y < 0)[0][:n_new]
        el_x[free] = cath_x + 0.2
        el_y[free] = np.random.uniform(2.0, 4.6, free.size)
        el_v[free] = v0
    ph_x[hit] = np.random.uniform(0.7, 1.2, n_hit)
    ph_y[hit] = np.random.uniform(2.4, 4.0, n_hit)

    live = el_y > 0
    el_v[live] -= decel
    el_x[live] += np.clip(el_v[live], -0.3, None)
    back = live & (el_x < cath_x + 0.1)
    el_y[back] = -1
    arrived = live & (el_x >= an_x - 0.15)
    arrivals.append(np.sum(arrived))
    el_y[arrived] = -1
    if len(arrivals) > 50:
        arrivals.pop(0)

    n_show = max(2, int(n_ph * rate))
    colour = wavelength_to_rgb(s_lam.val) if s_lam.val >= 380 else (0.55, 0.2, 0.85)
    photons.set_data(ph_x[:n_show], ph_y[:n_show])
    photons.set_color(colour)
    vis = el_y > 0
    electrons.set_data(el_x[vis], el_y[vis])

    current = np.sum(arrivals) / 12
    current_txt.set_text(f'{current:.2f}')
    Vs = max(KE, 0)/e
    if KE <= 0:
        banner.set_text('No photoemission: photon energy below the work function')
        banner.set_color(BAD)
        current_txt.set_color(BAD)
    elif s_ret.val >= Vs:
        banner.set_text(f'Electrons emitted but turned back: V > Vs = {Vs:.2f} V')
        banner.set_color(WARN)
        current_txt.set_color(WARN)
    else:
        banner.set_text('Photoelectrons are reaching the anode')
        banner.set_color(GOOD)
        current_txt.set_color(GOOD)
    return photons, electrons, current_txt, banner

refresh_static()
anim = FuncAnimation(fig, update, frames=100000, interval=40,
                     cache_frame_data=False)
plt.show()
