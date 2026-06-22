"""
Problem 2: k-Centers Clustering Problem (English & Arabic Explanation)
=======================================================================
1. Problem Statement (English):
-------------------------------
You are given a set of points P1, ..., Pn on a plane where for each point Pi we provide its coordinates (xi, yi). The goal is to select k points out of n as centers. Once we select k centers C1, ..., Ck from among the points P1, ..., Pn, we define for every point Pi the distance ri as the distance from Pi to its nearest center.

Having chosen k centers C1, ..., Ck, we define R(C1, ..., Ck) = max(r1, ..., rn) as the maximum distance from any point to its nearest center. It is clear then that if we placed a circle of radius R(C1, ..., Ck) around every center, then all points belong to the circle.

Our goal is to choose k centers such that we minimize the value of R as defined above.

=======================================================================
2. Explanation (Arabic):
------------------------
المسألة تطلب اختيار `k` من النقاط لتكون "مراكز" (Centers) بحيث تكون أقصى مسافة بين أي نقطة وأقرب مركز لها هي أقل ما يمكن (نقلل قيمة `R`).

الخوارزمية المستخدمة هنا هي خوارزمية **جشعة (Greedy Algorithm)**:
1. نبدأ باختيار أول نقطة في القائمة كمركز أول.
2. في كل خطوة تالية، نبحث عن النقطة الأبعد عن جميع المراكز التي تم اختيارها حالياً.
3. نضيف هذه النقطة الأبعد كمركز جديد.
4. نكرر العملية حتى نختار `k` من المراكز.

هذه الخوارزمية تعطي حلاً تقريبياً (2-Approximation) لمشكلة الـ k-Centers، وهي معروفة بكفاءتها وسهولة تنفيذها.

=======================================================================
3. Code Implementation:
-----------------------
"""

from math import sqrt
from matplotlib import pyplot as plt

def euclidean_distance(a, b):
    (xa, ya) = a
    (xb, yb) = b
    return sqrt((xb - xa)**2 + (yb - ya)**2)

def calculate_R(coords, center_indices):
    """
    Calculate the maximum distance R from any point to its nearest center.
    """
    n = len(coords)
    assert all(0 <= j < n for j in center_indices)
    # For each point, find the distance to its nearest center
    rj_values = [min([euclidean_distance(xj, coords[j]) for j in center_indices]) for xj in coords]
    return max(rj_values)

def plot_coords(coords, center_indices):
    """
    Plot the points and the selected centers with circles of radius R.
    """
    R = calculate_R(coords, center_indices)
    coords_x = [x for (x, y) in coords]
    coords_y = [y for (x, y) in coords]
    centers_x = [coords_x[j] for j in center_indices]
    centers_y = [coords_y[j] for j in center_indices]
    
    figure, axes = plt.subplots()
    axes.axis('equal')
    for k in center_indices:
        c = plt.Circle(coords[k], R, fill=True, alpha=0.5, facecolor='lightblue', 
                       clip_on=False, edgecolor='black', linewidth=1, linestyle='dashed')
        axes.add_artist(c)
    plt.scatter(coords_x, coords_y, s=30, marker='x', label='Points')
    plt.scatter(centers_x, centers_y, s=50, marker='o', color='red', label='Centers')
    plt.legend()
    plt.show()

def find_farthest_point_from_current_centers(coords, center_indices):
    """
    Find the index of the point that is farthest from its nearest center.
    """
    n = len(coords)
    assert all(0 <= j < n for j in center_indices)
    # For each point, compute distance to its nearest center
    rj_values = [(min([euclidean_distance(xi, coords[j]) for j in center_indices]), i) for (i, xi) in enumerate(coords)]
    (rj, j) = max(rj_values)
    return (j, rj)

def greedy_k_centers(coords, k, debug=True):
    """
    Greedy k-centers algorithm.
    
    Args:
        coords: list of (x, y) coordinate tuples.
        k: number of centers to select.
        debug: if True, prints progress messages.
    
    Returns:
        (centers_list, R) where
            - centers_list is a list of indices of the chosen centers,
            - R is the maximum distance from any point to its nearest center.
    """
    n = len(coords)
    assert n > 0, "coords must not be empty"
    # Start with the first point as the initial center
    centers = [0]
    if debug:
        print(f'Initial center: {coords[0]}')
    
    # Greedily add the farthest point from current centers until we have k centers
    while len(centers) < k:
        j, rj = find_farthest_point_from_current_centers(coords, centers)
        centers.append(j)
        if debug:
            print(f'Adding center: {coords[j]} (distance {rj:.4f})')
    
    # Compute the final radius after all k centers are placed
    _, R = find_farthest_point_from_current_centers(coords, centers)
    return centers, R

"""
=======================================================================
4. Time & Space Complexity Analysis:
------------------------------------
- Time Complexity: O(k * n)
  - في كل خطوة من خطوات الخوارزمية (k-1 خطوة)، نستدعي `find_farthest_point_from_current_centers` التي تقوم بالمرور على جميع النقاط `n` مرة واحدة لحساب المسافات وإيجاد النقطة الأبعد. وبما أننا نختار k مركز، فإن التعقيد الزمني الكلي هو O(k * n).

- Space Complexity: O(n)
  لتخزين قائمة الإحداثيات والمصفوفات المساعدة.
=======================================================================
"""

# ------------------- Test Cases -------------------
if __name__ == "__main__":
    # Test Case 1 (5 points)
    coords_1 = [(1,2), (3,5), (4,7), (8, 14), (9,3), (7,7), (6,5), (4, 6), (5,2), (1,8)]
    (center_indices_1, R1) = greedy_k_centers(coords_1, 2)
    print(f"Selected centers (k=2): {center_indices_1}")
    plot_coords(coords_1, center_indices_1)
    
    assert len(center_indices_1) == 2
    assert abs(R1 - calculate_R(coords_1, center_indices_1)) <= 1E-06, f'The returned value of R={R1} does not match the calculation'
    assert 4 <= R1 <= 16.2
    print('Test Case 1 Passed (5 points)\n')

    # Test Case 2 (5 points)
    (center_indices_2, R2) = greedy_k_centers(coords_1, 3)
    print(f"Selected centers (k=3): {center_indices_2}")
    plot_coords(coords_1, center_indices_2)
    
    assert len(center_indices_2) == 3
    assert abs(R2 - calculate_R(coords_1, center_indices_2)) <= 1E-06
    assert 3 <= R2 <= 12.0
    print('Test Case 2 Passed (5 points)\n')

    # Test Case 3 (5 points)
    from random import uniform
    n = 1000
    k = 12
    coords_3 = [(uniform(-2,-1), uniform(-2,2)) for i in range(n//4)] + \
               [(uniform(-1,1), uniform(-1,1)) for i in range(n//4)] + \
               [(uniform(1,2), uniform(-2,0)) for i in range(n//4)] + \
               [(uniform(1,2), uniform(0,2)) for i in range(n//4)]
    
    (center_indices_3, R3) = greedy_k_centers(coords_3, k, debug=False)
    plot_coords(coords_3, center_indices_3)
    
    assert len(center_indices_3) == k
    assert abs(R3 - calculate_R(coords_3, center_indices_3)) <= 1E-06
    print('Test Case 3 Passed (5 points)')
    
    print("All Tests Passed Successfully!")
