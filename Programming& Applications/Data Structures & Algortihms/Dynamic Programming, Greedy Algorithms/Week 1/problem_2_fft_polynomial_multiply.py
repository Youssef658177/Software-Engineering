"""
Problem 2: Polynomial Multiplication using FFT (English & Arabic Explanation)
=============================================================================
1. Problem Statement (English):
-------------------------------
We studied polynomial multiplication using FFT in class. Recall the algorithm given two polynomials a(x) = a0 + a1*x + ... + a_{n-1}*x^{n-1} and b(x) = b0 + b1*x + ... + b_{m-1}*x^{m-1}:

1. Pad the coefficients of a, b with zero coefficients to make up two polynomials of degree m + n - 2 (expected size of the result).
2. Compute FFTs of [a0, ..., a_{n-1}, 0, ..., 0] and [b0, ..., b_{m-1}, 0, ..., 0].
3. Let [A0, ..., A_{m+n-2}] and [B0, ..., B_{m+n-2}] be the resulting FFT sequences.
4. Multiply the FFT sequences: [A0 * B0, ..., A_{m+n-2} * B_{m+n-2}].
5. Compute the inverse FFT to obtain the polynomial c(x) = a(x)b(x).

Implement polynomial multiplication using FFT. Use the numpy.fft package.

================================================================
2. Explanation (Arabic):
------------------------
المسألة تطلب تنفيذ ضرب كثيرات الحدود (Polynomials) باستخدام خوارزمية التحويل السريع فورييه (FFT).

الخطوات الرئيسية للكود:
1. تحديد الحجم النهائي للمعادلة الناتجة `n = len(a) + len(b) - 1`.
2. إيجاد `fft_size` وهو أكبر قوة للعدد 2 (Power of 2) أكبر من أو يساوي `n`، وذلك لضمان كفاءة خوارزمية FFT.
3. حشو (Padding) قوائم المعاملات (`a_coeff_list`, `b_coeff_list`) بالأصفار ليصبح طول كل منها `fft_size`.
4. حساب تحويل فورييه (`fft`) للقائمتين، ثم ضربهما نقطة بنقطة (Point-wise multiplication).
5. حساب التحويل العكسي (`ifft`) للناتج، ثم استخراج الجزء الحقيقي (Real part) للتخلص من الأخطاء العائمة (Floating point errors) الصغيرة جداً.
6. إرجاع قائمة المعاملات للناتج النهائي.

التعقيد الزمني لهذه الخوارزمية هو `O(N log N)` حيث `N` هو `fft_size`، وهو أسرع بكثير من الضرب المباشر `O(n*m)`.

================================================================
3. Code Implementation:
-----------------------
"""

from numpy.fft import fft, ifft
from numpy import real, imag

def polynomial_multiply(a_coeff_list, b_coeff_list):
    # 1. تحديد الحجم المطلوب لـ FFT
    # درجة النتيجة هي (طول أ + طول ب - 2)
    # عدد النقاط المطلوبة يجب أن يكون قوة للعدد 2 (Power of 2) وأكبر من أو يساوي طول النتيجة
    n = len(a_coeff_list) + len(b_coeff_list) - 1
    fft_size = 1
    while fft_size < n:
        fft_size <<= 1  # مضاعفة الحجم حتى نصل لقوة 2
    
    # 2. حشو قوائم المعاملات بالأصفار ليصبح طولها fft_size
    a_padded = a_coeff_list + [0] * (fft_size - len(a_coeff_list))
    b_padded = b_coeff_list + [0] * (fft_size - len(b_coeff_list))
    
    # 3. حساب FFT للقائمتين
    fft_a = fft(a_padded)
    fft_b = fft(b_padded)
    
    # 4. ضرب نتائج الـ FFT نقطة بنقطة (Point-wise multiplication)
    fft_product = [fft_a[i] * fft_b[i] for i in range(fft_size)]
    
    # 5. حساب الـ Inverse FFT للحصول على معاملات الضرب
    product_complex = ifft(fft_product)
    
    # 6. استخراج الأجزاء الحقيقية فقط (للتخلص من الأجزاء التخيلية الصغيرة جداً الناتجة عن أخطاء الحساب)
    product_real = [real(x) for x in product_complex[:n]]
    
    return product_real

"""
================================================================
4. Time & Space Complexity Analysis:
------------------------------------
- Time Complexity: O(N log N)
  حيث N هو حجم FFT (Power of 2). N يكون عادة بين n و 2n.
  تعمل خوارزمية FFT في وقت O(N log N).

- Space Complexity: O(N)
  لتخزين المصفوفات الممهدة (Padded arrays) ونتائج الـ FFT.

================================================================
5. Test Cases:
--------------
"""
def check_poly(lst1, lst2):
    print(f'Your code found: {lst1}')
    print(f'Expected: {lst2}')
    assert(len(lst1) == len(lst2)), 'Lists have different lengths'
    for (k,j) in zip(lst1, lst2):
        assert abs(k-j)<= 1E-05, 'Polynomials do not match'
    print('Passed!')

if __name__ == "__main__":
    print('-------')
    print('Test # 1')
    # multiply (1 + x - x^3) with (2 - x + x^2)
    a = [1, 1, 0, -1]
    b = [2, -1, 1]
    c = polynomial_multiply(a,b)
    assert(len(c) == 6)
    print(f'c={c}')
    check_poly(c, [2,1,0,-1,1,-1])
    
    print('-------')
    print('Test # 2')
    # multiply 1 - x + x^2 + 2 x^3 + 3 x^5 with -x^2 + x^4 + x^6
    a = [1, -1, 1, 2, 0, 3]
    b = [0, 0, -1, 0, 1, 0, 1]
    c = polynomial_multiply(a,b)
    assert(len(c) == 12)
    print(f'c={c}')
    check_poly(c, [0, 0, -1, 1, 0, -3, 2, -2, 1, 5, 0, 3])
    
    print('-------')
    print('Test # 3')
    # multiply 1 - 2x^3 + x^7 - 11 x^11 with 2 - x^4 - x^6 + x^8
    a = [1, 0, 0, -2, 0, 0, 0, 1, 0, 0, 0, -11]
    b = [2, 0, 0, 0, -1, 0, -1, 0, 1]
    c = polynomial_multiply(a, b)
    assert(len(c) == 20)
    print(f'c={c}')
    check_poly(c, [2, 0, 0, -4, -1, 0, -1, 4, 1, 2, 0, -25, 0, -1, 0, 12, 0, 11, 0, -11])
    
    print('All tests passed (10 points!)')
