import numpy as np
import time
import csv
import math
import xlrd
from xlwt import Workbook
import os

# =========================================================================
# ============================== UNIVERSAL HASH ===========================
print("\n================================= UNIVERSAL HASH ===============================\n")

# Start timing the hashing process
start5 = time.time()

# Open workbooks and check sheet names
try:
    # Open Alice's workbook and verify sheet existence
    workbook_path = r"E:\PENS\Semester 8\Final TA\Code\Ruang Eksperimen\experimen 1\Program_1\files\Hasil_BCH_Alice.xls"
    if not os.path.exists(workbook_path):
        raise FileNotFoundError(f"Workbook not found: {workbook_path}")
    
    workbook = xlrd.open_workbook(workbook_path, on_demand=True)
    print(f"Available sheets in Hasil_BCH_DOSS1.xls: {workbook.sheet_names()}")  # Debugging line
    worksheet = workbook.sheet_by_name("BCH Alice")

    # Open charlie's workbook and verify sheet existence
    workbook1_path = r"E:\PENS\Semester 8\Final TA\Code\Ruang Eksperimen\experimen 1\Program_1\files\Hasil_BCH_charlie.xls"
    if not os.path.exists(workbook1_path):
        raise FileNotFoundError(f"Workbook not found: {workbook1_path}")

    workbook1 = xlrd.open_workbook(workbook1_path, on_demand=True)  # This line was missing
    print(f"Available sheets in Hasil_BCH_charlie_doss3.xls: {workbook1.sheet_names()}")  # Debugging line
    worksheet1 = workbook1.sheet_by_name("BCH Charlie")  # Accessing the correct sheet from workbook1
    
except (ValueError, xlrd.XLRDError, FileNotFoundError) as e:
    print(f"Error: {e}")
    exit()

# Get header row from charlie's sheet (just to verify the structure)
first_row_charlie = [worksheet1.cell_value(0, col) for col in range(worksheet1.ncols)]

# Extract charlie's data (only the first column)
charlie = [worksheet1.cell_value(row, 0) for row in range(1, worksheet1.nrows)]

print(f"Panjang Input UnivHASH charlie: {len(charlie)}")

# Adjust the length of charlie's data to be a multiple of 128
jumlahkeyb = math.floor(len(charlie) / 128)
jumlahkey = jumlahkeyb

ukuranhash = 128
# Remove any excess data that doesn't fit into a full 128-bit block
lencharlie = len(charlie) - (len(charlie) % 128)
charlie = charlie[:lencharlie]

# Load the Hash Table from CSV
Hashtab = []
with open('Hashtable128.csv', newline='') as f:
    reader = csv.reader(f)
    Hashtab = list(reader)

Hashtable = np.array(Hashtab, dtype=int)

# Generate keys for each block of data for charlie
key1_charlie = []
for i in range(jumlahkey):
    mat1 = []
    aaa = charlie[i * ukuranhash: (i + 1) * ukuranhash]
    
    print(f"Key-{i+1}: Panjang data adalah {len(aaa)} dan ukuran HashTable yaitu {ukuranhash} x {len(aaa)}")
    
    # Compute the hash for each row in the hash table
    for x in range(len(Hashtable)):
        total = sum(int(Hashtable[x][y]) * aaa[y] for y in range(len(aaa)))
        row = total % 2  # Apply mod 2 to each sum
        mat1.append(int(row))
    
    key1_charlie.append(mat1)
    print(f"Jumlah KEY charlie Sekarang: {len(key1_charlie)}")

# Flatten all keys into a single list for charlie
bx = [key1_charlie[i][j] for i in range(jumlahkey) for j in range(ukuranhash)]

# Prepare data for writing to CSV and Excel
univ2_charlie = np.array(bx).reshape(len(bx), 1)

# Save output to CSV for charlie
with open(r"E:\PENS\Semester 8\Final TA\Code\Ruang Eksperimen\experimen 1\Program_1\files\univhash_charlie_doss3.csv", "w", newline="") as fp:
    csv.writer(fp, delimiter=",").writerows(univ2_charlie)

# Save output to Excel for charlie
book_charlie = Workbook()
sheet1_charlie = book_charlie.add_sheet("UnivHASH")
sheet1_charlie.write(0, 0, "charlie")
for i in range(1, len(bx) + 1):
    sheet1_charlie.write(i, 0, int(bx[i - 1]))
book_charlie.save(r"E:\PENS\Semester 8\Final TA\Code\Ruang Eksperimen\experimen 1\Program_1\files\univhash_charlie_doss3.xls")

# End timing
end5 = time.time()

# Print the results for charlie
print(f"UNIVHASH Panjang bit hasil Universal Hash charlie = {len(bx)}")
print(f"UNIVHASH Jumlah hasil key yang dibangkitkan = {jumlahkey}")
print(f"Waktu Proses HASHING: {end5 - start5:.4f} seconds")
