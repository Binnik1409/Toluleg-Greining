import numpy as np
import matplotlib.pyplot as plt
import functions as f

ROUND = 2
TOL = 10**(-3)

def make_grid(R_low, R_high, I_low, I_high, N):
    # Fully vectorized grid construction
    r = np.linspace(R_low, R_high, N)
    i = np.linspace(I_low, I_high, N)
    R, I = np.meshgrid(r, i, indexing="ij")
    return R + 1j * I   # shape (N, N), complex

# Build grid as a NumPy array
grid = make_grid(-8, -6, -1, 1, 2000)

# Compute Newton results with one flat list comprehension
flat_grid = grid.ravel()
flat_results = np.array([f.newton(z, TOL, f.f, f.Df) for z in flat_grid],
                        dtype=complex)
results = flat_results.reshape(grid.shape)

# Round results and find unique solutions + color indices in one go
rounded = np.round(results, ROUND)
four_solutions, color_indices = np.unique(rounded, return_inverse=True)

# Optionally enforce that there are exactly 4 distinct roots
if len(four_solutions) != 4:
    raise RuntimeError(f"Expected 4 solutions, got {len(four_solutions)}")

# Reshape color indices back to grid shape
color_indices = color_indices.reshape(grid.shape)

colors = ["blue", "green", "red", "black"]

plt.figure()
for idx, root in enumerate(four_solutions):
    mask = (color_indices == idx)
    # Use masks directly, no Python-level grouping
    plt.scatter(
        grid.real[mask],
        grid.imag[mask],
        s=10,
        marker='s',
        linewidths=0,
        color=colors[idx],
        label=root
    )

plt.gca().set_aspect('equal', adjustable='box')
plt.axis('on')
plt.grid(False)
plt.legend()
plt.show()
