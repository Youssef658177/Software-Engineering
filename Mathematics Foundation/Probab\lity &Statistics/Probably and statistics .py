import numpy as np
import pandas as pd

# 1. Create a NumPy array for the student scores
scores_array = np.array([85, 92, 78, 90, 88, 75, 95, 80, 88, 91])

# 2. Convert the NumPy array to a Pandas Series for easy statistical calculation
scores_series = pd.Series(scores_array)

print("--- Descriptive Statistics for Student Scores ---")
print(f"Dataset (Scores): {scores_array.tolist()}")

# Calculate the descriptive statistics
mean_score = scores_series.mean()
median_score = scores_series.median()
mode_scores = scores_series.mode()
std_dev = scores_series.std()

# 3. Print the results
print("-" * 40)
print(f"الوسط (Mean Score): {mean_score:.2f}")
print(f"الوسيط (Median Score): {median_score:.2f}")
print(f"الانحراف المعياري (Standard Deviation): {std_dev:.2f}")

# Mode can return multiple values if they are equally frequent
print(f"الوضع (Mode Scores):")
for mode in mode_scores:
    print(f"  - {mode}")
