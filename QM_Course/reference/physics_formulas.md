# Physics formula sheet

Every equation used in the project, with symbols and the chapter that derives it.

## Constants (SI)

| Symbol | Value | Name |
|---|---|---|
| h | 6.62607015 × 10⁻³⁴ J s | Planck constant |
| ħ | 1.054571817 × 10⁻³⁴ J s | reduced Planck, h/2π |
| c | 2.99792458 × 10⁸ m s⁻¹ | speed of light |
| e | 1.602176634 × 10⁻¹⁹ C | elementary charge |
| mₑ | 9.1093837 × 10⁻³¹ kg | electron mass |
| m_p | 1.6726219 × 10⁻²⁷ kg | proton mass |
| k_B | 1.380649 × 10⁻²³ J K⁻¹ | Boltzmann constant |
| R | 8.314462618 J K⁻¹ mol⁻¹ | molar gas constant |
| ε₀ | 8.8541878128 × 10⁻¹² F m⁻¹ | permittivity of free space |
| a₀ | 5.29177 × 10⁻¹¹ m | Bohr radius |
| b | 2.897771955 × 10⁻³ m K | Wien displacement constant |
| λ_C | 2.42631 × 10⁻¹² m | Compton wavelength, h/mₑc |

Useful: 1 eV = 1.602 × 10⁻¹⁹ J; E(eV) = 1240/λ(nm)

---

## Random walks (Ch 9)

Step: Δx = s cos θ, Δy = s sin θ, θ ~ U[0, 2π)

Mean squared displacement: **⟨R²⟩ = N s²**  →  R_rms = s√N

Mean displacement: ⟨R⟩ = (√π/2)·s√(N)/… ≈ 0.886 s√N

Rayleigh distribution: P(R) = (R/σ²)exp(−R²/2σ²), σ² = Ns²/2

## Brownian motion (Ch 10)

Momentum conservation: m u + M V = m u′ + M V′

Kick per collision: ΔV ≈ (m/M) u, directed along −û (Newton's 3rd law)

Unit vector: û = (**p** − **b**)/|**p** − **b**|

Langevin: M dV/dt = −γV + F_random(t)

Einstein diffusion (2D): **⟨|R(t) − R(0)|²⟩ = 4Dt**

## Black body (Ch 11)

Planck: **B(λ,T) = (2hc²/λ⁵)/(e^{hc/λk_BT} − 1)**

Rayleigh–Jeans (classical): B = 2ck_BT/λ⁴ (diverges as λ→0)

Wien: **λ_max T = b = 2.898 × 10⁻³ m K**

Stefan–Boltzmann: total ∝ T⁴

Einstein heat capacity: **C = 3R(θ_E/T)² e^{θ_E/T}/(e^{θ_E/T} − 1)²**

Dulong–Petit limit: C → 3R ≈ 24.9 J K⁻¹ mol⁻¹

Einstein temperatures: lead 67 K, gold 121 K, copper 245 K, iron 350 K

## Photoelectric effect (Ch 12)

**KE_max = hf − W**   **V_s = (hf − W)/e**

Threshold: f₀ = W/h, λ₀ = hc/W

Graph V_s vs f: gradient h/e, x-intercept f₀, y-intercept −W/e

Work functions (eV): caesium 2.10, sodium 2.28, potassium 2.30, silver 4.26,
zinc 4.31, copper 4.70, gold 5.10, platinum 5.65

## Hydrogen (Ch 13)

Bohr radius: a₀ = 4πε₀ħ²/mₑe²

Energy levels: **Eₙ = −mₑe⁴/(8ε₀²h²n²) = −13.606 eV/n²**  (×Z² for hydrogenic)

Transition: **E = E₀(1/n₁² − 1/n₂²)**,  λ = hc/E

Series: n₁ = 1 Lyman (UV), 2 Balmer (visible), 3 Paschen, 4 Brackett, 5 Pfund

Series limit: E = E₀/n₁²

Balmer lab values (nm): 656.3 (Hα), 486.1 (Hβ), 434.0 (Hγ), 410.2 (Hδ)

Reduced mass correction: μ = mₑm_p/(mₑ + m_p) ≈ 0.99946 mₑ

## Electron diffraction (Ch 14)

De Broglie: **λ = h/p**

Accelerated electron: **λ = h/√(2mₑeV)** ≈ 1.226/√V nm (V in volts)

Bragg: **2d sin θ = nλ**

Ring radius on spherical screen: **x = r sin 2θ**, r = 65 mm

Linearised check: 1/√V ∝ sin θ, gradient = 2d√(2mₑe)/h

Graphite spacings: 0.213 nm and 0.123 nm (smaller d → outer ring)

## Particle in a box (Ch 15)

Schrödinger: −(ħ²/2m)ψ″ + Vψ = Eψ

**ψₙ(x) = √(2/a) sin(nπx/a)**   **Eₙ = n²h²/(8ma²)**

Nodes: n−1 inside the box. Zero-point energy: E₁ ≠ 0.

Δx = a√(1/12 − 1/(2n²π²)),  Δp = nπħ/a

**Δx·Δp ≥ ħ/2**; ground state gives 0.5678 ħ = ½√(π²/3 − 2)·… ≈ 0.568 ħ

## Quantum cryptography (Ch 16)

Malus: P(X) = cos²θ, P(Y) = sin²θ

Classical: **P(mismatch) = 1 − cos²θcos²φ − sin²θsin²φ**

Quantum: **P(mismatch) = sin²(φ − θ)**

CHSH bound: classical S ≤ 2, quantum S ≤ 2√2 ≈ 2.83

## Compton scattering (Ch 17)

**λ′ − λ = (h/mₑc)(1 − cos θ) = λ_C(1 − cos θ)**

Max shift at θ = 180°: 2λ_C = 4.85 pm

Electron KE: K = hc/λ − hc/λ′

Relativistic: γ = 1 + K/mₑc²,  **v = c√(1 − 1/γ²)**

Recoil angle: tan φ = (sin θ/λ′)/(1/λ − cos θ/λ′)

Checks: at 511 keV, max Δλ/λ = 2.0000 and max v = 0.800c

## Hydrogenic orbitals (Ch 18)

**ψ_{nlm} = R_{nl}(r) Y_l^m(θ,φ)**

R_{nl}(r) = √[(2Z/na₀)³(n−l−1)!/(2n(n+l)!)] e^{−ρ/2} ρ^l L_{n−l−1}^{2l+1}(ρ),
ρ = 2Zr/na₀

Y_l^m = √[(2l+1)(l−m)!/(4π(l+m)!)] P_l^m(cos θ) e^{imφ}

Quantum numbers: n ≥ 1; l = 0…n−1; m = −l…+l

Nodes: radial n−l−1, angular l, total n−1

Checks: **∫|ψ|²dV = 1**,  **⟨r⟩ = (a₀/2)[3n² − l(l+1)]**,
1s radial probability peaks at a₀

Laguerre recurrence: (i+1)L_{i+1}^α = (2i+1+α−x)L_i^α − (i+α)L_{i−1}^α

Legendre recurrence: (l−m)P_l^m = x(2l−1)P_{l−1}^m − (l+m−1)P_{l−2}^m

LCAO (H₂⁺): ψ_± = N_±(ψ_A ± ψ_B), overlap S = e^{−R}(1 + R + R²/3),
N_± = 1/√(2 ± 2S)

## Colour (Ch 21)

Tristimulus: X = ∫I(λ)x̄(λ)dλ, similarly Y, Z

sRGB gamma: C′ = 1.055 C^{1/2.4} − 0.055 (C > 0.0031308), else 12.92C
