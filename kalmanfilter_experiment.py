import openpyxl
import numpy as np
import time
import pandas as pd
import matplotlib.pyplot as plt

start = time.time()

# =========================================================================
# ============================== KALMAN FILTER ============================
start1 = time.time()
interval = 0.11

# Menggunakan openpyxl untuk membaca file .xlsx
file_path = 'E:\\PENS\\Semester 7\\Progress PA\\codingan\\Program\\channelprob_skenario1.xlsx'
workbook = openpyxl.load_workbook(file_path)
worksheet = workbook.active  # Menggunakan sheet pertama

# Mengambil data dari kolom DOSS1 dan DOSS2
rss_doss1 = []
rss_doss2 = []

for row in worksheet.iter_rows(min_row=2, max_row=worksheet.max_row, max_col=2, values_only=True):
    rss_doss1.append(int(row[0]) if row[0] is not None else 0)  # Kolom DOSS1
    rss_doss2.append(int(row[1]) if row[1] is not None else 0)  # Kolom DOSS2

bb = 50  # Jumlah loop
total_data = len(rss_doss1)
aa = total_data // bb  # Jumlah blok data yang valid

# Potong data agar sesuai dengan reshape
rss_doss1 = np.clip(rss_doss1[:aa * bb], -100, 100)  # Clipping untuk outlier
rss_doss2 = np.clip(rss_doss2[:aa * bb], -100, 100)

# Melakukan reshape data untuk DOSS1 dan DOSS2
doss1 = np.array(rss_doss1).reshape(aa, bb).T
doss2 = np.array(rss_doss2).reshape(aa, bb).T

a = 1  # a posteri error estimate
h = 1
R_initial = 1  # Measurement Error Covariance Matrix
Q_initial = 0.05  # Process Noise Covariance, lebih besar agar adaptif

xaposteriori_0 = -5  # Initial guesses
paposteriori_0 = 1

# Kalman Filter dengan Dynamic Tuning Q dan R
def kalman_filter_adaptive(rssival):
    xapriori = []
    residual = []
    papriori = []
    k = []
    paposteriori = []
    xaposteriori = []

    # Parameter awal
    Q = Q_initial
    R = R_initial

    # Proses untuk baris pertama
    row1, row2, row3, row4, row5, row6 = [], [], [], [], [], []
    for m in range(0, aa):
        row1.append(a * xaposteriori_0)
        row2.append(rssival[0][m] - h * row1[m])
        row3.append(a * a * paposteriori_0 + Q)
        row4.append(row3[m] / (row3[m] + R))
        row5.append(row3[m] * (1 - row4[m]))
        row6.append(row1[m] + row4[m] * row2[m])
    xapriori.append(row1)
    residual.append(row2)
    papriori.append(row3)
    k.append(row4)
    paposteriori.append(row5)
    xaposteriori.append(row6)

    # Proses untuk baris-baris berikutnya
    for j in range(1, bb):
        row7, row8, row9, row10, row11, row12 = [], [], [], [], [], []
        for n in range(0, aa):
            row7.append(xaposteriori[j - 1][n])
            row8.append(rssival[j][n] - h * row7[n])
            row9.append(a * a * paposteriori[j - 1][n] + Q)
            row10.append(row9[n] / (row9[n] + R))
            row11.append(row9[n] * (1 - row10[n]))
            row12.append(row7[n] + row10[n] * row8[n])
        xapriori.append(row7)
        residual.append(row8)
        papriori.append(row9)
        k.append(row10)
        paposteriori.append(row11)
        xaposteriori.append(row12)

        # Update Q dan R adaptif berdasarkan residual
        avg_residual = np.mean(np.abs(row8))
        Q = 0.02 * avg_residual
        R = 0.01 * avg_residual  # Meningkatkan fleksibilitas
    return np.array(xaposteriori)

# Kalman Filter adaptif
kalman_doss1 = kalman_filter_adaptive(doss1).T.flatten()
kalman_doss2 = kalman_filter_adaptive(doss2).T.flatten()

# Menyimpan hasil ke file Excel format .xlsx menggunakan pandas
df_output = pd.DataFrame({
    'DOSS1': kalman_doss1,
    'DOSS2': kalman_doss2
})

output_file_path = 'Praproses_Kalman_DOSS1_DOSS2_Optimized.xlsx'
df_output.to_excel(output_file_path, index=False, engine='openpyxl')

end1 = time.time()
time_kalman = end1 - start1
print('Waktu komputasi kalman = {} seconds'.format(time_kalman))

# Evaluasi numerik
def calculate_mse(original, filtered):
    return np.mean((np.array(original) - np.array(filtered)) ** 2)

print(f"MSE DOSS1: {calculate_mse(rss_doss1, kalman_doss1)}")
print(f"MSE DOSS2: {calculate_mse(rss_doss2, kalman_doss2)}")

# Visualisasi hasil Kalman Filter
def plot_kalman_results(original, kalman_filtered, label):
    plt.figure(figsize=(10, 6))
    plt.plot(original, label=f'Original {label}', linestyle='--', alpha=0.7)
    plt.plot(kalman_filtered, label=f'Kalman Filtered {label}', linewidth=2)
    plt.title(f'Hasil Kalman Filter - {label}')
    plt.xlabel('Data Index')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)
    plt.show()

# Plot untuk DOSS1 dan DOSS2
plot_kalman_results(rss_doss1, kalman_doss1, 'DOSS1')
plot_kalman_results(rss_doss2, kalman_doss2, 'DOSS2')
