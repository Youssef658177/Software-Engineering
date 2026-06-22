"""
Problem 3: TSP with Precedence Constraints (English & Arabic Explanation)
=========================================================================
1. Problem Statement (English):
-------------------------------
In this problem, we wish to solve TSP with additional constraints. Suppose we are given a TSP instance in the form of a n x n matrix C representing a complete graph.

We wish to solve a TSP with additional constraints specified as a list [(i0, j0), ..., (ik, jk)] wherein each pair (i_l, j_l) in the list specifies that vertex i_l must be visited in the tour before vertex j_l. Assume that the tour starts/ends at vertex 0 and none of the vertices in the constraint list is 0. I.e., i_l != 0, j_l != 0 for all l.

Modify one of the ILP encodings we have presented to solve TSP with extra constraints.

Implement your solution in the function `tsp_with_extra_constraints(n, cost_matrix, constraints)` where:
- `n`: number of vertices.
- `cost_matrix`: n x n matrix representing the TSP instance.
- `constraints`: list of pairs (i, j) meaning vertex i must be visited before vertex j.

=========================================================================
2. Explanation (Arabic):
------------------------
المسألة تطلب حل TSP مع قيود إضافية تقول إنه يجب زيارة مدينة `i` قبل مدينة `j` في المسار (Precedence Constraints). 

لحل هذه المسألة، نقوم بتعديل صياغة ILP الخاصة بـ MTZ (Miller-Tucker-Zemlin) كما يلي:
1. **المتغيرات:** متغيرات ثنائية `x_{i,j}` للحواف، ومتغيرات زمنية متصلة `u_i` للترتيب (الطوابع الزمنية) للمدن من 1 إلى n-1.
2. **دالة الهدف:** تقليل التكلفة الكلية `Σ C_{i,j} * x_{i,j}`.
3. **القيود الأساسية:** قيود الدرجة (الدخول والخروج لجميع المدن بما فيها المقر 0)، وقيود MTZ لمنع الجولات الفرعية (Subtour elimination): `u_i - u_j + (n-1) * x_{i,j} <= n-2`.
4. **قيود الأسبقية (Precedence):** لكل زوج `(i, j)` في قائمة `constraints`، نضيف القيد `u_i <= u_j - 1`. هذا يضمن أن الترتيب الزمني للمدينة `i` يأتي قبل الترتيب الزمني للمدينة `j` بحرفية.

بعد حل الـ ILP باستخدام `PULP_CBC_CMD`، نستخرج المسار النهائي (Tour) ونرتبه ونتأكد من صحة القيود.

=========================================================================
3. Code Implementation:
-----------------------
"""

from pulp import *

def tsp_with_extra_constraints(n, cost_matrix, constraints):
    assert len(cost_matrix) == n, f'Cost matrix is not {n}x{n}'
    assert all(len(cj) == n for cj in cost_matrix), f'Cost matrix is not {n}x{n}'
    assert all( 1 <= i < n and 1 <= j < n and i != j for (i,j) in constraints)

    prob = LpProblem('TSP_precedence', LpMinimize)
    V = range(n)                     # vertices 0..n-1, depot = 0

    # binary variables x_{i,j} for i != j
    x = {}
    for i in V:
        for j in V:
            if i != j:
                x[i, j] = LpVariable(f'x_{i}_{j}', cat='Binary')

    # continuous time stamps for vertices 1..n-1 (order in tour)
    u = {i: LpVariable(f'u_{i}', lowBound=1, upBound=n-1, cat='Continuous')
         for i in range(1, n)}

    # objective: minimise total travel cost
    prob += lpSum(cost_matrix[i][j] * x[i, j]
                  for i in V for j in V if i != j), 'TotalCost'

    # degree constraints
    for i in range(1, n):
        prob += lpSum(x[i, j] for j in V if j != i) == 1   # leave i exactly once
        prob += lpSum(x[j, i] for j in V if j != i) == 1   # enter i exactly once
    prob += lpSum(x[0, j] for j in range(1, n)) == 1       # leave depot once
    prob += lpSum(x[i, 0] for i in range(1, n)) == 1       # return to depot once

    # MTZ subtour elimination constraints
    for i in range(1, n):
        for j in range(1, n):
            if i != j:
                prob += u[i] - u[j] + (n - 1) * x[i, j] <= n - 2

    # extra precedence constraints: i must be visited before j
    for (i, j) in constraints:
        prob += u[i] <= u[j] - 1

    # solve
    prob.solve(PULP_CBC_CMD(msg=False))

    # extract the tour
    tour = [0]
    cur = 0
    while True:
        nxt = None
        for j in V:
            if j != cur and x[cur, j].varValue > 0.5:
                nxt = j
                break
        if nxt is None or nxt == 0:
            break
        tour.append(nxt)
        cur = nxt

    # sanity check: should contain every vertex exactly once
    assert len(tour) == n, f'Extracted tour has {len(tour)} vertices, expected {n}'
    return tour

"""
=========================================================================
4. Time & Space Complexity Analysis:
------------------------------------
- Time Complexity: The problem is NP-Hard. 
  The ILP uses O(n^2) binary variables and O(n^2) constraints. The CBC solver uses branch-and-bound to find the optimal solution. For n up to ~15-20, the solver performs exceptionally fast.
- Space Complexity: O(n^2) to store the cost matrix, binary variables, and the MILP model.
=========================================================================
"""

# ------------------- Test Cases -------------------
if __name__ == "__main__":
    from random import uniform, randint

    # Test Case 1: 3 points (Precedence constraints (3,4) and (1,2))
    print("--- Test 1 ---")
    cost_matrix = [ [None,3,4,3,5],
                    [1, None, 2,4, 1],
                    [2, 1, None, 5, 4],
                    [1, 1, 5, None, 4],
                    [2, 1, 3, 5, None] ]
    n = 5
    constraints_1 = [(3,4),(1,2)]
    tour = tsp_with_extra_constraints(n, cost_matrix, constraints_1)
    i = 0
    tour_cost = 0
    for j in tour[1:]:
        tour_cost += cost_matrix[i][j]
        i = j
    tour_cost += cost_matrix[i][0]
    print(f'Tour: {tour}')
    print(f'Cost of your tour: {tour_cost}')
    assert abs(tour_cost-10) <= 0.001, 'Expected cost was 10'
    for i in range(n):
        num = sum([1 if j == i else 0 for j in tour])
        assert num == 1, f'Vertex {i} repeats {num} times in tour'
    for (i, j) in constraints_1:
        assert tour.index(i) < tour.index(j), f'Tour does not respect constraint {(i,j)}'
    print('Test 1 Passed (3 points)\n')


    # Test Case 2: 3 points (Precedence constraints (4,3) and (1,2))
    print("--- Test 2 ---")
    constraints_2 = [(4,3),(1,2)]
    tour = tsp_with_extra_constraints(n, cost_matrix, constraints_2)
    i = 0
    tour_cost = 0
    for j in tour[1:]:
        tour_cost += cost_matrix[i][j]
        i = j
    tour_cost += cost_matrix[i][0]
    print(f'Tour: {tour}')
    print(f'Cost of your tour: {tour_cost}')
    assert abs(tour_cost-13) <= 0.001, 'Expected cost was 13'
    for i in range(n):
        num = sum([1 if j == i else 0 for j in tour])
        assert num == 1, f'Vertex {i} repeats {num} times in tour'
    for (i, j) in constraints_2:
        assert tour.index(i) < tour.index(j), f'Tour does not respect constraint {(i,j)}'
    print('Test 2 Passed (3 points)\n')


    # Test Case 3: 10 points (Random trials)
    print("--- Test 3: Random Trials ---")
    def create_cost(n):
        return [ [uniform(0, 5) if i != j else None for j in range(n)] for i in range(n)]

    for trial in range(20):
        print(f'Trial # {trial}')
        n = randint(6, 11)
        cost_matrix = create_cost(n)
        constraints = [(1, 3), (4, 2), (n-1, 1), (n-2, 2)]
        tour = tsp_with_extra_constraints(n, cost_matrix, constraints)
        i = 0
        tour_cost = 0
        for j in tour[1:]:
            tour_cost += cost_matrix[i][j]
            i = j
        tour_cost += cost_matrix[i][0]
        print(f'Tour: {tour}')
        print(f'Cost of your tour: {tour_cost}')
        for i in range(n):
            num = sum([1 if j == i else 0 for j in tour])
            assert num == 1, f'Vertex {i} repeats {num} times in tour'
        for (i, j) in constraints:
            assert tour.index(i) < tour.index(j), f'Tour does not respect constraint {(i,j)}'
    print('Test 3 Passed (10 points)')
    
    print("\nAll Tests Passed Successfully!")
