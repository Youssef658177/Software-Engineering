# Linear Algebra — Full Practical Course (Python Version)
# Covers: vectors, matrices, linear systems, decompositions, eigenvalues, SVD

import numpy as np
import matplotlib.pyplot as plt

# --- 1. Vectors ---
v = np.array([2, 3])
w = np.array([-1, 4])
print("Vectors:\nv =", v, "\nw =", w)
print("v + w =", v + w)
print("3 * v =", 3 * v)
print("dot(v, w) =", np.dot(v, w))
print("||v|| =", np.linalg.norm(v))

# --- 2. Projection & Angle ---
proj_v_on_w = (np.dot(v, w) / np.dot(w, w)) * w
cos_theta = np.dot(v, w) / (np.linalg.norm(v) * np.linalg.norm(w))
angle_deg = np.degrees(np.arccos(np.clip(cos_theta, -1, 1)))
print("Projection of v on w =", proj_v_on_w)
print("Angle between v and w =", angle_deg, "degrees")

# --- 3. Matrices ---
A = np.array([[1, 2], [3, 4]])
B = np.array([[2, 0], [1, 3]])
print("\nMatrix A:\n", A)
print("Matrix B:\n", B)
print("A @ B =\n", A @ B)
print("det(A) =", np.linalg.det(A))
print("A inverse =\n", np.linalg.inv(A))
print("A.T =\n", A.T)

# --- 4. Solve Ax = b ---
b = np.array([5, 11])
x = np.linalg.solve(A, b)
print("\nSolve A x = b, with b =", b)
print("x =", x)
print("Check A @ x =", A @ x)

# --- 5. Eigenvalues & Eigenvectors ---
eigvals, eigvecs = np.linalg.eig(A)
print("\nEigenvalues:", eigvals)
print("Eigenvectors:\n", eigvecs)

# --- 6. Matrix Decompositions ---
U, S, VT = np.linalg.svd(A)
print("\nSVD:")
print("U =\n", U)
print("S =", S)
print("VT =\n", VT)

Q, R = np.linalg.qr(A)
print("\nQR decomposition:")
print("Q =\n", Q)
print("R =\n", R)

L, U = np.tril(A), np.triu(A)
print("\nLU form (approx):\nL =\n", L, "\nU =\n", U)

# --- 7. Random 3x3 Example ---
M = np.random.randint(1, 5, (3, 3))
print("\nRandom 3x3 Matrix:\n", M)
print("det(M) =", np.linalg.det(M))
print("rank(M) =", np.linalg.matrix_rank(M))

# --- 8. Visualization (2D vectors) ---
plt.figure(figsize=(5,5))
plt.axhline(0, color='gray')
plt.axvline(0, color='gray')
plt.quiver(0, 0, v[0], v[1], angles='xy', scale_units='xy', scale=1, color='b', label='v')
plt.quiver(0, 0, w[0], w[1], angles='xy', scale_units='xy', scale=1, color='r', label='w')
plt.quiver(0, 0, proj_v_on_w[0], proj_v_on_w[1], angles='xy', scale_units='xy', scale=1, color='g', label='proj_v_on_w')
plt.legend()
plt.axis('equal')
plt.grid(True)
plt.title("v, w and projection of v on w")
plt.show()

print("\n--- END OF COURSE ---")
