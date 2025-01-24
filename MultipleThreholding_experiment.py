import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Baca data hasil Kalman Filter dari file Excel
file_path = 'E:\\PENS\\Semester 7\\Progress PA\\codingan\\Program\\Praproses_Kalman_IP2_IP3_IP4_Optimized.xlsx'

# Pastikan worksheet tersedia
workbook = pd.ExcelFile(file_path)
print("Available sheets:", workbook.sheet_names)

# Menggunakan sheet pertama sebagai fallback jika nama 'KalmanFilter' tidak ditemukan
sheet_name = 'Sheet1' if 'Sheet1' in workbook.sheet_names else workbook.sheet_names[0]

df = pd.read_excel(file_path, sheet_name=sheet_name)

# Ambil kolom hasil Kalman Filter
kalman_ip2 = df['IP2'].values
kalman_ip3 = df['IP3'].values
kalman_ip4 = df['IP4'].values

# Fungsi untuk menghitung ambang batas berdasarkan CDF dengan formula yang diberikan
def calculate_thresholds(data, m):
    dist = stats.norm(loc=np.mean(data), scale=np.std(data))
    thresholds = [dist.ppf(k / (2**m)) for k in range(1, 2**m)]
    return thresholds

# Fungsi untuk melakukan quantization berdasarkan ambang batas
def multi_threshold_quantization(data, thresholds):
    return np.digitize(data, bins=thresholds)

# Fungsi untuk konversi ke Gray Code
def gray_code(n):
    return n ^ (n >> 1)

# Fungsi untuk konversi dari Gray Code ke Biner
def gray_to_binary(gray):
    binary = gray
    shift = gray >> 1
    while shift != 0:
        binary ^= shift
        shift >>= 1
    return binary

# Fungsi untuk konversi hasil Gray Code ke string biner
def gray_code_to_binary_string(gray, bit_length):
    binary = gray_to_binary(gray)
    return format(binary, f'0{bit_length}b')

# Set nilai m (jumlah bit kuantisasi)
m = 3  # misal: 3 bit kuantisasi menghasilkan 8 level (0-7)
bit_length = m  # Set panjang bit sesuai jumlah level

# Hitung thresholds dan kuantisasi data
thresholds_ip2 = calculate_thresholds(kalman_ip2, m)
thresholds_ip3 = calculate_thresholds(kalman_ip3, m)
thresholds_ip4 = calculate_thresholds(kalman_ip4, m)

quantized_ip2 = multi_threshold_quantization(kalman_ip2, thresholds_ip2)
quantized_ip3 = multi_threshold_quantization(kalman_ip3, thresholds_ip3)
quantized_ip4 = multi_threshold_quantization(kalman_ip4, thresholds_ip4)

# Konversi hasil kuantisasi ke Gray Code, lalu ke Biner
binary_ip2 = [gray_code_to_binary_string(gray_code(level), bit_length) for level in quantized_ip2]
binary_ip3 = [gray_code_to_binary_string(gray_code(level), bit_length) for level in quantized_ip3]
binary_ip4 = [gray_code_to_binary_string(gray_code(level), bit_length) for level in quantized_ip4]

# Simpan hanya hasil biner ke Excel
output_df = pd.DataFrame({
    'Binary_IP2': binary_ip2,
    'Binary_IP3': binary_ip3,
    'Binary_IP4': binary_ip4
})
output_file_path = 'Final_Binary_MultiThreshold.xlsx'
output_df.to_excel(output_file_path, index=False, engine='openpyxl')

print(f'Hasil bit sequence dalam format biner disimpan di {output_file_path}')

# Plot hasil kuantisasi untuk memverifikasi
def plot_quantization(data, quantized, thresholds, title):
    plt.figure(figsize=(10, 6))
    plt.plot(data, label='Original Data', linestyle='--', alpha=0.7)
    plt.scatter(range(len(quantized)), quantized, color='red', label='Quantized Levels', s=10)
    for threshold in thresholds:
        plt.axhline(y=threshold, color='green', linestyle=':', label=f'Threshold = {threshold:.2f}')
    plt.title(f'Multi-Threshold Quantization - {title}')
    plt.xlabel('Data Index')
    plt.ylabel('RSS Value / Quantized Level')
    plt.legend()
    plt.grid(True)
    plt.show()

# Plot untuk IP2, IP3, dan IP4
plot_quantization(kalman_ip2, quantized_ip2, thresholds_ip2, 'IP2')
plot_quantization(kalman_ip3, quantized_ip3, thresholds_ip3, 'IP3')
plot_quantization(kalman_ip4, quantized_ip4, thresholds_ip4, 'IP4')
