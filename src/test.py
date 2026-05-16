import numpy as np

mu0 = 4 * np.pi * 1e-7

# -------- Sample --------
R_s = 4e-3
H_s = 24e-3
M = 1.0  # along x

# -------- Coil --------
# R_c = 14e-3
R_c = 24.5e-3
H_c = 75e-3
phi_open = 120 * np.pi / 180
z_offset = 0.0

# -------- Discretization --------
Nr_s, Nphi_s, Nz_s = 15, 30, 30
Nphi_c, Nz_c = 60, 60

# -------- Sample grid (FULL 3D now!) --------
r_s = np.linspace(0, R_s, Nr_s)
phi_s = np.linspace(0, 2 * np.pi, Nphi_s, endpoint=False)
z_s = np.linspace(-H_s / 2, H_s / 2, Nz_s)

dr_s = R_s / Nr_s
dphi_s = 2 * np.pi / Nphi_s
dz_s = H_s / Nz_s

R_sg, Phi_sg, Z_sg = np.meshgrid(r_s, phi_s, z_s, indexing="ij")

# Convert to Cartesian
x_s = (R_sg * np.cos(Phi_sg)).flatten()
y_s = (R_sg * np.sin(Phi_sg)).flatten()
z_s = Z_sg.flatten()

# Volume element
dV = (R_sg * dr_s * dphi_s * dz_s).flatten()

# Dipole moments (Mx)
m_vec = np.zeros((len(dV), 3))
m_vec[:, 0] = M * dV  # along x

# -------- Coil grid --------
phi_c = np.linspace(-phi_open / 2, phi_open / 2, Nphi_c)
z_c = np.linspace(-H_c / 2, H_c / 2, Nz_c)

dphi_c = phi_open / Nphi_c
dz_c = H_c / Nz_c

flux = 0.0

for ph in phi_c:
    cos_ph = np.cos(ph)
    sin_ph = np.sin(ph)

    for z in z_c:
        # Coil point
        x_c = R_c * cos_ph
        y_c = R_c * sin_ph
        z_c_pos = z + z_offset

        # Surface normal (radial)
        n_hat = np.array([cos_ph, sin_ph, 0.0])

        # Vector from source → field point
        rx = x_c - x_s
        ry = y_c - y_s
        rz = z_c_pos - z_s

        r_vec = np.stack((rx, ry, rz), axis=1)
        r_mag = np.linalg.norm(r_vec, axis=1)

        mask = r_mag > 1e-12

        r_hat = np.zeros_like(r_vec)
        r_hat[mask] = r_vec[mask] / r_mag[mask][:, None]

        dot = np.sum(m_vec * r_hat, axis=1)

        B = np.zeros_like(r_vec)
        B[mask] = (mu0 / (4 * np.pi)) * (
            (3 * dot[mask][:, None] * r_hat[mask] - m_vec[mask])
            / r_mag[mask][:, None] ** 3
        )

        # Project onto surface normal
        Bn = np.dot(B, n_hat)

        B_total = np.sum(Bn)

        # Surface element
        dA = R_c * dphi_c * dz_c

        flux += B_total * dA

print("Flux (Wb):", flux)

print("gV:", flux / mu0 / (np.pi * R_s**2 * H_s) / M)
