import numpy as np
import pandas as pd

# 1. إعداد البيانات وتطبيق الجبر الخطي (Linear Algebra)
# درجات 4 طلاب في 3 مواد (الرياضيات، البرمجة، المشروع)
# الصفوف تمثل الطلاب، الأعمدة تمثل المواد
student_names = ['Student_A', 'Student_B', 'Student_C', 'Student_D']
scores_matrix = np.array([
    [80, 90, 75],   # A: Math=80, Prog=90, Proj=75
    [95, 85, 90],   # B: Math=95, Prog=85, Proj=90
    [70, 75, 80],   # C: Math=70, Prog=75, Proj=80
    [60, 65, 70]    # D: Math=60, Prog=65, Proj=70
])
weights_vector = np.array([0.3, 0.5, 0.2]) # أوزان المواد: البرمجة لها الوزن الأكبر

# ضرب المصفوفات لحساب الدرجة النهائية المرجحة
final_scores_array = scores_matrix @ weights_vector
final_scores_series = pd.Series(final_scores_array, index=student_names)

print("--- 1. تطبيق الجبر الخطي ---")
print(f"الدرجات النهائية المرجحة:\n{final_scores_series.round(2)}\n")


# 2. التحليل الإحصائي (Statistical Analysis)
df_scores = pd.DataFrame(scores_matrix, columns=['Math', 'Programming', 'Project'], index=student_names)

print("--- 2. التحليل الإحصائي ---")
print(f"الوسط (Mean):\n{df_scores.mean().round(2)}")
print(f"\nالانحراف المعياري (Std Dev):\n{df_scores.std().round(2)}\n")


# 3. تطبيق نظرية المجموعات (Set Theory)
# أسماء الطلاب الذين حصلوا على 85 فما فوق في مادة البرمجة
excellent_programmers = set(df_scores[df_scores['Programming'] >= 85].index)
# أسماء الطلاب الذين حصلوا على 85 فما فوق في مادة المشروع
project_achievers = set(df_scores[df_scores['Project'] >= 85].index)

print("--- 3. تطبيق نظرية المجموعات ---")
# التقاطع: يستحقون الحافز في كلتا المادتين
incentive_intersection = excellent_programmers.intersection(project_achievers)
print(f"الطلاب الذين يستحقون حافز (تقاطع): {incentive_intersection}")

# الاتحاد: يستحقون مكافأة في إحداها على الأقل
reward_union = excellent_programmers.union(project_achievers)
print(f"الطلاب الذين يستحقون مكافأة (اتحاد): {reward_union}\n")


# 4. تطبيق المنطق والتصنيف (Logic and Classification)
pass_threshold = 70
project_min = 65

print("--- 4. تطبيق المنطق والتصنيف ---")
for student, score in final_scores_series.items():
    # المنطق: (الدرجة النهائية > 70) AND (درجة المشروع > 65)
    passed_logic = (score > pass_threshold) and (df_scores.loc[student, 'Project'] > project_min)
    status = "ناجح (Pass)" if passed_logic else "راسب (Fail)"
    print(f"الطالب {student}: الدرجة النهائية {score:.2f}، الحالة: {status}")
