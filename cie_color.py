import numpy as np

def cie_xyz_bar(lam_nm):
    def g(x, mu, s1, s2):
        s = np.where(x < mu, s1, s2)
        return np.exp(-0.5*((x - mu)/s)**2)
    l = np.asarray(lam_nm, dtype=float)
    xbar = (1.056*g(l, 599.8, 37.9, 31.0) + 0.362*g(l, 442.0, 16.0, 26.7)
            - 0.065*g(l, 501.1, 20.4, 26.2))
    ybar = 0.821*g(l, 568.8, 46.9, 40.5) + 0.286*g(l, 530.9, 16.3, 31.1)
    zbar = 1.217*g(l, 437.0, 11.8, 36.0) + 0.681*g(l, 459.0, 26.0, 13.8)
    return xbar, ybar, zbar

XYZ_TO_RGB = np.array([[ 3.2406, -1.5372, -0.4986],
                       [-0.9689,  1.8758,  0.0415],
                       [ 0.0557, -0.2040,  1.0570]])

def xyz_to_srgb(X, Y, Z):
    rgb = XYZ_TO_RGB @ np.array([X, Y, Z])
    rgb = np.clip(rgb, 0, None)
    if rgb.max() > 0:
        rgb = rgb / rgb.max()
    rgb = np.where(rgb <= 0.0031308, 12.92*rgb,
                   1.055*rgb**(1/2.4) - 0.055)
    return np.clip(rgb, 0, 1)

def wavelength_to_rgb(lam_nm, brightness=1.0):
    xbar, ybar, zbar = cie_xyz_bar(lam_nm)
    rgb = xyz_to_srgb(float(xbar), float(ybar), float(zbar))
    fade = 1.0
    if lam_nm < 420:
        fade = max(0.25, (lam_nm - 380)/40)
    elif lam_nm > 660:
        fade = max(0.25, (740 - lam_nm)/80)
    return tuple(np.clip(rgb * brightness * fade, 0, 1))

def spectrum_to_rgb(lam_nm, intensity):
    xbar, ybar, zbar = cie_xyz_bar(lam_nm)
    X = np.trapezoid(intensity*xbar, lam_nm)
    Y = np.trapezoid(intensity*ybar, lam_nm)
    Z = np.trapezoid(intensity*zbar, lam_nm)
    return tuple(xyz_to_srgb(X, Y, Z))

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(9, 2.2))
    lams = np.linspace(380, 740, 361)
    for lam in lams:
        ax.axvline(lam, color=wavelength_to_rgb(lam), lw=3)
    ax.set_xlim(380, 740)
    ax.set_yticks([])
    ax.set_xlabel('wavelength (nm)')
    ax.set_title('CIE 1931 wavelength -> sRGB engine (Wyman et al. fit)')
    plt.tight_layout()
    plt.show()
