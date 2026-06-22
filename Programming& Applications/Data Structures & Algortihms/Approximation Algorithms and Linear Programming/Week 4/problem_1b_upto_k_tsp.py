"""
Problem 1B: k-TSP with At Most k Salespeople (English & Arabic Explanation)
============================================================================
1. Problem Statement (English):
-------------------------------
Notice that in the previous part (Problem 1A), using more salespeople can sometimes lead to a worse cost than using fewer. We wish to modify the problem to allow salespeople to idle. In other words, although we input k salespeople, the tour we construct may involve 1 <= l <= k salespeople.

Modify the ILP formulation to solve the problem of up to k people rather than exactly k salespeople. The requirement that every vertex be visited exactly once by some salesperson remains.

The function `upto_k_tsp_mtz_encoding(n, k, cost_matrix)` should return a list with at most k tours.

============================================================================
2. Explanation (Arabic):
------------------------
في هذه المسألة (Problem 1B)، نريد إجراء تعديل على صياغة الـ ILP الخاصة بـ k-TSP بحيث نسمح للبائعين بعدم العمل (Idle) إذا كان ذلك يؤدي إلى تقليل التكلفة الكلية. 
على سبيل المثال، في الاختبار الأول، استخدام بائع واحد فقط هو الأمثل (التكلفة 10) بدلاً من استخدام 3 بائعين.

**التعديل الأساسي الذي تم في الكود:**
في المسألة السابقة (1A)، كنا نفرض أن عدد الحواف الخارجة من المقر (العقدة 0) يساوي `k` تماماً: 
   `sum(x[0, j]) == k`
أما في هذه المسألة، فقد تم تغيير هذا القيد ليصبح بين 1 و `k`:
   `1 <= sum(x[0, j]) <= k`

هذا التعديل يسمح لمحلِّل الـ ILP (CBC solver) باختيار عدد البائعين الذي يحقق أقل تكلفة إجمالية، طالما أنه لا يتجاوز الحد الأقصى `k` ولا يقل عن 1 (بائع واحد على الأقل ضروري لزيارة جميع المدن).

============================================================================
3. Code Implementation:
-----------------------
"""

from pulp import *

def upto_k_tsp_mtz_encoding(n, k, cost_matrix):
    # check inputs are OK
    assert 1 <= k < n
    assert len(cost_matrix) == n, f'Cost matrix is not {n}x{n}'
    assert all(len(cj) == n for cj in cost_matrix), f'Cost matrix is not {n}x{n}'

    prob = LpProblem('kTSP', LpMinimize)

    V = range(n)                    # all vertices 0..n-1, depot = 0
    # binary variables x_ij for i != j
    x = {}
    for i in V:
        for j in V:
            if i != j:
                x[i, j] = LpVariable(f'x_{i}_{j}', cat='Binary')

    # continuous MTZ variables for non‑depot vertices, 1 <= u_i <= n-1
    u = {i: LpVariable(f'u_{i}', lowBound=1, upBound=n-1, cat='Continuous')
         for i in range(1, n)}

    # objective: minimise total travel cost
    prob += lpSum(cost_matrix[i][j] * x[i, j]
                  for i in V for j in V if i != j), 'TotalCost'

    # degree constraints for non‑depot vertices
    for i in range(1, n):
        prob += lpSum(x[i, j] for j in V if j != i) == 1, f'out_{i}'   # leave i once
        prob += lpSum(x[j, i] for j in V if j != i) == 1, f'in_{i}'    # enter i once

    # depot out‑degree between 1 and k (in-degree will automatically match)
    prob += lpSum(x[0, j] for j in range(1, n)) >= 1, 'depot_out_min'
    prob += lpSum(x[0, j] for j in range(1, n)) <= k, 'depot_out_max'

    # MTZ subtour elimination constraints
    for i in range(1, n):
        for j in range(1, n):
            if i != j:
                prob += u[i] - u[j] + (n - 1) * x[i, j] <= n - 2, f'mtz_{i}_{j}'

    # solve the ILP (suppress solver output)
    prob.solve(PULP_CBC_CMD(msg=False))

    # extract the tours (at most k)
    tours = []
    for j in range(1, n):
        if x[0, j].varValue > 0.5:          # j is the first city after depot
            tour = [0, j]
            cur = j
            while True:
                nxt = None
                for l in V:
                    if l != cur and x[cur, l].varValue > 0.5:
                        nxt = l
                        break
                if nxt is None or nxt == 0:   # back to depot -> end of tour
                    break
                tour.append(nxt)
                cur = nxt
            tours.append(tour)

    # post‑condition: 1 <= len(tours) <= k
    assert 1 <= len(tours) <= k, f'Extracted {len(tours)} tours, expected between 1 and {k}'
    return tours

"""
============================================================================
4. Time & Space Complexity Analysis:
------------------------------------
- Time Complexity: 
    The problem is NP-Hard. The number of binary variables is O(n^2) and the number of constraints is O(n^2) as well. The solver uses branch-and-bound. By changing the depot constraint to an inequality instead of equality, the search space becomes slightly larger, but the solver (CBC) handles it very efficiently for n up to ~15-20.
- Space Complexity: O(n^2) to store the cost matrix and the ILP model variables.
============================================================================
"""

# ------------------- Test Cases -------------------
if __name__ == "__main__":
    from random import uniform, randint

    # Test 1: 3 points
    cost_matrix = [ [None,3,4,3,5],
                    [1, None, 2,4, 1],
                    [2, 1, None, 5, 4],
                    [1, 1, 5, None, 4],
                    [2, 1, 3, 5, None] ]
    n, k = 5, 3
    all_tours = upto_k_tsp_mtz_encoding(n, k, cost_matrix)
    print(f'Test 1 Tours: {all_tours}')
    assert len(all_tours) <= k, f'<= {k} tours -- your code returns {len(all_tours)} tours instead'
    
    tour_cost = 0
    for tour in all_tours:
        assert tour[0] == 0, 'Each salesperson tour must start from vertex 0'
        i = 0
        for j in tour[1:]:
            tour_cost += cost_matrix[i][j]
            i = j
        tour_cost += cost_matrix[i][0]

    assert len(all_tours) == 1, f'In this example, just one salesperson is needed. Your code returns {len(all_tours)}'
    assert abs(tour_cost - 10) <= 0.001, f'Expected tour cost is 10, your code returned {tour_cost}'
    print('Test 1 passed: 3 points\n')


    # Test 2: 3 points
    cost_matrix2 = [ 
     [None, 1, 1, 1, 1, 1, 1, 1],
        [0, None, 1, 2, 1, 1, 1, 1],
        [1, 0, None, 1, 2, 2, 2, 1],
        [1, 2, 2, None, 0, 1, 2, 1],
        [1, 1, 1, 1, None, 1, 1, 1],
        [0,  1, 2, 1, 1, None, 1, 1],
        [1, 0,  1, 2, 2, 2,None, 1],
        [1, 2, 2, 0, 1, 2, 1, None],
    ]
    n, k = 8, 5
    all_tours = upto_k_tsp_mtz_encoding(n, k, cost_matrix2)
    print(f'Test 2 Tours: {all_tours}')
    assert len(all_tours) <= k, f'k={k} must yield at most k tours'
    tour_cost = 0
    for tour in all_tours:
        i = 0
        for j in tour[1:]:
            tour_cost += cost_matrix2[i][j]
            i = j
        tour_cost += cost_matrix2[i][0]

    assert abs(tour_cost - 4) <= 0.001, f'Expected tour cost is 4, your code returned {tour_cost}'
    print('Test 2 passed: 3 points\n')


    # Test 3: 4 points (Randomized)
    def create_cost(n):
        return [ [uniform(0, 5) if i != j else None for j in range(n)] for i in range(n)]

    for trial in range(20):
        n = randint(5, 11)
        k = randint(2, n//2)
        rand_cost_matrix = create_cost(n)
        all_tours = upto_k_tsp_mtz_encoding(n, k, rand_cost_matrix)
        assert len(all_tours) <= k, f'k={k} must yield at most k tours'
        for tour in all_tours:
            assert tour[0] == 0, 'Each tour must start from vertex 0'
        
        for i in range(1, n):
            is_in_tour = [1 if i in tour else 0 for tour in all_tours]
            assert sum(is_in_tour) == 1, f' vertex {i} is in {sum(is_in_tour)} tours'
    print('Test 3 passed: 4 points')
    
    print("All Tests Passed Successfully!")
