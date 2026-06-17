"""
Problem 1: Makespan Scheduling (English & Arabic Explanation)
==============================================================
1. Problem Statement (English):
-------------------------------
Let us consider n jobs that take times T1, ..., Tn to complete where each Ti > 0. We have m >= 2 processors to process these jobs. Our goal is to assign these jobs to the processors.

An assignment is modeled as an array A : [A1, ..., An] wherein each Ai represents the number of the processor to which job i is assigned. Eg., A3 = 4 means that job number 3 is assigned to processor 4. Therefore each Ai ∈ {1, ..., m}.

Once the assignment is complete, each processor runs the jobs assigned to it under some order.

Question 1: Let Mj be the total time taken by some processor j to complete all the jobs assigned to it. Write down an expression for Mj.
Question 2: Consider jobs with times [T1: 2, T2: 2, T3: 2, T4: 2, T5: 2, T6: 2, T7: 3] and m = 3 processors. Assignment A: [A1: 1, A2: 1, A3: 2, A4: 2, A5: 3, A6: 3, A7: 2]. Calculate the makespan.

MakeSpan(A) = max(Mj) where j = 1..m, denoting the maximum total time taken by any processor.

================================================================
2. Explanation (Arabic):
------------------------
المسألة بتتعامل مع "جدولة المهام" (Scheduling). عندنا n من المهام، كل مهمة ليها وقت تنفيذ معين T_i، وعندنا m من المعالجات (Processors) بنشتغل بالتوازي. المطلوب هو توزيع المهام على المعالجات بحيث يكون "الوقت الكلي للإنجاز" (Makespan) أقل ما يمكن. الوقت الكلي هو أقصى وقت بيقضيه أي معالج لإنجاز المهام الموكلة إليه.

الكود المطلوب (Part A) هو مجرد حساب الـ Makespan لتوزيع معين:
- بنمر على كل المهام، ونضيف وقتها للمعالج المخصص لها.
- الـ Makespan هو أكبر مجموع أوقات تم تجميعه لأي معالج.

**إجابة Question 1:** M_j = مجموع أوقات جميع المهام المخصصة للمعالج j.
**إجابة Question 2:**
- المعالج 1: المهمة 1 + المهمة 2 = 2 + 2 = 4
- المعالج 2: المهمة 3 + المهمة 4 + المهمة 7 = 2 + 2 + 3 = 7
- المعالج 3: المهمة 5 + المهمة 6 = 2 + 2 = 4
- الـ Makespan هو أقصى قيمة = 7.

================================================================
3. Code Implementation:
-----------------------
"""

def compute_makespan(times, m, assign):
    """
    Computes the makespan of a given job assignment.
    times: list of execution times for each job.
    m: number of processors.
    assign: list where assign[i] is the processor ID (0-indexed) for job i.
    """
    # Initialize an array to store the total time for each processor
    processor_times = [0] * m
    
    # Iterate through each job
    for i in range(len(times)):
        # Get the processor assigned to this job
        processor_id = assign[i]
        # Add the job time to the assigned processor's total
        processor_times[processor_id] += times[i]
        
    # The makespan is the maximum load among all processors
    return max(processor_times)

"""
================================================================
4. Time & Space Complexity Analysis:
------------------------------------
- Time Complexity: O(n) 
  حيث n هو عدد المهام. الخوارزمية بتستخدم حلقة واحدة بتعدي على جميع المهام لتجميع الأوقات.
- Space Complexity: O(m)
  لتخزين مصفوفة الأوقات التراكمية للمعالجات (processor_times) التي طولها m.
================================================================
"""

# ------------------- Test Cases -------------------
if __name__ == "__main__":
    print('Test 1 ... ', end = '')
    times = [2, 2, 2, 2, 3, 3, 2]
    assigns = [0, 0, 0, 0, 1, 1, 2]
    m = 3
    s = compute_makespan(times, m, assigns)
    assert s == 8, f'Expected makespan is 8, your code returned: {s}'
    print(' passed!')

    print('Test 2 ...', end='')
    times = [2, 1, 2, 2, 1, 3, 2, 1, 1, 3]
    assigns = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
    m = 3
    s = compute_makespan(times, m, assigns)
    assert s == 10, f' Expected makespan is 10, your code returned {s}'
    print('  passed!')
    
    print('Tests passed: 10 points!')
