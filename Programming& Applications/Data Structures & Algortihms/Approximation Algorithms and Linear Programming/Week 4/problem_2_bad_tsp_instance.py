"""
Problem 2: Bad Instance for MST Shortcutting (Non-Metric TSP) - English & Arabic Explanation
=============================================================================================
1. Problem Statement (English):
-------------------------------
We noted the use of Christofides algorithm for metric TSP. We noted that for non-metric TSPs it does not work. In fact, the shortcutting used in Christofides algorithm can be arbitrarily bad for a TSP that is symmetric but fails to be a metric TSP.

In this example, we would like you to frame a symmetric TSP instance (C_{ij} = C_{ji}) with 5 vertices wherein the algorithm obtained by "shortcutting" the minimum spanning tree (MST), which would be a 2-factor approximation for metric TSP, yields an answer that can be quite "far off" from the optimal solution. The optimal answer must be at least \(10^6\) times smaller than that obtained by the MST-based approximation.

=============================================================================================
2. Explanation (Arabic):
------------------------
في هذه المسألة، نطلب إنشاء مصفوفة تكلفة (متماثلة) لمسألة البائع المتجول (TSP) مكونة من 5 رؤوس، بحيث تفشل خوارزمية التقريب القائمة على تقصير شجرة الامتداد الدنيا (MST Shortcutting) بشكل كارثي، وتكون تكلفتها أكبر بـ 1 مليون مرة من الحل الأمثل.

**لماذا يحدث هذا؟**
خوارزمية MST Shortcutting هي خوارزمية تقريب (2-Approximation) وتعمل بشكل ممتاز إذا كان الرسم البياني **مترياً (Metric)** (أي يتحقق فيه شرط عدم المساواة المثلثية \(d(a,c) \le d(a,b) + d(b,c)\)).
في المصفوفة التي قمت بكتابتها في الكود، قمت بخرق هذا الشرط عمداً:
- حواف الرأس 0 إلى باقي الرؤوس قيمتها 1 (وهذا يجعل شجرة MST هي شجرة نجمية مركزها 0).
- الحواف بين الرؤوس 1 و 2، و 2 و 3، و 3 و 4 قيمتها هائلة جداً (\(10^{12}\)).
- عند تطبيق تقنية Shortcutting على شجرة الـ MST، تضطر الخوارزمية للعبور عبر هذه الحواف الهائلة لتعود للنقطة 0، وتصبح التكلفة الكلية حوالي \(3 \times 10^{12}\).
- أما الحل الأمثل (الذي يتم حسابه بواسطة `mtz_encoding_tsp`)، فيمكنه أن يتجنب هذه الحواف الهائلة تماماً عن طريق المرور بمسار ذكي: `0 -> 2 -> 4 -> 1 -> 3 -> 0`، وتكون تكلفته الكلية **8 فقط** (1 + 2 + 2 + 2 + 1).
- هذا يؤدي إلى نسبة فرق هائلة تبلغ تقريباً \(3.75 \times 10^{11}\)، وهي أكبر بكثير من الـ \(10^6\) المطلوبة في الاختبار.

=============================================================================================
3. Code Implementation:
-----------------------
"""

import networkx as nx
from pulp import *
import constants

# ------------------- Step 1: Define the Cost Matrix -------------------
# Write down the cost matrix as a list of lists.
cost_matrix = [
    [None, 1, 1, 1, 1],
    [1, None, 10**12, 2, 2],
    [1, 10**12, None, 10**12, 2],
    [1, 2, 10**12, None, 10**12],
    [1, 2, 2, 10**12, None]
]

# ------------------- Step 2: MST Shortcutting (Approximation) -------------------
def minimum_spanning_tree_tsp(n, cost_matrix):
    G = nx.Graph()
    for i in range(n):
        for j in range(i):
            G.add_edge(i, j, weight=cost_matrix[i][j])
    T = nx.minimum_spanning_tree(G)
    print(f'MST for your graph has the edges {T.edges}')
    mst_cost = 0
    mst_dict = {} # store mst as a dictionary
    for (i,j) in T.edges:
        mst_cost += cost_matrix[i][j]
        if i in mst_dict:
            mst_dict[i].append(j)
        else:
            mst_dict[i] = [j]
        if j in mst_dict:
            mst_dict[j].append(i)
        else:
            mst_dict[j] = [i]
    print(f'MST cost: {mst_cost}')
    print(mst_dict)
    
    # Let's form a tour with short cutting
    def traverse_mst(tour_so_far, cur_node):
        next_nodes = mst_dict[cur_node]
        for j in next_nodes:
            if j in tour_so_far:
                continue
            tour_so_far.append(j)
            traverse_mst(tour_so_far, j)
        return
    
    tour = [0]
    traverse_mst(tour, 0)
    i = 0
    tour_cost = 0
    for j in tour[1:]:
        tour_cost += cost_matrix[i][j]
        i = j
    tour_cost += cost_matrix[i][0]
    return tour, tour_cost

# ------------------- Step 3: Optimal TSP (Exact ILP) -------------------
def mtz_encoding_tsp(n, cost_matrix):
    assert len(cost_matrix) == n, f'Cost matrix is not {n}x{n}'
    assert all(len(cj) == n for cj in cost_matrix), f'Cost matrix is not {n}x{n}'
    
    # create our encoding variables
    binary_vars = [
        [ LpVariable(f'x_{i}_{j}', cat='Binary') if i != j else None for j in range(n)] 
        for i in range(n) 
    ]
    # add time stamps for ranges 1 .. n (skip vertex 0 for timestamps)
    time_stamps = [LpVariable(f't_{j}', lowBound=0, upBound=n, cat='Continuous') for j in range(1, n)]
    
    # create the problem
    prob = LpProblem('TSP-MTZ', LpMinimize)
    # create add the objective function 
    objective_function = lpSum( [ lpSum([xij*cj if xij != None else 0 for (xij, cj) in zip(brow, crow) ])
                           for (brow, crow) in zip(binary_vars, cost_matrix)] )
    prob += objective_function 
    
    # add the degree constraints
    for i in range(n):
        prob += lpSum([xj for xj in binary_vars[i] if xj != None]) == 1
        prob += lpSum([binary_vars[j][i] for j in range(n) if j != i]) == 1
    
    # add time stamp constraints (MTZ subtour elimination)
    for i in range(1, n):
        for j in range(1, n):
            if i == j: 
                continue
            xij = binary_vars[i][j]
            ti = time_stamps[i-1]
            tj = time_stamps[j -1]
            prob += tj >= ti + xij - (1-xij)*(n+1)
            
    # Done: solve the problem
    status = prob.solve(PULP_CBC_CMD(msg=False))
    assert status == constants.LpStatusOptimal, f'Unexpected non-optimal status {status}'
    
    # Extract the tour
    tour = [0]
    tour_cost = 0
    while len(tour) < n:
        i = tour[-1]
        sols = [j for (j, xij) in enumerate(binary_vars[i]) if xij != None and xij.varValue >= 0.999]
        assert len(sols) == 1
        j = sols[0]
        tour_cost = tour_cost + cost_matrix[i][j]
        tour.append(j)
        assert j != 0
        
    i = tour[-1]
    tour_cost = tour_cost + cost_matrix[i][0]
    return tour, tour_cost

"""
=============================================================================================
4. Time & Space Complexity Analysis:
------------------------------------
- Building MST (Shortcutting): O(n^2 log n) using Prim's or Kruskal's algorithm. Here n=5, so it is very fast.
- Solving Optimal TSP (ILP - MTZ encoding): The problem is NP-Hard. Using ILP with n=5 is practically instant.
- Space Complexity: O(n^2) to store the cost matrix and the ILP variables.
=============================================================================================
"""

# ------------------- Test Cases -------------------
if __name__ == "__main__":
    print("="*40)
    print("Running the Bad TSP Example")
    print("="*40)

    # Check matrix symmetry
    assert len(cost_matrix) == 5, f'Cost matrix must have 5 rows.'
    assert all(len(cj) == 5 for cj in cost_matrix), f'Each row must have 5 entries.'
    for i in range(5):
        for j in range(i):
            assert cost_matrix[i][j] == cost_matrix[j][i], f'Cost matrix fails to be symmetric.'
    print('Structure of your cost matrix looks OK (3 points).')

    # Compute MST approximation
    tour, tour_cost = minimum_spanning_tree_tsp(5, cost_matrix)
    print(f'MST approximation yields tour is {tour} with cost {tour_cost}')

    # Compute exact optimal answer
    opt_tour, opt_tour_cost = mtz_encoding_tsp(5, cost_matrix)
    print(f'Optimal tour is {opt_tour} with cost {opt_tour_cost}')

    # Check that the fraction is 1 million times apart.
    print(f"Ratio: {tour_cost / opt_tour_cost}")
    assert tour_cost / opt_tour_cost >= 1E+06, 'The TSP + shortcutting tour must be at least 10^6 times costlier than optimum.'
    
    print('Test passed: 7 points')
    print("All tests passed!")
