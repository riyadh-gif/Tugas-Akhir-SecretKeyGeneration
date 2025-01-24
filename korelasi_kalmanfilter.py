import pandas as pd
from scipy.stats import pearsonr

# Baca file Excel
file_path = 'E:\\PENS\\Semester 7\\Progress PA\\codingan\\Program\\Praproses_Kalman_DOSS1_DOSS2_Optimized.xlsx'
data = pd.read_excel(file_path)

# Asumsikan kolom untuk Alice dan Bob bernama 'Alice' dan 'Bob'
doss1_data = data['DOSS1']
doss2_data = data['DOSS2']

# Hitung korelasi menggunakan scipy
correlation, p_value = pearsonr(doss1_data, doss2_data)
print(f"Korelasi Pearson antara Alice dan Bob: {correlation}")
