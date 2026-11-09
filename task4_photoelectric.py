import numpy as np
import matplotlib.pyplot as plt

h = 6.62607015e-34
e = 1.602176634e-19
c = 2.99792458e8

metals = {'caesium': 2.10, 'sodium': 2.28, 'zinc': 4.31,
          'copper': 4.70, 'platinum': 5.65}

f = np.linspace(0, 2.5e15, 1000)

plt.figure(figsize=(9, 5))
for name, W_eV in metals.items():
    W = W_eV * e
    f0 = W / h
    V = (h*f - W) / e
    V[f < f0] = np.nan
    plt.plot(f/1e15, V, label=f'{name} (W = {W_eV} eV)')
    print(f'{name:9s}: cutoff f0 = {f0/1e15:.3f} PHz,  '
          f'cutoff wavelength = {c/f0*1e9:.0f} nm')

fvis = np.array([c/700e-9, c/380e-9])
plt.axvspan(fvis[0]/1e15, fvis[1]/1e15, color='yellow', alpha=0.15,
            label='visible light')

rng = np.random.default_rng(1)
fs = np.linspace(1.5e15, 2.5e15, 12)
Vs_data = (h*fs - metals['platinum']*e) / e + rng.normal(0, 0.05, fs.size)
m_fit, c_fit = np.polyfit(fs, Vs_data, 1)
h_measured = m_fit * e
W_measured = -c_fit
plt.plot(fs/1e15, Vs_data, 'kx', ms=6, label='simulated experiment (platinum)')
plt.plot(fs/1e15, m_fit*fs + c_fit, 'k-', lw=0.8)
print(f'\nsimulated experiment, 12 data points, noise sd = 0.05 V:')
print(f'h from fitted gradient = {h_measured:.4e} J s   '
      f'(true {h:.4e}, error {abs(h_measured-h)/h*100:.2f} %)')
print(f'W from fitted intercept = {W_measured:.2f} eV   '
      f'(true {metals["platinum"]:.2f} eV)')

plt.axhline(0, color='k', lw=0.5)
plt.xlabel('photon frequency f (PHz = 10$^{15}$ Hz)')
plt.ylabel('stopping voltage $V_s$ (V)')
plt.title('Photoelectric effect: $eV_s = hf - W$')
plt.legend()
plt.show()
