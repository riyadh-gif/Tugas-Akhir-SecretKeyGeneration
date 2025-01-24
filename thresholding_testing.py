import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Fungsi untuk memplot hasil kuantisasi
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

# Baca data hasil Kalman Filter dari file Excel
file_path = 'E:\\PENS\\Semester 7\\Progress PA\\codingan\\Program\\Praproses_Kalman_DOSS1_DOSS2_Optimized.xlsx'

# Pastikan worksheet tersedia
workbook = pd.ExcelFile(file_path)
print("Available sheets:", workbook.sheet_names)

# Menggunakan sheet yang sesuai, dalam hal ini 'Sheet1' atau sheet yang ada
sheet_name = 'Sheet1' if 'Sheet1' in workbook.sheet_names else workbook.sheet_names[0]

df = pd.read_excel(file_path, sheet_name=sheet_name)

# Ambil kolom DOSS1 dan DOSS2
doss1 = df['DOSS1'].values
doss2 = df['DOSS2'].values

# Fungsi untuk menghitung ambang batas berdasarkan CDF dengan formula yang diberikan
def calculate_thresholds(data, m):
    dist = stats.norm(loc=np.mean(data), scale=np.std(data))
    # Hitung threshold untuk 2^(m-1) level
    thresholds = [dist.ppf(k / (2**(m-1))) for k in range(1, 2**(m-1))]
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
    return format(binary, f'0{bit_length}b')  # Gunakan m-1 bit untuk ekstraksi

# Set nilai m (jumlah bit kuantisasi) yang ingin diekstrak
m = 3  # misal: 3 bit kuantisasi menghasilkan 8 level (0-7)
bit_length = m - 1  # Ekstrak m-1 bit per pengukuran

# Hitung thresholds dan kuantisasi data untuk DOSS1 dan DOSS2
thresholds_doss1 = calculate_thresholds(doss1, m)
thresholds_doss2 = calculate_thresholds(doss2, m)

quantized_doss1 = multi_threshold_quantization(doss1, thresholds_doss1)
quantized_doss2 = multi_threshold_quantization(doss2, thresholds_doss2)

# Konversi hasil kuantisasi ke Gray Code, lalu ke Biner dengan m-1 bit
binary_doss1 = [gray_code_to_binary_string(gray_code(level), bit_length) for level in quantized_doss1]
binary_doss2 = [gray_code_to_binary_string(gray_code(level), bit_length) for level in quantized_doss2]

# Mengubah data hasil kuantisasi menjadi format vertikal
def format_binary_as_vertical(binary_data):
    formatted_data = []
    for binary in binary_data:
        for digit in binary:  # Pisahkan setiap digit
            formatted_data.append(digit)
    return formatted_data

# Formatkan DOSS1 dan DOSS2 dalam format vertikal
formatted_binary_doss1 = format_binary_as_vertical(binary_doss1)
formatted_binary_doss2 = format_binary_as_vertical(binary_doss2)

# Buat DataFrame untuk hasil vertikal
max_length = max(len(formatted_binary_doss1), len(formatted_binary_doss2))
data_dict = {
    'Binary_DOSS1': formatted_binary_doss1 + [''] * (max_length - len(formatted_binary_doss1)),
    'Binary_DOSS2': formatted_binary_doss2 + [''] * (max_length - len(formatted_binary_doss2)),
}
output_df = pd.DataFrame(data_dict)

# Simpan hasil ke file Excel dalam format vertikal
output_file_path = 'Final_Binary_MultiThreshold_Vertical.xlsx'
output_df.to_excel(output_file_path, index=False, engine='openpyxl')

print(f'Hasil biner dalam format vertikal disimpan di {output_file_path}')

# Simpan hanya hasil biner ke Excel
output_df_horizontal = pd.DataFrame({
    'Binary_DOSS1': binary_doss1,
    'Binary_DOSS2': binary_doss2
})
output_file_path_horizontal = 'Final_Binary_MultiThreshold_Horizontal.xlsx'
output_df_horizontal.to_excel(output_file_path_horizontal, index=False, engine='openpyxl')

print(f'Hasil bit sequence dalam format biner disimpan di {output_file_path_horizontal}')

# Plot hasil kuantisasi untuk memverifikasi
plot_quantization(doss1, quantized_doss1, thresholds_doss1, 'DOSS1')
plot_quantization(doss2, quantized_doss2, thresholds_doss2, 'DOSS2')
