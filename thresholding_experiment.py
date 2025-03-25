import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Load data hasil Kalman Filter dari Excel
file_path = r'E:\PENS\Semester 8\Final TA\Code\Ruang Eksperimen\experimen 1\Program_1\files\hasil_kalman.xlsx'
df = pd.read_excel(file_path, sheet_name='Sheet1')

# Ambil data kolom DOSS1, DOSS2, dan DOSS3
doss1 = df['Kalman DOSS1'].values
doss2 = df['Kalman DOSS2'].values
doss3 = df['Kalman DOSS3'].values

# Fungsi hitung threshold dengan CDF
def calculate_thresholds(data, m):
    dist = stats.norm(loc=np.mean(data), scale=np.std(data))
    thresholds = [dist.ppf(k / (2**(m-1))) for k in range(1, 2**(m-1))]
    return thresholds

# Fungsi kuantisasi multi-level
def multi_threshold_quantization(data, thresholds):
    return np.digitize(data, bins=thresholds)

# Fungsi Gray Code
def gray_code(n):
    return n ^ (n >> 1)

# Fungsi konversi Gray ke biner
def gray_to_binary(gray):
    binary = gray
    shift = gray >> 1
    while shift != 0:
        binary ^= shift
        shift >>= 1
    return binary

def gray_code_to_binary_string(gray, bit_length):
    binary = gray_to_binary(gray)
    return format(binary, f'0{bit_length}b')

# Parameter kuantisasi (m bit total)
m = 3
bit_length = m - 1  # jumlah bit dari kuantisasi level (tanpa fading trend)

# Hitung thresholds dan kuantisasi data (LANGKAH 1 - yang BENAR)
thresholds_doss1 = calculate_thresholds(doss1, m)
thresholds_doss2 = calculate_thresholds(doss2, m)
thresholds_doss3 = calculate_thresholds(doss3, m)

quantized_doss1 = multi_threshold_quantization(doss1, thresholds_doss1)
quantized_doss2 = multi_threshold_quantization(doss2, thresholds_doss2)
quantized_doss3 = multi_threshold_quantization(doss3, thresholds_doss3)

# Identifikasi fading trend secara eksplisit (LANGKAH 2 - BENAR)
median_doss1 = np.median(doss1)
median_doss2 = np.median(doss2)
median_doss3 = np.median(doss3)

fading_trend_doss1 = ['1' if val >= median_doss1 else '0' for val in doss1]
fading_trend_doss2 = ['1' if val >= median_doss2 else '0' for val in doss2]
fading_trend_doss3 = ['1' if val >= median_doss3 else '0' for val in doss3]

# Gabungkan fading trend dengan hasil quantisasi (LANGKAH 3 - BENAR)
m = 3
bit_length = m - 1

binary_doss1_final = [
    fading_trend_doss1[i] + gray_code_to_binary_string(gray_code(level), bit_length)
    for i, level in enumerate(quantized_doss1)
]

binary_doss2_final = [
    fading_trend_doss2[i] + gray_code_to_binary_string(gray_code(level), bit_length)
    for i, level in enumerate(quantized_doss2)
]

binary_doss3_final = [
    fading_trend_doss3[i] + gray_code_to_binary_string(gray_code(level), bit_length)
    for i, level in enumerate(quantized_doss3)
]

# Fungsi plot kuantisasi
def plot_quantization(data, quantized, thresholds, title):
    plt.figure(figsize=(10, 6))
    plt.plot(data, label='Original Data', linestyle='--', alpha=0.7)
    plt.scatter(range(len(quantized)), quantized, color='red', label='Quantized Levels', s=10)
    for threshold in thresholds:
        plt.axhline(y=threshold, color='green', linestyle=':', alpha=0.7)
    plt.title(f'Multi-Threshold Quantization - {title}')
    plt.xlabel('Data Index')
    plt.ylabel('RSS Value / Quantized Level')
    plt.legend()
    plt.grid(True)
    plt.show()

# Fungsi format vertikal
def format_binary_as_vertical(binary_data):
    return [digit for binary in binary_data for digit in binary]

# Simpan hasil vertikal ke Excel
formatted_df_vertical = pd.DataFrame({
    'Binary_DOSS1': format_binary_as_vertical(binary_doss1_final),
    'Binary_DOSS2': format_binary_as_vertical(binary_doss2_final),
    'Binary_DOSS3': format_binary_as_vertical(binary_doss3_final)
})
formatted_df_vertical.to_excel(r'E:\PENS\Semester 8\Final TA\Code\Ruang Eksperimen\experimen 1\Program_1\files\Final_RTQ_Binary_Vertical.xlsx', index=False, engine='openpyxl')

print('Hasil biner dalam format vertikal disimpan di Final_RTQ_Binary_Vertical.xlsx')

# Simpan hasil horizontal ke Excel
formatted_df_horizontal = pd.DataFrame({
    'Binary_DOSS1': binary_doss1_final,
    'Binary_DOSS2': binary_doss2_final,
    'Binary_DOSS3': binary_doss3_final
})
formatted_df_horizontal.to_excel(r'E:\PENS\Semester 8\Final TA\Code\Ruang Eksperimen\experimen 1\Program_1\files\Final_RTQ_Binary_Horizontal.xlsx', index=False, engine='openpyxl')

print('Hasil biner dalam format horizontal disimpan di Final_RTQ_Binary_Horizontal.xlsx')

# Plot hasil untuk verifikasi
plot_quantization(doss1, quantized_doss1, thresholds_doss1, 'DOSS1')
plot_quantization(doss2, quantized_doss2, thresholds_doss2, 'DOSS2')
plot_quantization(doss3, quantized_doss3, thresholds_doss3, 'DOSS3')
