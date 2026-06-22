"""
Problem 3: Optimal Transport (English & Arabic Explanation)
============================================================
1. Problem Statement (English):
-------------------------------
Suppose we have piles of raw material at various locations in a worksite. The piles of raw material are given as a list of source coordinates and weights. We need to plan to redistribute this pile to a new configuration (destination coordinates and weights).

We want to compute a transportation plan that minimizes the overall cost of moving raw materials.

Given:
- `source_coords` and `source_weights`: The starting piles.
- `dest_coords` and `dest_weights`: The desired ending piles (sum of source_weights must equal sum of dest_weights).
- `w` units moved over distance `D` costs `w * D`.

Let `x_{i,j}` be the amount of material transported from source `i` to destination `j`.
We wish to minimize the total cost:
    Σ_{i,j} x_{i,j} * D_{i,j}
subject to:
    1. For each source `i`: Σ_{j} x_{i,j} = source_weights[i]
    2. For each destination `j`: Σ_{i} x_{i,j} = dest_weights[j]
    3. x_{i,j} >= 0

================================================================
2. Explanation (Arabic):
------------------------
المسألة بتطلب حساب خطة النقل المثلى (Optimal Transport Plan) لنقل المواد الخام من مواقعها الحالية إلى مواقع جديدة بأقل تكلفة ممكنة.
تكلفة نقل وحدة واحدة لمسافة معينة تساوي الوزن مضروباً في المسافة الإقليدية (Euclidean Distance).

لحل المشكلة، بنستخدم البرمجة الخطية (Linear Programming) من خلال مكتبة `scipy.optimize.linprog`:
1. بنحسب متجه التكلفة `c` لكل زوج (مصدر i, وجهة j) (حجمه `n * m`).
2. نضع قيود التساوي `A_eq * x = b_eq`، بحيث مجموع الصفوف يساوي أوزان المصادر، ومجموع الأعمدة يساوي أوزان الوجهات.
3. نبقي المتغيرات غير سالبة (`bounds=(0, None)`).
4. بما أن الحلول من الـ LP قد تحتوي على أخطاء عائمة (Floating Point Errors) صغيرة جداً، الكود يضيف خطوات إعادة توازن (Proportional Scaling و Exact Margin Adjustment) لضمان أن مجموع الصفوف والأعمدة يطابق الأوزان الأصلية بدقة تامة.

================================================================
3. Code Implementation:
-----------------------
"""

from math import sqrt
from scipy.optimize import linprog

def calculate_distance(a, b):
    (xa, ya) = a
    (xb, yb) = b
    return sqrt((xa - xb)**2 + (ya - yb)**2)

def get_objective(var_values, source_coords, dest_coords):
    """
    Calculates the total cost of the transportation plan.
    var_values: 2D list (n x m) of transported amounts.
    """
    total_cost = 0.0
    n = len(source_coords)
    m = len(dest_coords)
    
    for i in range(n):
        for j in range(m):
            dist = calculate_distance(source_coords[i], dest_coords[j])
            total_cost += var_values[i][j] * dist
            
    return total_cost

def calculate_optimal_transport_plan(source_coords, source_weights, dest_coords, dest_weights):
    n = len(source_coords)
    m = len(dest_coords)

    # Cost vector (row‑major): length n * m
    c = [calculate_distance(source_coords[i], dest_coords[j])
         for i in range(n) for j in range(m)]

    # Equality constraints A_eq @ x = b_eq
    A_eq = []
    b_eq = []

    # Source constraints (rows sum to source_weights[i])
    for i in range(n):
        row = [0] * (n * m)
        for j in range(m):
            row[i * m + j] = 1
        A_eq.append(row)
        b_eq.append(source_weights[i])

    # Destination constraints (columns sum to dest_weights[j])
    for j in range(m):
        row = [0] * (n * m)
        for i in range(n):
            row[i * m + j] = 1
        A_eq.append(row)
        b_eq.append(dest_weights[j])

    bounds = [(0, None)] * (n * m)

    # Solve LP – try 'highs' or fallback to other solvers
    res = None
    for method in ['highs', 'revised simplex', 'simplex', None]:
        try:
            if method is None:
                res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds)
            else:
                res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method=method)
            if res.success:
                break
        except ValueError:
            continue
            
    if res is None or not res.success:
        raise RuntimeError("All LP solvers failed.")

    # Reshape solution into 2D list
    x = res.x
    plan = [[x[i * m + j] for j in range(m)] for i in range(n)]

    # ------------------------------------------------------------------
    # 1. Proportional scaling to get close to exact constraints
    # ------------------------------------------------------------------
    for _ in range(20):
        # Scale rows
        for i in range(n):
            s = sum(plan[i])
            if s > 0:
                factor = source_weights[i] / s
                plan[i] = [v * factor for v in plan[i]]
        # Scale columns
        for j in range(m):
            s = sum(plan[i][j] for i in range(n))
            if s > 0:
                factor = dest_weights[j] / s
                for i in range(n):
                    plan[i][j] *= factor

    # ------------------------------------------------------------------
    # 2. Exact margin adjustment (ensures sums match perfectly)
    # ------------------------------------------------------------------
    for _ in range(100):
        max_err = 0.0
        # Fix rows
        for i in range(n):
            s = sum(plan[i])
            err = source_weights[i] - s
            if abs(err) > 1e-12:
                max_err = max(max_err, abs(err))
                # Add the error to the largest element of this row
                j_max = max(range(m), key=lambda j: plan[i][j])
                plan[i][j_max] += err
        # Fix columns
        for j in range(m):
            s = sum(plan[i][j] for i in range(n))
            err = dest_weights[j] - s
            if abs(err) > 1e-12:
                max_err = max(max_err, abs(err))
                i_max = max(range(n), key=lambda i: plan[i][j])
                plan[i_max][j] += err
        if max_err < 1e-12:
            break

    return plan 

"""
================================================================
4. Time & Space Complexity Analysis:
------------------------------------
- Building the linear programming model:
    - Time: O(n * m) to construct the cost vector `c` and constraint matrix `A_eq`.
    - Space: O(n * m) to store the matrix and arrays.
- Solving the LP:
    - The internal solver (e.g., 'highs' or 'simplex') runs in polynomial time in practice. For a problem with `n*m` variables and `n+m` constraints, it is highly efficient.
- Rebalancing steps: O(iterations * (n*m)) where iterations is a constant (20 for scaling, 100 for adjustment).
================================================================
"""

# ------------------- Test Cases -------------------
if __name__ == "__main__":
    # Test 1: 10 points
    source_coords = [(1,5), (4,1), (5,5)]
    source_weights = [9, 4, 5]
    dest_coords = [(2,2), (6,6)]
    dest_weights = [9, 9]
    n = 3; m = 2

    var_values = calculate_optimal_transport_plan(source_coords, source_weights, dest_coords, dest_weights)
    obj_val = get_objective(var_values, source_coords, dest_coords)
    print(f'Test 1 Objective value: {obj_val}')

    for i in range(n):
        assert (sum(var_values[i][j] for j in range(m)) == source_weights[i])
    for j in range(m):
        assert (sum(var_values[i][j] for i in range(n)) == dest_weights[j])

    assert(abs(obj_val - 52.22) <= 1E-01)
    print('Test 1 Passed: 10 points\n')


    # Test 2: 8 points
    source_coords = [(1,1), (2,2), (3,3), (4, 4), (5,5), (6,6)]
    source_weights = [10, 10, 10, 10, 10, 10]
    dest_coords = [(6,1), (5, 2), (4,3), (3,2), (2,1)]
    dest_weights = [12, 12, 12, 12, 12]
    n = 6; m = 5

    var_values = calculate_optimal_transport_plan(source_coords, source_weights, dest_coords, dest_weights)
    obj_val = get_objective(var_values, source_coords, dest_coords)
    print(f'Test 2 Objective value: {obj_val}')

    for i in range(n):
        assert (sum(var_values[i][j] for j in range(m)) == source_weights[i])
    for j in range(m):
        assert (sum(var_values[i][j] for i in range(n)) == dest_weights[j])

    assert(abs(obj_val - 127.19) <= 1E-1)
    print('Test 2 Passed: 8 points\n')


    # Test 3: 5 points
    source_coords = [(i,1) for i in range(20)]
    source_weights = [10] * 20
    dest_coords = [(6,i+5) for i in range(8)] + [(14,i+5) for i in range(8)]
    dest_weights = [12.5]*16
    n = 20; m = 16

    var_values = calculate_optimal_transport_plan(source_coords, source_weights, dest_coords, dest_weights)
    obj_val = get_objective(var_values, source_coords, dest_coords)
    print(f'Test 3 Objective value: {obj_val}')

    for i in range(n):
        assert (sum(var_values[i][j] for j in range(m)) == source_weights[i])
    for j in range(m):
        assert (sum(var_values[i][j] for i in range(n)) == dest_weights[j])

    assert(abs(obj_val - 1598.11) <= 1E-1)
    print('Test 3 Passed: 5 points\n')

    print("All tests passed successfully!")
