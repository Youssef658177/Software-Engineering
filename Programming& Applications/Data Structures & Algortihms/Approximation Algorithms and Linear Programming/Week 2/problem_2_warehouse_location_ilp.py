"""
Problem 2: Warehouse Location (Facility Location Problem) - English & Arabic Explanation
========================================================================================
1. Problem Statement (English):
-------------------------------
Imagine you are operating grocery stores across the country with n store locations numbered 0, ..., n-1. Each location i has coordinates (x_i, y_i). The travel distance between locations i and j is given by the Euclidean distance d_{i,j}.

You are asked to locate warehouses among these n locations so that for each location j, the distance to the closest warehouse is less than some specified limit R >= 0. Your goal is to minimize the number of warehouses, as they are expensive to create and operate.

Given:
- A list of coordinates of the locations: [(x0, y0), ..., (x_{n-1}, y_{n-1})]
- The acceptable distance limit R > 0

Formulate an Integer Linear Program (ILP) to solve this problem.

========================================================================================
2. Explanation (Arabic):
------------------------
المسألة تطلب اختيار مواقع للمستودعات (Warehouses) من بين مواقع المتاجر الحالية، بحيث كل متجر يبعد عن أقرب مستودع مسافة أقل من أو تساوي R، مع تقليل عدد المستودعات لأقل ما يمكن (لأن إنشاء مستودعات مكلف).

**صياغة المسألة كـ ILP:**
- (A) **متغيرات القرار:** لكل موقع `j`، متغير ثنائي `y_j`. قيمته 1 إذا اخترنا إنشاء مستودع في الموقع `j`، و 0 بخلاف ذلك.
- (B) **دالة الهدف:** تقليل عدد المستودعات. `Minimize Σ y_j`
- (C) **القيود:** لكل متجر `i`، يجب أن يكون هناك مستودع واحد على الأقل في نطاق مسافة `R` منه.
  نقوم بتعريف المجموعة `covering_j` على أنها جميع المواقع `j` التي تبعد عن المتجر `i` مسافة أقل من أو تساوي `R`. ثم نفرض القيد: `Σ_{j في covering_j} y_j >= 1`.

نستخدم مكتبة `PuLP` لصياغة هذه القيود، ونحل المسألة باستخدام solver `CBC`. ثم نعيد قائمة بأرقام المواقع التي تم اختيارها لإنشاء المستودعات.

========================================================================================
3. Code Implementation:
-----------------------
"""

from pulp import *
from math import sqrt 

def euclidean_distance(location_coords, i, j):
    assert 0 <= i and i < len(location_coords)
    assert 0 <= j and j < len(location_coords)
    if i == j: 
        return 0.0
    (xi, yi) = location_coords[i] # unpack coordinate
    (xj, yj) = location_coords[j]
    return sqrt( (xj - xi)**2 + (yj - yi)**2 )

def solve_warehouse_location(location_coords, R):
    assert R > 0.0, 'radius must be positive'
    n = len(location_coords)
    prob = LpProblem('Warehouse_Location', LpMinimize)
    
    # Decision variables: y[j] = 1 if we place a warehouse at location j
    y = {j: LpVariable(f'y_{j}', cat='Binary') for j in range(n)}
    
    # Objective: minimize number of warehouses
    prob += lpSum([y[j] for j in range(n)])
    
    # Constraints: every location i must be covered by at least one warehouse within distance R
    for i in range(n):
        # find all j within distance R of i (including i itself)
        covering_j = [j for j in range(n) if euclidean_distance(location_coords, i, j) <= R]
        prob += lpSum([y[j] for j in covering_j]) >= 1
    
    # Solve the ILP
    prob.solve(PULP_CBC_CMD(msg=0))
    
    # If optimal solution found, return list of chosen warehouse indices
    if LpStatus[prob.status] == 'Optimal':
        warehouse_locs = [j for j in range(n) if value(y[j]) == 1]
        return warehouse_locs
    else:
        # Fallback (should not happen because placing everywhere is feasible)
        return list(range(n))

"""
========================================================================================
4. Time & Space Complexity Analysis:
------------------------------------
- Time Complexity: The problem is an Integer Linear Program (ILP). Finding the optimal solution is NP-Hard in general. 
  However, since the number of locations `n` in these tests is relatively small (10-15), the CBC solver solves it almost instantaneously using Branch and Bound.
- Space Complexity: O(n) to store the decision variables `y` and the model constraints O(n).
========================================================================================
"""

# ------------------- Helper Functions for Visualization and Validation -------------------
def check_solution(location_coords, R, warehouse_locs):
    n = len(location_coords)
    assert all(j >= 0 and j < n for j in warehouse_locs), f'Warehouse locations must be between 0 and {n-1}'
    neighborhoods = [ [j for j in range(n) if euclidean_distance(location_coords, i, j) <= R] for i in range(n)]
    W = set(warehouse_locs)
    for (i, n_list) in enumerate(neighborhoods):
        assert any(j in W for j in n_list), f'Location # {i} has no warehouse within distance {R}.'
    print('Passed coverage validation!')

def visualize_solution(location_coords, R, warehouse_locs):
    import matplotlib.pyplot as plt 
    n = len(location_coords)
    (xCoords, yCoords) = zip(*location_coords)
    warehouse_x, warehouse_y = [xCoords[j] for j in warehouse_locs], [yCoords[j] for j in warehouse_locs]
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    plt.scatter(xCoords, yCoords, label='Store Locations')
    for j in warehouse_locs: 
        circ = plt.Circle(location_coords[j], R, alpha=0.3, color='g', ls='--', lw=2, ec='k')
        ax.add_patch(circ)
    
    for i in range(n):
        (x,y) = location_coords[i]
        ax.annotate(f'{i}', location_coords[i])
    
    plt.scatter(warehouse_x, warehouse_y, marker='x', c='r', s=50, label='Warehouse Location')
    plt.legend()
    plt.show()


# ------------------- Test Cases -------------------
if __name__ == "__main__":
    from matplotlib import pyplot as plt

    # Test 0: Simple test from the prompt logic
    location_coords_0 = [(1,2), (3, 5), (4, 7), (5, 1), (6, 8), (7, 9), (8,14), (13,6)]
    R_0 = 5
    locs_0 = solve_warehouse_location(location_coords_0, R_0)
    print(f'Test 0: Warehouse locations: {locs_0}')
    assert len(locs_0) <= 4, f'Error: There is a solution involving just 4 locations whereas your code returns {len(locs_0)}'
    visualize_solution(location_coords_0, R_0, locs_0)
    check_solution(location_coords_0, R_0, locs_0)

    # Test 1: R = 2
    location_coords = [(1,1), (1, 2), (2, 3), (1, 4), (5, 1), (3, 3), (4,4), (1,6), (0,3), (3,5), (2,4)]
    R = 2
    print("\n--- Test 1: R = 2 ---")
    locs1 = solve_warehouse_location(location_coords, R)
    print(f'Warehouse locations: {locs1}')
    assert len(locs1) <= 4, f'Error: There is a solution involving just 4 locations whereas your code returns {len(locs1)}'
    visualize_solution(location_coords, R, locs1)
    check_solution(location_coords, R, locs1)
    print('Test 1 (R=2) Passed!\n')

    # Test 2: R = 3
    R = 3
    print("--- Test 2: R = 3 ---")
    locs2 = solve_warehouse_location(location_coords, R)
    print(f'Warehouse locations: {locs2}')
    assert len(locs2) <= 2, f'Error: There is a solution involving just 2 locations whereas your code returns {len(locs2)}'
    visualize_solution(location_coords, R, locs2)
    check_solution(location_coords, R, locs2)
    print('Test 2 (R=3) Passed!')
