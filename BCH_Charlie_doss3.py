import numpy
import numpy as np
import time
import math
import xlrd
from math import floor
from random import seed
from xlwt import Workbook
import csv

#=====================================================================================================================
#============================================BCH CODE=================================================================
print("\n================================= BCH CODE ===============================\n")
start4 = time.time()

# Inisialisasi global untuk menampung hasil BCH decoding
charliebch = []
alalice = []
bobob = []
errbch = []

# Inisialisasi global untuk deleteblok
deleteblok = 0  # Tambahkan inisialisasi global untuk deleteblok

# Membaca file Excel untuk Alice, Bob, dan Charlie
workbook = xlrd.open_workbook(r"E:\PENS\Semester 8\Final TA\Code\Ruang Eksperimen\experimen 1\Program_1\files\Threshold_Alice.xls", on_demand=True)
worksheet = workbook.sheet_by_name("Sheet1")
workbook1 = xlrd.open_workbook(r"E:\PENS\Semester 8\Final TA\Code\Ruang Eksperimen\experimen 1\Program_1\files\Threshold_Bob.xls", on_demand=True)
worksheet1 = workbook1.sheet_by_name("Sheet1")
workbook2 = xlrd.open_workbook(r"E:\PENS\Semester 8\Final TA\Code\Ruang Eksperimen\experimen 1\Program_1\files\Threshold_Charlie.xls", on_demand=True)  # Tambahkan Charlie
worksheet2 = workbook2.sheet_by_name("Sheet1")

# Mengambil data dari Alice, Bob, dan Charlie
a = [worksheet.cell_value(row, 0) for row in range(1, worksheet.nrows)]
b = [worksheet1.cell_value(row, 0) for row in range(1, worksheet1.nrows)]
c = [worksheet2.cell_value(row, 0) for row in range(1, worksheet2.nrows)]  # Data Charlie

# KDR Sebelum BCH Error Correction untuk Charlie
errkuan_ca = [i+1 for i in range(len(c)) if c[i] != a[i]]
kdrkuan_ca = len(errkuan_ca) / len(c)
print("KDR Kuantisasi CHARLIE - ALICE Sebelum BCH = %.2f%%" % (kdrkuan_ca * 100))

# Perhitungan KDR Charlie - Bob Sebelum BCH
errkuan_cb = [i+1 for i in range(len(c)) if c[i] != b[i]]
kdrkuan_cb = len(errkuan_cb) / len(c)
print("KDR Kuantisasi CHARLIE - BOB Sebelum BCH = %.2f%%" % (kdrkuan_cb * 100))

# Inisialisasi parameter BCH
m = 5
n = 2**m - 1  # codeword length (n = 2^m - 1 = 31)
k = 6  # information bits
t = 7  # correcting capability
maks = math.floor(len(a) / k)

# Menyiapkan data untuk BCH encoding
alice = [a[k*i:k*(i+1)] for i in range(int(maks))]
bob = [b[k*i:k*(i+1)] for i in range(int(maks))]
charlie = [c[k*i:k*(i+1)] for i in range(int(maks))]

# ------------------- GF-ARITHMETIC --------------------
# ------------------------------------------------------
def gf_add(a, b):
    prod = ""
    if len(a) > len(b):
        b = '0'*(len(a) - len(b)) + b
    elif len(a) < len(b):
        a = '0'*(len(b) - len(a)) + a
    for i in range(len(a)):
        prod += '1' if a[i] != b[i] else '0'
    return prod

def gf_mul(a, b):
    prod = '0' * (len(a) + len(b) - 1)
    for i in range(len(a)):
        for j in range(len(b)):
            tmp = '1' if a[i] == '1' and b[j] == '1' else '0'
            if prod[i + j] == tmp:
                prod = prod[:i + j] + '0' + prod[i + j + 1:]
            else:
                prod = prod[:i + j] + '1' + prod[i + j + 1:]
    return prod

def gf_xor(a, b):
    return ''.join(['1' if x != y else '0' for x, y in zip(a[1:], b[1:])])

def gf_div(a, b, mode=0):
    pick = len(b)
    q = ""  # quotient
    r = a[:pick]  # remainder
    while pick < len(a):
        if r[0] == '1':
            q += '1'
            r = gf_xor(b, r) + a[pick]
        else:
            q += '0'
            r = gf_xor('0' * pick, r) + a[pick]
        pick += 1
    if r[0] == '1':
        q += '1'
        r = gf_xor(b, r)
    else:
        q += '0'
        r = gf_xor('0' * pick, r)
    return r if not mode else q

# ------------------- CODER/DECODER --------------------
# ------------------------------------------------------
def bch_encode(data, g):
    return gf_mul(data, g)

def bch_decode(c, g):
    syndrome = gf_div(c, g)
    if not weight(syndrome):
        return c
    cnt_rot = 0
    recd = c
    stp = 0
    while weight(syndrome) > t:
        recd = l_rotate(recd)
        syndrome = gf_div(recd, g)
        cnt_rot += 1
        stp += 1
        if stp > n:
            break
    recd = gf_add(recd, syndrome)
    recd = r_rotate(recd, cnt_rot)
    return recd

def l_rotate(poly, s=1):
    return poly[s:] + poly[:s]

def r_rotate(poly, s=1):
    return poly[-s:] + poly[:-s]

def weight(poly):
    return sum([int(coeff) for coeff in poly])

# ------------------------ MAIN ------------------------
# ------------------------------------------------------
global totalerrorbch
totalerrorbch = []
global parityalice
parityalice = []

def main(data, data2, data3, z):
    global deleteblok
    seed()

    g = "11001011011110101000100111"  # BCH (31,6) m=5 k=6 t=7
    c1 = bch_encode(data, g)  # codeword c(x) (Charlie)
    c2 = bch_encode(data2, g)  # codeword c(x) (Alice)
    c3 = bch_encode(data3, g)  # codeword c(x) (Bob)

    errcode = 0
    poserrcode = []
    # Menghitung error kode antara Charlie, Alice, dan Bob
    for i in range(n - k):
        if c1[i + k] != c2[i + k] or c1[i + k] != c3[i + k]:
            errcode += 1
            poserrcode.append(i + k)
    
    # Jika jumlah error kurang dari atau sama dengan kemampuan koreksi BCH
    if errcode <= t:
        for i in range(errcode):
            c2 = c2[:poserrcode[i]] + ('0' if c2[poserrcode[i]] == '1' else '1') + c2[poserrcode[i] + 1:]
            c3 = c3[:poserrcode[i]] + ('0' if c3[poserrcode[i]] == '1' else '1') + c3[poserrcode[i] + 1:]

        # Dekoding BCH
        recd1 = bch_decode(c1, g)
        recd2 = bch_decode(c2, g)
        recd3 = bch_decode(c3, g)

        charliebch.append(recd1)  # Hasil dekoding Charlie
        alalice.append(recd2)  # Hasil dekoding Alice
        bobob.append(recd3)    # Hasil dekoding Bob
    else:
        deleteblok += 1  # Meningkatkan jumlah blok yang dihapus

# ----------------------- START ------------------------
# ------------------------------------------------------
for i in range(int(maks)):
    dt1 = ''.join(str(e) for e in charlie[i])
    dt2 = ''.join(str(e) for e in alice[i])
    dt3 = ''.join(str(e) for e in bob[i])
    main(dt1, dt2, dt3, i + 1)

# Collecting results
charlie11 = ''.join(charliebch)
alice11 = ''.join(alalice)
bob11 = ''.join(bobob)

bitcharlie = list(map(int, charlie11))
bitalice = list(map(int, alice11))
bitbob = list(map(int, bob11))

# Calculate errors by comparing the decoded bits
errbch_ca = [i+1 for i in range(len(bitcharlie)) if bitcharlie[i] != bitalice[i]]  # KDR Charlie - Alice
errbch_cb = [i+1 for i in range(len(bitcharlie)) if bitcharlie[i] != bitbob[i]]  # KDR Charlie - Bob

# Calculate KDR for Charlie-Alice, Charlie-Bob
kdrca = len(errbch_ca) / len(bitcharlie)
kdrcb = len(errbch_cb) / len(bitcharlie)

# Display the KDR for both comparisons
print(f"KDR Kuantisasi CHARLIE - ALICE Setelah BCH = {kdrca * 100:.2f}%")
print(f"KDR Kuantisasi CHARLIE - BOB Setelah BCH = {kdrcb * 100:.2f}%")

# Results
print(f'Jumlah blok error: {deleteblok}, Jumlah blok dikoreksi: {maks - deleteblok}, KDR Charlie-Alice = {kdrca:.2f}, KDR Charlie-Bob = {kdrcb:.2f}')


# Membuat workbook dan sheet baru
book = Workbook()
sheet1 = book.add_sheet("BCH Charlie")

# Menulis header
sheet1.write(0, 0, "Charlie")

# Menulis hasil BCH Charlie
for i, bit in enumerate(bitcharlie):
    sheet1.write(i + 1, 0, bit)

# Menyimpan file XLS
book.save(r'E:\PENS\Semester 8\Final TA\Code\Ruang Eksperimen\experimen 1\Program_1\files\Hasil_BCH_Charlie.xls')

print("Data Charlie sukses disimpan dengan nama Hasil_BCH_Charlie.xls")
