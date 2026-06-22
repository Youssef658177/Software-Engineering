"""
Problem 2: LP formulation for an investment problem (English & Arabic Explanation)
==================================================================================
1. Problem Statement (English):
-------------------------------
Welcome to the world of finance! We are interested in investing in a portfolio of various stocks where we wish to maximize the overall return (profit/gain) on the investment but at the same time we do not want our investment to be diversified and the Price-to-Earnings (PE) ratio to be not too high, etc., in order to mitigate risk.

Given:
- Budget: B > 0 (Total budget available, e.g., B = 10,000).
- 6 Stocks (IBM, META, Astra-Zeneca, Pfizer, Unilever, Procter-Gamble) with:
    - Expected Return per unit
    - Current price per unit
    - Earnings per unit
    - Market category (Tech, HealthCare, Commodities)

We want to maximize total expected return subject to:
1. Total cost of investment <= B.
2. Investment amounts must be non-negative (x_i >= 0).
3. Investment must be balanced (amount in each market category is between 1/6 and 2/3 of total budget B).
4. The Price/Earnings ratio of the overall portfolio must not exceed 15.

==================================================================================
2. Explanation (Arabic):
------------------------
المسألة تطلب بناء نموذج برمجة خطية (Linear Programming) لاختيار محفظة استثمارية تحقق أعلى عائد ممكن، مع مراعاة عدة قيود مالية واستثمارية.

البيانات (من الجدول في الصورة):
- الأسهم: 6 أسهم مختلفة (من شركات Tech، Health، Commodities).
- المتغيرات: `x1` إلى `x6` تمثل عدد الوحدات المشتراة من كل سهم (يمكن أن تكون كسوراً).

القيود المطلوبة:
1. **الميزانية:** إجمالي التكلفة (Price × Quantity) <= 10,000.
2. **التنويع (Diversification):** الاستثمار في كل قطاع (Tech, Health, Comm) يجب أن يكون:
   - أكبر من أو يساوي 1/6 من الميزانية (لضمان التنويع الأدنى).
   - أقل من أو يساوي 2/3 من الميزانية (لتجنب التركيز الزائد).
3. **نسبة السعر إلى الربح (P/E Ratio):** يجب أن تكون النسبة الكلية للمحفظة <= 15.

الكود أدناه يستخدم مكتبة `PuLP` لصياغة هذه القيود وحل المسألة، وقد تم صياغتها جميعاً بدقة.

==================================================================================
3. Conceptual Answers (From Images):
------------------------------------
(أ) Objective function:
    Maximize Z = 25*x1 + 20*x2 + 3*x3 + 1.5*x4 + 3*x5 + 4.5*x6

(ب) List of Constraints:
    1. Budget: 129*x1 + 286*x2 + 72.29*x3 + 38*x4 + 52*x5 + 148*x6 <= 10,000
    
    2. Tech Category Constraints (1/6 to 2/3 of B):
       Tech >= 1666.67  =>  129*x1 + 286*x2 >= 1666.67
       Tech <= 6666.67  =>  129*x1 + 286*x2 <= 6666.67
       
    3. Health Category Constraints:
       Health >= 1666.67  =>  72.29*x3 + 38*x4 >= 1666.67
       Health <= 6666.67  =>  72.29*x3 + 38*x4 <= 6666.67
       
    4. Commodities Category Constraints:
       Comm >= 1666.67  =>  52*x5 + 148*x6 >= 1666.67
       Comm <= 6666.67  =>  52*x5 + 148*x6 <= 6666.67

    5. P/E Ratio Constraint:
       (Total Price) <= 15 * (Total Earnings)
       Σ (Price_i - 15 * Earnings_i) * x_i <= 0

==================================================================================
4. Code Implementation:
-----------------------
"""

from pulp import *

# -------------------------------
# Data (Updated to match the table)
# -------------------------------
B = 10000

prices   = [129, 286, 72.29, 38, 52, 148]       # Price/Unit
returns  = [25, 20, 3, 1.5, 3, 4.5]             # Expected Return/Unit
earnings = [1.9, 8.1, 1.5, 5, 2.5, 5.2]         # Earnings/Unit

# Market categories
tech_idx   = [0, 1]
health_idx = [2, 3]
comm_idx   = [4, 5]

# -------------------------------
# Linear Programming Model
# -------------------------------
lpModel = LpProblem('InvestmentProblem', LpMaximize)

# 1. Decision variables (Continuous shares to allow fractions)
x = [LpVariable(f'x{i+1}', lowBound=0, cat='Continuous') for i in range(6)]

# 2. Objective: maximize expected return
lpModel += lpSum(returns[i] * x[i] for i in range(6)), "Total_Expected_Return"

# 3. Constraints

# (a) Budget constraint: total cost <= B
lpModel += lpSum(prices[i] * x[i] for i in range(6)) <= B, "Budget"

# (b) Diversification: each category between 1/6 B and 2/3 B
lpModel += lpSum(prices[i] * x[i] for i in tech_idx)   >= (1/6) * B, "Tech_min"
lpModel += lpSum(prices[i] * x[i] for i in tech_idx)   <= (2/3) * B, "Tech_max"
lpModel += lpSum(prices[i] * x[i] for i in health_idx) >= (1/6) * B, "Health_min"
lpModel += lpSum(prices[i] * x[i] for i in health_idx) <= (2/3) * B, "Health_max"
lpModel += lpSum(prices[i] * x[i] for i in comm_idx)   >= (1/6) * B, "Comm_min"
lpModel += lpSum(prices[i] * x[i] for i in comm_idx)   <= (2/3) * B, "Comm_max"

# (c) Price/Earnings ratio <= 15
# Derivation: Total Price / Total Earnings <= 15  =>  Total Price - 15 * Total Earnings <= 0
#             Σ (Price_i - 15 * Earnings_i) * x_i <= 0
lpModel += lpSum((prices[i] - 15 * earnings[i]) * x[i] for i in range(6)) <= 0, "PE_ratio"

# -------------------------------
# Solve and output
# -------------------------------
lpModel.solve()

print("Optimization Results:")
print("=" * 40)
for v in lpModel.variables():
    print(f"{v.name} = {v.varValue}")
print("=" * 40)
print(f"Maximum Expected Return = {value(lpModel.objective)}")

# -------------------------------
# Assertion Tests
# -------------------------------
expected_return = 1098.59
actual_return = value(lpModel.objective)
print(f"\nChecking solution against expected value ({expected_return})...")
assert abs(actual_return - expected_return) <= 0.1, f"Test failed: Expected {expected_return}, got {actual_return}"
print("Test Passed Successfully!")
