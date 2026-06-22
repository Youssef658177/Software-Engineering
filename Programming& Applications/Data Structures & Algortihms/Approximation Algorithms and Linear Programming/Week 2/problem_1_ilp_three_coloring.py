"""
Problem Set 2 - Problem 1: Three Coloring using Integer Linear Programming (English & Arabic Explanation)
==========================================================================================================
1. Problem Statement (English):
-------------------------------
In this problem, you will setup and solve the three coloring problem as an integer linear programming problem.

The three coloring problem inputs an undirected graph G with vertices V = {0, ..., n - 1} and undirected edges E. We are looking to color each vertex one of three colors red, green, or blue such that for any edge (i, j) the nodes i, j have different colors.

Given a graph, we wish to know if a three coloring is possible and if so, we wish to find the three coloring.

We formulate this problem as an Integer Linear Program:
- Decision variables: x_i^R, x_i^G, x_i^B (Binary values 0 or 1).
- Constraints:
    1. Each vertex must take exactly one color: x_i^R + x_i^G + x_i^B = 1.
    2. Adjacent vertices cannot have the same color: For each edge (i,j) and each color c, x_i^c + x_j^c <= 1.

Write a function `encode_and_solve_three_coloring(n, edge_list)` that solves this problem using PuLP.

==========================================================================================================
2. Explanation (Arabic):
------------------------
المسألة تطلب حل مشكلة تلوين الرسم البياني بـ 3 ألوان باستخدام البرمجة الخطية الصحيحة (Integer Linear Programming - ILP). 
الهدف هو تحديد ما إذا كان الرسم البياني يمكن تلوينه بـ 3 ألوان (أحمر، أخضر، أزرق) بحيث لا يتشارك رأسين متجاورين في نفس اللون.

**كيفية صياغة المسألة كـ ILP:**
1. **المتغيرات:** لكل رأس `i` ولكل لون `c`، نعرف متغير ثنائي `x_{i,c}`. قيمته 1 إذا كان الرأس `i` ملوناً باللون `c`، و 0 بخلاف ذلك.
2. **القيود:**
   - **التلوين الفريد:** كل رأس `i` يجب أن يأخذ لوناً واحداً فقط. (x_{i,'r'} + x_{i,'g'} + x_{i,'b'} == 1).
   - **منع نفس اللون:** لكل حافة `(i, j)` ولكل لون `c`، لا يمكن للرأسين `i` و `j` أن يأخذا اللون `c` معاً. (x_{i,c} + x_{j,c} <= 1).

نستخدم مكتبة `PuLP` في بايثون لحل هذه المسألة (نبحث عن حل ممكن، بدون دالة هدف، حيث `prob += 0`).
إذا وجد الحل، نرجع `(True, color_assignment)`، وإلا نرجع `(False, None)`.

==========================================================================================================
3. Code Implementation:
-----------------------
"""

from pulp import *

def encode_and_solve_three_coloring(n, edge_list):
    assert n >= 1, 'Graph must have at least one vertex'
    assert all( 0 <= i and i < n and 0 <= j and j < n and i != j for (i,j) in edge_list ), 'Edge list is not well formed'
    
    # Create the LP problem. We are looking for a feasible solution, so we minimize 0.
    prob = LpProblem('Three_Coloring', LpMinimize)
    colors = ['r', 'g', 'b']
    
    # Decision variables: x[(i, c)] = 1 if vertex i gets color c, else 0
    x = {}
    for i in range(n):
        for c in colors:
            x[(i, c)] = LpVariable(f"x_{i}_{c}", cat='Binary')
    
    # No objective, just feasibility
    prob += 0
    
    # Constraint 1 (Part A): Each vertex must have exactly one color
    for i in range(n):
        prob += lpSum([x[(i, c)] for c in colors]) == 1
    
    # Constraint 2 (Part B): Adjacent vertices cannot share the same color
    for (i, j) in edge_list:
        for c in colors:
            prob += x[(i, c)] + x[(j, c)] <= 1
    
    # Solve quietly (suppress solver output)
    prob.solve(PULP_CBC_CMD(msg=0))
    
    # Check if a feasible solution was found
    if LpStatus[prob.status] == 'Optimal':
        color_assign = [None] * n
        for i in range(n):
            for c in colors:
                if value(x[(i, c)]) == 1:
                    color_assign[i] = c
                    break
        return True, color_assign
    else:
        return False, None

"""
==========================================================================================================
4. Time & Space Complexity Analysis:
------------------------------------
- Number of variables: n * 3 binary variables.
- Number of constraints: 
    - n constraints for the "exactly one color" rule.
    - |E| * 3 constraints for the "adjacent different color" rule.
- Building the model: O(n + |E|).
- Solving the model: Internally, the solver uses Branch and Bound. In the worst case, it could be exponential O(3^n), but the ILP solvers (like CBC) are highly optimized and perform very well in practice for graphs of this size.
- Space Complexity: O(n + |E|) to store the model.
==========================================================================================================
"""

# ------------------- Helper Function for Tests -------------------
def check_three_color_assign(n, edge_list, color_assign):
    assert len(color_assign) == n, f'Error: The list of color assignments has {len(color_assign)} entries but must be same as number of vertices {n}'
    assert all( col == 'r' or col == 'b' or col == 'g' for col in color_assign), f'Error: Each entry in color assignment list must be r, g or b. Your code returned: {color_assign}'
    for (i, j) in edge_list:
        ci = color_assign[i]
        cj = color_assign[j]
        assert ci != cj, f' Error: For edge ({i,j}) we have same color assignment ({ci, cj})'
    print('Success: Three coloring assignment checks out!!')

# ------------------- Test Cases -------------------
if __name__ == "__main__":
    # Test 1: 10 points (3-colorable graph, 4 vertices - 1 edge missing)
    n = 4
    edge_list = [(0,1), (0, 2), (0,3), (1, 3), (2,3)]
    (flag, color_assign) = encode_and_solve_three_coloring(n, edge_list)
    assert flag == True, 'Error: Graph is three colorable but your code wrongly returns flag = False'
    print(f'Three color assignment: {color_assign}')
    check_three_color_assign(n, edge_list, color_assign)
    print('Passed: 10 points!\n')


    # Test 2: 5 points (NOT 3-colorable - K4 complete graph)
    n = 4
    edge_list = [(0,1), (0, 2), (0,3), (1,2), (1, 3), (2,3)]
    (flag, color_assign) = encode_and_solve_three_coloring(n, edge_list)
    assert flag == False, 'Error: Graph is NOT three colorable but your code wrongly returns flag = True'
    print('Passed: 5 points!\n')


    # Test 3: 5 points (3-colorable complex graph)
    n = 9
    edge_list = [ (0, 4), (0, 6), (0, 8), (1, 3), (1, 4), (1, 8), (2, 3), (2, 5), (2,6), (2,7), (3, 4), (3,5), (3,6), (3,8),(4,5), (4,6),(5,7),(6,8),(7,8)]
    (flag, color_assign) = encode_and_solve_three_coloring(n, edge_list)
    assert flag == True, 'Error: Graph is three colorable but your code wrongly returns flag = False'
    print(f'Three color assignment: {color_assign}')
    check_three_color_assign(n, edge_list, color_assign)
    print('Passed: 5 points!\n')

    print("All tests passed successfully!")
