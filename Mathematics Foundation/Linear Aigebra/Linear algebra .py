#!/usr/bin/env python3
"""
MIT Linear Algebra - Lectures 1 & 2
Author: Joesph Solomon (example)
Practical Python for understanding A·x = b and Gaussian Elimination
"""

import numpy as np

# ------------------------------
# Lecture 1: The Geometry of Linear Equations
# ------------------------------

# Example: Solve system of equations
#   x + 2y = 4
#   3x + 8y = 18

A = np.array([[1, 2],
              [3, 8]])
b = np.array([4, 18])

# Solve system A·x = b
x = np.linalg.solve(A, b)

print("=== Lecture 1 — Geometry of Linear Equations ===")
print("Matrix A:\n", A)
print("Vector b:", b)
print("Solution x:", x)
print("Check (A·x):", A @ x)  # verify A·x = b

# ------------------------------
# Lecture 2: Elimination and Matrix Multiplication
# ------------------------------

print("\n=== Lecture 2 — Elimination and Matrix Multiplication ===")

# Step 1: Forward elimination manually
A2 = np.array([[2, 1, -1],
               [-3, -1, 2],
               [-2, 1, 2]], dtype=float)
b2 = np.array([8, -11, -3], dtype=float)

print("Original System:")
print("A =\n", A2)
print("b =", b2)

# Gaussian Elimination manually
n = len(b2)
for i in range(n):
    # Normalize the pivot
    pivot = A2[i, i]
    A2[i] = A2[i] / pivot
    b2[i] = b2[i] / pivot

    # Eliminate below
    for j in range(i + 1, n):
        factor = A2[j, i]
        A2[j] = A2[j] - factor * A2[i]
        b2[j] = b2[j] - factor * b2[i]

print("\nAfter Forward Elimination:")
print("A =\n", A2)
print("b =", b2)

# Step 2: Back substitution
x2 = np.zeros(n)
for i in range(n - 1, -1, -1):
    x2[i] = b2[i] - np.dot(A2[i, i + 1:], x2[i + 1:])

print("\nSolution (by elimination):", x2)

# Step 3: Compare with numpy solution
x_check = np.linalg.solve(np.array([[2, 1, -1],
                                    [-3, -1, 2],
                                    [-2, 1, 2]]), np.array([8, -11, -3]))
print("Solution (by numpy.linalg.solve):", x_check)

# Step 4: Matrix multiplication verification
A3 = np.array([[1, 2],
               [0, 3]])
B3 = np.array([[4, 1],
               [2, 2]])
C3 = A3 @ B3
print("\nMatrix Multiplication Example:")
print("A =\n", A3)
print("B =\n", B3)
print("A·B =\n", C3)
