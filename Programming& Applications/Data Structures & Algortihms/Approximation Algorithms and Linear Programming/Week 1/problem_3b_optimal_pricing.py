"""
Problem 3B: Optimal Pricing Model (English & Arabic Explanation)
=================================================================
1. Problem Statement (English):
-------------------------------
Let us consider a variant of the optimal transportation problem where we have the same data including the starting and desired configurations:
- Source locations: (x_i, y_i), weights w_i
- Target locations: (x'_j, y'_j), weights w'_j

The cost of transporting one unit weight from source i to target j is given by the Euclidean distance D_{i,j}.

Instead of deriving the transportation plan, we focus on setting purchase/sale prices:
- At each source location i, we set a price p_i per unit.
- At each target location j, we set a price p'_j per unit.

Constraint: For each source i and target j, the price difference p'_j - p_i must be less than or equal to D_{i,j} (Economic constraint to prevent competitors from undercutting us).

Goal: Maximize the revenue = Σ_{j} p'_j * w'_j - Σ_{i} p_i * w_i.

=================================================================
2. Explanation (Arabic):
------------------------
في هذه النسخة من مسألة النقل المثلى، بدلاً من إيجاد خطة النقل، نقوم بحساب "أسعار البيع والشراء المثلى" لتعظيم الأرباح.
المسألة تُصاغ كمسألة برمجة خطية (Dual LP) مزدوجة للمسألة الأصلية:
- لدينا أسعار للمصادر (Source Prices) وأسعار للوجهات (Destination Prices).
- القيد الأساسي: فرق السعر بين الوجهة والمصدر لا يمكن أن يتجاوز تكلفة النقل الفعلية بينهما (`p'_j - p_i <= D_{i,j}`). هذا يمنع المنافسين من تقديم عرض أفضل.
- دالة الهدف: تعظيم الفرق بين إيرادات البيع في الوجهات وتكلفة الشراء من المصادر: `max Σ p'_j * w'_j - Σ p_i * w_i`.
- الحل باستخدام مكتبة `PuLP` سهل، ونتيجة الربح الناتجة من هذا النموذج المزدوج يجب أن تساوي تماماً التكلفة الدنيا للنقل من المسألة السابقة (Primal Problem)، مما يؤكد صحة النموذجين (كما هو موضح في الاختبارات).

=================================================================
3. Code Implementation:
-----------------------
"""

from pulp import *
from math import sqrt

def calculate_distance(a, b):
    (xa, ya) = a
    (xb, yb) = b
    return sqrt((xa - xb)**2 + (ya - yb)**2)

def compute_optimal_prices(source_coords, source_weights, dest_coords, dest_weights):
    n = len(source_coords)
    assert (n == len(source_weights))
    m = len(dest_coords)
    assert (m == len(dest_weights))
    assert sum(source_weights) == sum(dest_weights)

    # Create maximization problem (LP Model for the Dual)
    lpModel = LpProblem('Transportation_Dual', LpMaximize)

    # Decision variables (unrestricted in sign: can be positive or negative)
    source_vars = [LpVariable(f'source_{i}', lowBound=None) for i in range(n)]
    dest_vars   = [LpVariable(f'dest_{j}',   lowBound=None) for j in range(m)]

    # Objective: maximize Σ (destination_weight * destination_price) - Σ (source_weight * source_price)
    lpModel += (lpSum(dest_vars[j] * dest_weights[j] for j in range(m))
                - lpSum(source_vars[i] * source_weights[i] for i in range(n)))

    # Dual constraints: v_j - u_i <= c_ij (Price difference cannot exceed transport cost)
    for i in range(n):
        for j in range(m):
            lpModel += (dest_vars[j] - source_vars[i] <=
                        calculate_distance(source_coords[i], dest_coords[j]))

    # Solve the LP
    lpModel.solve(PULP_CBC_CMD(msg=False))   # suppress solver output

    # Extract solution
    source_prices = [v.varValue for v in source_vars]
    dest_prices   = [v.varValue for v in dest_vars]

    return (source_prices, dest_prices)

"""
=================================================================
4. Time & Space Complexity Analysis:
------------------------------------
- Time Complexity: O(n * m) 
  بناء نموذج LP يتطلب إضافة `n * m` قيد (قيود المسافات). خوارزمية الحل (مثل CBC) تعمل بكفاءة عالية على هذا الحجم من القيود.

- Space Complexity: O(n * m)
  لتخزين مصفوفة القيود والمسافات داخل نموذج الـ LP.
=================================================================
"""

# ------------------- Test Cases -------------------
if __name__ == "__main__":
    # Test 1: 7 points
    source_coords = [ (1,5), (4,1), (5,5) ]
    source_weights = [9, 4, 5]
    dest_coords = [ (2,2), (6,6) ]
    dest_weights = [9, 9]
    n = 3
    m = 2
    (source_prices, dest_prices) = compute_optimal_prices(source_coords, source_weights, dest_coords, dest_weights)
    
    # Calculate profit
    profit = sum([pi*wi for (pi, wi) in zip(dest_prices, dest_weights)]) - sum([pj*wj for (pj, wj) in zip(source_prices, source_weights)])
    print(f'Test 1 Profit: {profit}')
    assert(abs(profit - 52.22) <= 1E-01), f'Error: Expected profit is {52.22} obtained: {profit}'
    print('Test Passed: 7 points\n')


    # Test 2: 8 points
    source_coords = [ (i,1) for i in range(20) ]
    source_weights = [10] * 20
    dest_coords = [ (6,i+5) for i in range(8) ] + [ (14,i+5) for i in range(8) ] 
    dest_weights = [12.5]*16
    n = 20
    m = 16
    (src_prices, dest_prices) = compute_optimal_prices(source_coords, source_weights, dest_coords, dest_weights)
    
    profit = sum([pi*wi for (pi, wi) in zip(dest_prices, dest_weights)]) - sum([pj*wj for (pj, wj) in zip(src_prices, source_weights)])
    print(f'Test 2 Profit: {profit}')
    assert(abs(profit - 1598.11) <= 1E-1), f'Error: Expected profit is {1598.11} obtained: {profit}'
    print('Test Passed: 8 points')
