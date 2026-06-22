"""
Problem 1: k-Travelling Salespeople Problem (k-TSP) - English & Arabic Explanation
==================================================================================
1. Problem Statement (English):
-------------------------------
We saw how to solve TSPs in this module. In this problem, we will ask you to adapt the TSP solution to encode a TSP as an integer linear program to the related problem of k Travelling Salespeople Problem (k-TSP).

Let G be a complete graph with n vertices that we will label 0, ..., n-1. Our costs are specified using a matrix C where C_{i,j} is the cost of the edge i to j for i != j.

In this problem, we have k >= 1 salespeople who must start from vertex 0 (the sales office) and together visit every location in the graph, each returning back to vertex 0. Each location must be visited exactly once by some salesperson. Therefore, no two salesperson tours have a vertex in common (other than vertex 0).

We use the MTZ approach to formulate the ILP:
- Decision variables: x_{i,j} (binary) for i != j denoting if the tour traverses the edge from i to j.
- Time stamps: t_i for i = 1, ..., n-1. The start/end vertex 0 does not get a time stamp.
- Constraints:
    - Degree constraints: Each non-depot vertex has exactly one incoming and one outgoing edge. The depot (vertex 0) has k outgoing and k incoming edges.
    - MTZ subtour elimination constraints: u_i - u_j + (n-1) * x_{i,j} <= n-2.

==================================================================================
2. Explanation (Arabic):
------------------------
المسألة تتعلق بنسخة معدلة من مسألة البائع المتجول (TSP) حيث لدينا `k` من البائعين الذين يبدأون جميعاً من العقدة 0 (المقر) ويجب عليهم زيارة جميع المدن الأخرى (1 إلى n-1) مرة واحدة فقط، والعودة إلى المقر.

لصياغة المسألة كـ ILP باستخدام نهج MTZ:
1. **متغيرات القرار:** `x_{i,j}` ثنائي (1 إذا تم السفر من i إلى j، 0 خلاف ذلك)، و `u_i` مستمر (يمثل الترتيب الزمني للعقدة i).
2. **دالة الهدف:** تقليل التكلفة الكلية: `Σ C_{i,j} * x_{i,j}`.
3. **القيود:**
   - لكل مدينة (غير المقر): درجة الخروج = 1، ودرجة الدخول = 1.
   - بالنسبة للمقر (العقدة 0): درجة الخروج = k (لأن كل بائع يخرج مرة)، ودرجة الدخول = k (لأن كل بائع يعود مرة).
   - **قيود منع الجولات الفرعية (MTZ):** باستخدام متغيرات `u_i`، نفرض أن ترتيب الزيارة يتزايد دائماً. `u_i - u_j + (n-1) * x_{i,j} <= n-2`.

بعد الحل، يتم استخراج المسارات (tours) باتباع الحواف من المقر `0` إلى باقي المدن، ثم تتبع المسار حتى العودة إلى `0`.

==================================================================================
3. Code Implementation:
-----------------------
"""

from pulp import *

def k_tsp_mtz_encoding(n, k, cost_matrix):
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

    # depot out‑ and in‑degree must equal k
    prob += lpSum(x[0, j] for j in range(1, n)) == k, 'depot_out'
    prob += lpSum(x[i, 0] for i in range(1, n)) == k, 'depot_in'

    # MTZ subtour elimination constraints
    for i in range(1, n):
        for j in range(1, n):
            if i != j:
                prob += u[i] - u[j] + (n - 1) * x[i, j] <= n - 2, f'mtz_{i}_{j}'

    # solve the ILP (suppress solver output)
    prob.solve(PULP_CBC_CMD(msg=False))

    # extract the k tours
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

    assert len(tours) == k, f'Extracted {len(tours)} tours instead of {k}'
    return tours

"""
==================================================================================
4. Time & Space Complexity Analysis:
------------------------------------
- Time Complexity: The problem is NP-Hard. 
  The number of binary variables is O(n^2) and the number of constraints is O(n^2) as well.
  The CBC solver uses branch-and-bound to find the optimal solution. In practice, it handles up to ~15-20 cities efficiently with this ILP formulation.
- Space Complexity: O(n^2) to store the cost matrix and the ILP model variables.
==================================================================================
"""

# ------------------- Test Cases -------------------
if __name__ == "__main__":
    from random import uniform, randint

    # Test 1: k=2 (3 points)
    cost_matrix1 = [ [None,3,4,3,5],
                     [1, None, 2,4, 1],
                     [2, 1, None, 5, 4],
                     [1, 1, 5, None, 4],
                     [2, 1, 3, 5, None] ]
    n1, k1 = 5, 2
    all_tours1 = k_tsp_mtz_encoding(n1, k1, cost_matrix1)
    print(f'Test 1 Tours: {all_tours1}')
    assert len(all_tours1) == k1, f'k={k1} must yield two tours'

    tour_cost1 = 0
    for tour in all_tours1:
        assert tour[0] == 0, 'Each salesperson tour must start from vertex 0'
        i = 0
        for j in tour[1:]:
            tour_cost1 += cost_matrix1[i][j]
            i = j
        tour_cost1 += cost_matrix1[i][0]

    assert abs(tour_cost1 - 12) <= 0.001, f'Expected tour cost is 12, got {tour_cost1}'
    print('Test 1 passed: 3 points\n')


    # Test 2: k=3 (2 points) - Same matrix, different k
    n2, k2 = 5, 3
    all_tours2 = k_tsp_mtz_encoding(n2, k2, cost_matrix1)
    print(f'Test 2 Tours: {all_tours2}')
    assert len(all_tours2) == k2, f'k={k2} must yield three tours'

    tour_cost2 = 0
    for tour in all_tours2:
        assert tour[0] == 0, 'Each salesperson tour must start from vertex 0'
        i = 0
        for j in tour[1:]:
            tour_cost2 += cost_matrix1[i][j]
            i = j
        tour_cost2 += cost_matrix1[i][0]

    assert abs(tour_cost2 - 16) <= 0.001, f'Expected tour cost is 16, got {tour_cost2}'
    print('Test 2 passed: 2 points\n')


    # Test 3: k=2 (3 points) - Different matrix
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
    n3, k3 = 8, 2
    all_tours3 = k_tsp_mtz_encoding(n3, k3, cost_matrix2)
    print(f'Test 3 Tours: {all_tours3}')
    tour_cost3 = 0
    for tour in all_tours3:
        i = 0
        for j in tour[1:]:
            tour_cost3 += cost_matrix2[i][j]
            i = j
        tour_cost3 += cost_matrix2[i][0]

    assert abs(tour_cost3 - 4) <= 0.001, f'Expected tour cost is 4, got {tour_cost3}'
    print('Test 3 passed: 3 points\n')


    # Test 4: k=4 (2 points) - Different matrix, different k
    n4, k4 = 8, 4
    all_tours4 = k_tsp_mtz_encoding(n4, k4, cost_matrix2)
    print(f'Test 4 Tours: {all_tours4}')
    tour_cost4 = 0
    for tour in all_tours4:
        i = 0
        for j in tour[1:]:
            tour_cost4 += cost_matrix2[i][j]
            i = j
        tour_cost4 += cost_matrix2[i][0]

    assert abs(tour_cost4 - 6) <= 0.001, f'Expected tour cost is 6, got {tour_cost4}'
    print('Test 4 passed: 2 points\n')


    # Test 5: Random Trials (15 points)
    def create_cost(n):
        return [ [uniform(0, 5) if i != j else None for j in range(n)] for i in range(n)]

    for trial in range(5):
        print(f'Trial # {trial}')
        n_rand = randint(5, 11)
        k_rand = randint(2, n_rand//2)
        print(f' n= {n_rand}, k={k_rand}')
        rand_cost_matrix = create_cost(n_rand)
        all_tours_rand = k_tsp_mtz_encoding(n_rand, k_rand, rand_cost_matrix)

        assert len(all_tours_rand) == k_rand, f'k={k_rand} must yield k tours'
        for tour in all_tours_rand:
            assert tour[0] == 0, 'Each tour must start from vertex 0'
        
        for i in range(1, n_rand):
            is_in_tour = [1 if i in tour else 0 for tour in all_tours_rand]
            assert sum(is_in_tour) == 1, f'Vertex {i} is in {sum(is_in_tour)} tours'
        print('------')
    print('Test 5 passed: 15 points')
    
    print("All Tests Passed Successfully!")
