"""
Solutions: Chapters 1-5 (Python from zero)
Run this file to see all answers with explanations.
"""

print("=" * 60)
print("CHAPTER 1 - Setup and first program")
print("=" * 60)

# 1.1
print("Hakeem")
print(2026)

# 1.2  Use single quotes outside so double quotes can sit inside
print('He said "quantum"')

# 1.3
print(7 / 2)    # 3.5   true division, always float
print(7 // 2)   # 3     floor division, throws away remainder
print(7 % 2)    # 1     modulo, the remainder itself

# 1.4  Deleting a closing bracket makes Python blame the NEXT line,
#      because it keeps reading, hoping the expression will finish.

# 1.5
print(2 ** 10)  # 1024  -- ** is "to the power of"


print("\n" + "=" * 60)
print("CHAPTER 2 - Variables and types")
print("=" * 60)

h = 6.62607015e-34
e = 1.602176634e-19
me = 9.1093837015e-31
c = 2.99792458e8

# 2.1
print(f"h  = {h:.4e} J s")
print(f"e  = {e:.4e} C")
print(f"me = {me:.4e} kg")

# 2.2
lam = 486.1e-9
E_joules = h * c / lam
E_eV = E_joules / e
print(f"photon energy = {E_joules:.4e} J = {E_eV:.2f} eV")

# 2.3
print(10 % 3)    # 1
print(10 // 3)   # 3
print(-7 // 2)   # -4  (floors DOWNWARD, not toward zero)

# 2.4
print(0.1 + 0.2 == 0.3)                 # False
print(abs((0.1 + 0.2) - 0.3) < 1e-9)    # True - the correct way

# 2.5
kB = 1.380649e-23
T = 5778
correct = h * c / (lam * kB * T)
wrong = h * c / lam * kB * T
print(f"correct = {correct:.4e}, wrong = {wrong:.4e}")
print(f"ratio = {wrong/correct:.4e}  (wrong by a factor of (kB*T)^2)")

# 2.6
lam_nm = 656.3
E = 1.89
print(f"lambda = {lam_nm} nm  |  E = {E} eV")


print("\n" + "=" * 60)
print("CHAPTER 3 - Decisions and loops")
print("=" * 60)

# 3.1
for i in range(1, 11):
    print(i**2, end=' ')
print()

# 3.2
metals = {'caesium': 2.10, 'sodium': 2.28, 'zinc': 4.31, 'copper': 4.70}
photon_500nm = 1240 / 500          # eV, using the E(eV)=1240/lambda(nm) shortcut
for name, W in metals.items():
    if photon_500nm > W:
        print(f"{name}: emits ({photon_500nm:.2f} eV > {W} eV)")
    else:
        print(f"{name}: no emission ({photon_500nm:.2f} eV < {W} eV)")

# 3.3
print("\nMultiplication table:")
for i in range(1, 6):
    for j in range(1, 6):
        print(f"{i*j:>4}", end='')
    print()

# 3.4
print("\nHydrogen transitions:")
for n1 in range(1, 4):
    for n2 in range(n1+1, n1+5):
        E = 13.6 * (1/n1**2 - 1/n2**2)
        print(f"  n={n2} -> n={n1}: {E:.3f} eV")

# 3.5  Un-indenting the print moves it outside the inner loop, so it only
#      runs once per outer iteration, printing the LAST value each time.

# 3.6
n = 1
while n**2 <= 10000:
    n += 1
print(f"\nsmallest n with n^2 > 10000: {n}")


print("\n" + "=" * 60)
print("CHAPTER 4 - Lists and collections")
print("=" * 60)

# 4.1
balmer = [656.3, 486.1, 434.0, 410.2, 397.0, 388.9]
print("first:", balmer[0], " last:", balmer[-1], " middle two:", balmer[2:4])

# 4.2
squares = []
for i in range(1, 6):
    squares.append(i**2)
print("squares:", squares)

# 4.3
for name, W in metals.items():
    print(f"{name:9s} cutoff = {1240/W:.0f} nm")

# 4.4
data = [3, 8, 2, 9, 4]
print(f"len={len(data)} sum={sum(data)} mean={sum(data)/len(data):.1f} "
      f"max={max(data)} min={min(data)}")

# 4.5
a = [1, 2, 3]
b = a
b[0] = 99
print("shared:", a[0])        # 99 - b is the SAME list
a = [1, 2, 3]
b = a.copy()
b[0] = 99
print("copied:", a[0])        # 1 - now independent

# 4.6
orbitals = [(1, 0, 0), (2, 1, 0), (3, 2, 1)]
for n, l, m in orbitals:
    print(f"n={n} l={l} m={m}, sum={n+l+m}")


print("\n" + "=" * 60)
print("CHAPTER 5 - Functions")
print("=" * 60)

import numpy as np

# 5.1
def de_broglie(V):
    """Electron de Broglie wavelength (m) for accelerating voltage V (volts)."""
    return h / np.sqrt(2 * me * e * V)

print(f"de Broglie at 1000 V = {de_broglie(1000):.3e} m")

# 5.2
def bohr_energy(n):
    """Hydrogen energy level n, in eV."""
    return -13.6 / n**2

for n in range(1, 6):
    print(f"  E{n} = {bohr_energy(n):.3f} eV")

# 5.3
def transition(n1, n2):
    """Return (photon energy in eV, wavelength in nm) for n2 -> n1."""
    E_eV = 13.606 * (1/n1**2 - 1/n2**2)
    lam_nm = 1239.84 / E_eV
    return E_eV, lam_nm

E, lam = transition(2, 3)
print(f"n=3 -> 2: {E:.3f} eV, {lam:.1f} nm")

# 5.4  Code after 'return' never runs - return exits the function immediately.
def demo():
    return 42
    print("never printed")
print("demo() =", demo())

# 5.5
def escape_velocity(M, R, G=6.674e-11):
    return np.sqrt(2*G*M/R)

print(f"Earth escape velocity = {escape_velocity(5.972e24, 6.371e6):.0f} m/s")

# 5.6  Two fixes for the counter problem
count = 0
def increment_global():
    global count
    count += 1
increment_global()
print("with global:", count)

def increment_pure(c):
    return c + 1
count2 = increment_pure(0)
print("by returning:", count2)
print("The returning version is cleaner: no hidden state, easy to test.")
