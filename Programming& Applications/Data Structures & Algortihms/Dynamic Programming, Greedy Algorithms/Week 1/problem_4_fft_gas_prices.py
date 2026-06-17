"""
Problem 4: Time Series Analysis using FFT (English & Arabic Explanation)
========================================================================
1. Problem Statement (English):
-------------------------------
We have been given a file called `natural_gas_futures_weekly_all.csv` which is weekly data for natural gas futures from 8/2000 to 5/2021.

For convenience, the code below opens the CSV file and for each week, calculates the average of High and Low prices to get a list of weekly prices.
The goal is to use Fast Fourier Transform (FFT) to analyze the signal (weekly prices), split it into different frequency components (low, medium, high frequencies), and visualize each component.

We perform the following steps:
1. Load the CSV and extract the weekly price data.
2. Compute the FFT of the data.
3. Compute the corresponding frequency bins for the FFT result.
4. Define a function `select_all_items_in_freq_range(lo, hi)` to filter the FFT result based on frequency limits and return the inverse FFT (time domain signal) of those specific frequencies.
5. Split the price data into:
   - Frequencies < 1/year (Long-term trend).
   - Frequencies between 1/year and 1/quarter (Seasonal patterns).
   - Frequencies >= 1/quarter (Short-term noise).
6. Plot and verify that the sum of the components reconstructs the original signal perfectly.

========================================================================
2. Explanation (Arabic):
------------------------
المسألة تطلب تحليل سلسلة زمنية (Time Series) لأسعار الغاز الطبيعي باستخدام تحويل فورييه السريع (FFT).

الخطوات الأساسية في الكود:
1. قراءة ملف CSV واستخراج متوسط السعر الأسبوعي.
2. حساب تحويل فورييه (FFT) للإشارة، مما يحولها من مجال الزمن إلى مجال التردد.
3. حساب الترددات المقابلة لكل نقطة في خرج الـ FFT.
4. كتابة دالة `select_all_items_in_freq_range(lo, hi)` والتي تقوم بفلترة الـ FFT، بحيث تبقي فقط الترددات الموجودة بين `lo` و `hi`، وتقوم بحساب التحويل العكسي (IFFT) لإعادتها للمجال الزمني.
5. تقسيم الإشارة إلى ثلاثة مكونات:
   - الترددات المنخفضة (أقل من مرة في السنة): تمثل الاتجاه العام (Trend).
   - الترددات المتوسطة (بين مرة في السنة ومرة في الربع): تمثل التغيرات الموسمية (Seasonality).
   - الترددات العالية (أكبر من مرة في الربع): تمثل التقلبات العشوائية (Noise).
6. التأكد من أن مجموع المكونات الثلاثة يساوي الإشارة الأصلية، وهو ما يؤكد صحة التحليل.

========================================================================
3. Code Implementation:
-----------------------
"""

import csv
from matplotlib import pyplot as plt
from numpy.fft import fft, ifft
from numpy import real, imag

# --- 1. Load Data ---
file = open('natural_gas_futures_weekly_all.csv', 'r')
csv_handle = csv.DictReader(file)

weekly_prices = []
dates = []

for rows in csv_handle:
    dates.append(rows['Date'])
    # Calculate mid-price (average of High and Low)
    weekly_prices.append(0.5 * (float(rows['High']) + float(rows['Low'])))

file.close()

# --- 2. Compute FFT and Frequencies ---
fft_data = fft(weekly_prices)
N = len(fft_data)

# Calculate frequencies array. Frequencies are symmetric.
# fft_frequencies represents normalized frequencies between -0.5 and 0.5.
fft_frequencies = [k / N if k <= N//2 else (k - N) / N for k in range(N)]

# --- 3. Helper Function to Filter Frequencies ---
def select_all_items_in_freq_range(lo, hi):
    new_fft_data = []
    # Filter the FFT values based on frequency range
    for (fft_val, fft_freq) in zip(fft_data, fft_frequencies):
        # Keep if frequency is in positive range [lo, hi) OR negative range (-hi, -lo]
        if lo <= fft_freq < hi or -hi < fft_freq <= -lo:
            new_fft_data.append(fft_val)
        else:
            new_fft_data.append(0.0)
    # Perform inverse FFT on the filtered data
    filtered_data = ifft(new_fft_data)
    # Extract the real part (imaginary parts are near zero due to floating point errors)
    return [real(x) for x in filtered_data]

# --- 4. Split Signal into Components ---
# Since 1 year = 52 weeks:
# - Low frequency: less than 1 cycle per year
upto_1_year = select_all_items_in_freq_range(0, 1/52)
# - Medium frequency: 1 to 4 cycles per year (1 per quarter)
one_year_to_1_quarter = select_all_items_in_freq_range(1/52, 1/13)
# - High frequency: >= 4 cycles per year (less than a quarter)
less_than_1_quarter = select_all_items_in_freq_range(1/13, 10.0)

"""
========================================================================
4. Time & Space Complexity Analysis:
------------------------------------
- Time Complexity: O(N log N) for FFT computation (N is the number of weeks).
- Space Complexity: O(N) to store the price list and FFT results.

Note: While reading the CSV is O(N), the FFT dominates the running time.
========================================================================
"""

# ------------------- Visualization and Tests -------------------
if __name__ == "__main__":
    # Plotting the separated components
    plt.figure(figsize=(12, 6))
    plt.plot(upto_1_year, '-b', lw=2, label='< 1/year (Trend)')
    plt.plot(weekly_prices, '--r', lw=0.2, label='Original Prices')
    plt.xlabel('Week #')
    plt.ylabel('Price')
    plt.title('Frequency components < once/year')
    plt.legend()
    
    plt.figure(figsize=(12, 6))
    plt.plot(one_year_to_1_quarter, '-b', lw=2, label='1/year to 1/quarter')
    plt.plot(weekly_prices, '--r', lw=0.2, label='Original Prices')
    plt.title('Frequency components between once/year and once/quarter')
    plt.xlabel('Week #')
    plt.ylabel('Price')
    plt.legend()
    
    plt.figure(figsize=(12, 6))
    plt.plot(less_than_1_quarter, '-b', lw=2, label='> 1/quarter (Noise)')
    plt.plot(weekly_prices, '--r', lw=0.2, label='Original Prices')
    plt.title('Frequency components > once/quarter')
    plt.xlabel('Week #')
    plt.ylabel('Price')
    plt.legend()

    # Check if sum of components equals the original signal
    sum_components = [(v1 + v2 + v3) for (v1, v2, v3) in zip(upto_1_year, one_year_to_1_quarter, less_than_1_quarter)]
    plt.figure(figsize=(12, 6))
    plt.plot(sum_components, '-b', lw=2, label='Sum of Components')
    plt.plot(weekly_prices, '--r', lw=0.2, label='Original Prices')
    plt.title('Sum of all the components vs Original')
    plt.xlabel('Week #')
    plt.ylabel('Prices')
    plt.legend()
    
    # Final validation assertions
    N = len(weekly_prices)
    assert(len(fft_frequencies) == len(weekly_prices))
    assert(fft_frequencies[0] == 0.0)
    assert(abs(fft_frequencies[N//2] - 0.5) <= 0.05)
    assert(abs(fft_frequencies[N//4] - 0.25) <= 0.05)
    assert(abs(fft_frequencies[3*N//4] + 0.25) <= 0.05)
    assert(abs(fft_frequencies[1] - 1/N) <= 0.05)
    assert(abs(fft_frequencies[N-1] + 1/N) <= 0.05)

    for (v1, v2, v3, v4) in zip(weekly_prices, upto_1_year, one_year_to_1_quarter, less_than_1_quarter):
        assert ( abs(v1 - (v2 + v3 + v4)) <= 0.01), 'The components are not adding up'
    
    print('All tests OK -- 10 points!!')
    plt.show() # Show all plots at the end
