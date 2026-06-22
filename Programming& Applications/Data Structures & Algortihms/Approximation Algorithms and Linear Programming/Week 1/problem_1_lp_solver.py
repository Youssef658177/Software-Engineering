"""
Problem 1: Use PULP to encode a linear programming problem (English & Arabic Explanation)
==========================================================================================
1. Problem Statement (English):
-------------------------------
This problem set will involve using a python library called PULP to formulate and solve linear programming problems.

As a "warm up" exercise, we are going to use pulp to solve a generic LP of the form:

    max      c0*x0 + ... + cn-1*xn-1
    s.t.     a0,0*x0 + ... + a0,n-1*xn-1 <= b0
             ...
             am-1,0*x0 + ... + am-1,n-1*xn-1 <= bm-1

The LP has n decision variables x0, ..., xn-1 and m constraints.
The data is given in the form of three lists:
    - list_c: a list of size n containing objective coefficients.
    - list_a: a list of m lists, each of size n, representing the constraint coefficients (matrix A).
    - list_b: a list of size m representing the RHS coefficients of each inequality.

The goal is to:
1. Setup the LP model in PuLP.
2. Solve it.
3. Return a tuple (is_feasible, is_bounded, opt_sol).

==========================================================================================
2. Explanation (Arabic):
------------------------
المسألة تطلب استخدام مكتبة `Pulp` في بايثون لصياغة وحل مسائل البرمجة الخطية (Linear Programming).

الفكرة الأساسية:
- لدينا دالة هدف نريد تعظيمها: `max c^T * x`
- لدينا قيود على المتغيرات على شكل متباينات: `A * x <= b`
- المدخلات عبارة عن 3 قوائم:
    1. `list_c`: معاملات دالة الهدف (حجمها n).
    2. `list_a`: مصفوفة القيود (حجمها m × n).
    3. `list_b`: معاملات الطرف الأيمن للقيود (حجمها m).

الكود يقوم بالآتي:
1. التحقق من صحة أحجام المدخلات.
2. إنشاء متغيرات القرار `x0, x1, ..., xn-1`.
3. إضافة دالة الهدف إلى النموذج.
4. إضافة القيود `A * x <= b` إلى النموذج.
5. حل المسألة باستخدام solver (`PULP_CBC_CMD`).
6. إرجاع النتيجة على شكل `(is_feasible, is_bounded, opt_sol)`.

==========================================================================================
3. Code Implementation:
-----------------------
"""

from pulp import *

def formulate_lp_problem(m, n, list_c, list_a, list_b):
    # Assert that the data is compatible.
    assert n > 0
    assert m > 0
    assert len(list_c) == n
    assert len(list_a) == len(list_b) and len(list_b) == m
    assert all(len(l) == n for l in list_a)

    # Create a LP Model 
    lpModel = LpProblem('LPProblem', LpMaximize)

    ## 1. Create all the decision variables and store all the decision variables in a list
    decision_vars = [LpVariable(f'x{i}', None, None) for i in range(n)]

    ## 2. Create the objective function
    lpModel += lpSum([list_c[i] * decision_vars[i] for i in range(n)]), "Objective"

    ## 3. Create all the constraints
    for i in range(m):
        lhs = lpSum([list_a[i][j] * decision_vars[j] for j in range(n)])
        lpModel += (lhs <= list_b[i]), f"Constraint_{i}"

    # Solve the LP
    lpModel.solve(PULP_CBC_CMD(msg=False))
    status = LpStatus[lpModel.status]

    # Interpret status and return appropriate values
    if status == 'Optimal':
        sols = [value(v) for v in decision_vars]
        return (True, True, sols)
    elif status == 'Unbounded':
        return (True, False, None)
    else:  # 'Infeasible' or other failure modes
        return (False, False, None)

"""
==========================================================================================
4. Time Complexity Analysis:
----------------------------
- Building the model: O(m * n) because we loop over all constraints and all variables to construct the objective and constraints.
- Solving the LP: The actual solving time depends on the underlying solver (CBC). While the simplex method has exponential worst-case time complexity, it runs in polynomial time in practice for most real-world problems. Interior point methods are polynomial (O(n^3 L)).
==========================================================================================
"""

# ------------------- Test Cases -------------------
if __name__ == "__main__":
    # Test 1: Feasible and Bounded
    m = 4
    n = 3
    list_c = [1, 1, 1]
    list_a = [ [2, 1, 2], [1, 0, 0], [0, 1, 0], [0, 0, -1]]
    list_b = [5, 7, 9, 4]
    (is_feas, is_bnded, sols) = formulate_lp_problem(m, n, list_c, list_a, list_b)
    assert is_feas, 'The LP should be feasible -- your code returns infeasible'
    assert is_bnded, 'The LP should be bounded -- your code returns unbounded '
    print(f"Test 1 Solutions: {sols}")
    assert abs(sols[0] - 2.0) <= 1E-04 , 'x0 must be 2.0'
    assert abs(sols[1] - 9.0) <= 1E-04 , 'x1 must be 9.0'
    assert abs(sols[2] + 4.0) <= 1E-04 , 'x2 must be -4.0'
    print('Test 1 Passed: 3 points!')

    # Test 2: Unbounded problem
    m = 5
    n = 4 
    list_c = [-1, 2, 1, 1]
    list_a = [ [ 1, 0, -1, 2], [2, -1, 0, 1], [1, 1, 1, 1], [1, -1, 1, 1], [0, -1, 0, 1]]
    list_b = [3, 4, 5, 2.5, 3]
    (is_feas, is_bnded, sols) = formulate_lp_problem(m, n, list_c, list_a, list_b)
    assert is_feas, "The LP should be feasible. But your code returns a status of infeasible."
    assert not is_bnded, "The LP should be unbounded but your code returns a status of bounded."
    print('Test 2 Passed: 3 points')

    # Test 3: Infeasible problem
    m = 4
    n = 3
    list_c = [1, 1, 1]
    list_a = [ [-2, -1, -2], [1, 0, 0], [0, 1, 0], [0, 0, 1]]
    list_b = [-8, 1, 1, 1]
    (is_feas, is_bnded, sols) = formulate_lp_problem(m, n, list_c, list_a, list_b)
    assert not is_feas, 'The LP should be infeasible -- your code returns feasible'
    print('Test 3 Passed: 3 points!')

    # Test 4: Advanced check
    n = 15
    m = 16
    list_c = [1]*n 
    list_c[6] = list_c[6]+1
    list_a = []
    list_b = []
    for i in range(n):
        lst = [0]*n
        lst[i] = -1
        list_a.append(lst)
        list_b.append(0)
    list_a.append([1]*n)
    list_b.append(1)
    (is_feas, is_bnded, sols) = formulate_lp_problem(m, n, list_c, list_a, list_b)
    assert is_feas, 'Problem is feasible but your code returned infeasible'
    assert is_bnded, 'Problem is bounded but your code returned unbounded'
    print(f"Test 4 Solutions: {sols}")
    assert abs(sols[6] - 1.0)  <= 1E-03, 'Solution does not match expected one'
    assert all( [abs(sols[i]) <= 1E-03 for i in range(n) if i != 6]) , 'Solution does not match expected one'
    print('Test 4 Passed: 3 points!')

    print("All tests passed: 12 points!")
