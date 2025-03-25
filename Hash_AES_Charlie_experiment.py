import numpy
import numpy as np
import time
import csv
import matplotlib.pyplot as plt
import pandas as pd
from pandas import read_excel
import math
import subprocess
import xlrd
from math import floor
from math import pow
from math import log
from random import seed, randint
from tempfile import TemporaryFile
from sys    import exit
from xlwt import Workbook
#from keras.models import Sequential
#from keras.layers import Dense
#from keras.layers import LSTM
#from sklearn.preprocessing import MinMaxScaler
#from sklearn.preprocessing import RobustScaler
#from sklearn.metrics import mean_squared_error
import sys
import hashlib
import socket
import pyaes
import binascii
from PIL import Image
import numpy as np
import pyaes
import binascii
import time
# =========================================================================
# ============================== UNIVERSAL HASH ===========================
print("\n================================= UNIVERSAL HASH ===============================\n")

start5=time.time()
workbook = xlrd.open_workbook(r"files\Hasil_BCH_Charlie.xls", on_demand=True)
worksheet = workbook.sheet_by_name("BCH Charlie")

first_row = []  # Header
for col in range(0, worksheet.ncols):
    first_row.append(worksheet.cell_value(0, col))
    # transform the workbook to a list of dictionnaries

# Mengambil nilai dari excel ke rss_charlie
ccharlie = []
for row in range(1, worksheet.nrows):
    elm = {}
    for col in range(1):
        elm = worksheet.cell_value(row, col)
    ccharlie.append(elm)

print("Panjang Input UnivHASH charlie %d" % len(ccharlie))

key = []
jumlahkeya = math.floor(len(ccharlie) / 128)
jumlahkey = jumlahkeya

ukuranhash = 128
aaaa = len(ccharlie) % 128
lencharlie = len(ccharlie) - aaaa

for i in range(0, aaaa):
    del ccharlie[lencharlie]

Hashtab = []
with open('Hashtable128.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        Hashtab.append(row)
Hashtable = []
Hashtable = np.array(Hashtab)

key1 = []
for i in range(jumlahkey):
    mat1 = []
    aaa = []
    aaa = ccharlie[(i * ukuranhash): (ukuranhash * (i + 1))]
    print(
        "Key-%d: Panjang data adalah %d dan ukuran HashTable yaitu %d x %d"
        % (i + 1, len(aaa), ukuranhash, len(aaa))
    )
    # print('Input skr',aaa)
    for x in range(0, len(Hashtable)):
        row = []
        total = 0
        for y in range(0, len(aaa)):
            total = total + (int(Hashtable[x][y]) * aaa[y])
            row = total % 2
        mat1.append(int(row))
    key1.append(mat1)
    print("Jumlah KEY charlie Sekarang : ", len(key1))

v = 0
ax = [0] * 128 * jumlahkey
for i in range(jumlahkey):
    for j in range(128):
        ax[v] = key1[i][j]
        v = v + 1
univ = []
for i in range(0, len(ax)):
    univ.append(ax[i])

univ1 = np.array(univ)
univ2 = univ1.reshape(len(ax), 1)
# Memasukkan data ke excel
with open(r"files\univhash_charlie_doss3.csv", "w", newline="") as fp:
    a = csv.writer(fp, delimiter=",")
    a.writerows(univ2)
book = Workbook()
sheet1 = book.add_sheet("UnivHASH")
sheet1.write(0, 0, "charlie")
for i in range(1, len(ax) + 1):
    sheet1.write(i, 0, int(ax[i - 1]))
book.save("Universal_Hash_charlie_I10_7030_DeepLearning_New97.xls")
end5 = time.time()
#kgruniv=len(ccharlie)*((endhash - starthash) + (end_jana-start_jana) + (end3 - start3))
#print('UNIVHASH KGR = %f'%(kgruniv))
print('UNIVHASH Panjang bit hasil Universal Hash charlie = %d, charlie= %d'%(len(ax),len(ax)))
print('UNIVHASH Jumlah hasil key yang dibangkitkan = %d'%jumlahkey)
print('Waktu Proses HASHING : ', end5 - start5)

# =========================================================================
# ============================== CEK NIST =================================
print('\n\n====================== CEK NIST ========================')
print('============================================================\n')

startnist = time.time()
command = "./NIST-TestCharlie128"
#subprocess.Popen(command, shell=True)

indeks = []
indek = []

time.sleep(1)

with open(r"files\sudujinist_charlie.csv", newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        indeks.append(row)
prindek = []
for i in range(0, len(indeks)):
    indek.append(int(indeks[i][0]))
    prindek.append(int(indeks[i][0]) + 1)
endnist = time.time()
print('===========~~~~~~~~~~~=========~~~~~~~~~~~~~~==============\n')
print('NIST Hasil prioritas index',prindek)
print('Waktu Proses Uji NIST : ', endnist - startnist)

# =========================================================================
# ================================= SHA-128 ===============================
print('\n\n====================== SHA-128 ========================')
print('============================================================\n')

start6=time.time()
datacharlie = []
hex1 = []
abc1 = []
for j in range(len(indek)):
    hash1 = [0] * 128
    for i in range(128):
        # print(key1[0][indek[j]][i])
        hash1[i] = key1[0][indek[j]]

    data1 = "".join(str(e) for e in hash1)
    someText1 = data1.encode("ascii")
    b1 = hashlib.sha1(someText1).hexdigest()
    hex1.append(b1)

    print('Hasil hash charlie Kunci-{} = {}'.format(indek[j]+1, hex1[j]))

book = Workbook()
sheet1 = book.add_sheet('sha128')
sheet1.write(0, 0, 'charlie')
for i in range(1, len(hex1)+1):
    sheet1.write(i, 0, hex1[i-1])
book.save('SHA128charlie_I10_7030_97.xls')
book.save(TemporaryFile())

# Di nyalain saat di rasbery
# socketsend('SHA128charlie.xls') 
# socketrecv()

workbook = xlrd.open_workbook('SHA128charlie_I10_7030_97.xls', on_demand=True)
worksheet = workbook.sheet_by_index(0)
first_row = []  # Header
for col in range(0, worksheet.ncols):
    first_row.append(worksheet.cell_value(0, col))
    # tronsform the workbook to a list of dictionnaries
hex2 = []
for row in range(1, worksheet.nrows):
    elm = {}
    for col in range(1):
        elm = worksheet.cell_value(row, col)
    hex2.append(elm)

for j in range(len(indek)):
    if(hex1[j] == hex2[j]):
        print('Hash Value-%d valid, proses enkripsi dapat dilakukan' % (j+1))
    else:
        print('Hash Value-%d not valid' % (j+1))
end6=time.time()
print('Waktu Proses HASHING : ', end6 - start6)
# =========================================================================
# ================================= AES-128 ===============================
print('\n\n===========~~~~~~~~~~~== AES ~~~~~~~~~~~~~~==============')
print('===========~~~~~~~~~~~=========~~~~~~~~~~~~~~==============\n')
start7=time.time()
        
for kuncinya in range(len(indek)):
    if hex1[kuncinya] == hex2[kuncinya]:
        keybit = ''.join(str(e) for e in key1[indek[kuncinya]])
        keyint = int(keybit, 2)
        hex_str = '%x' % keyint
        if len(hex_str) % 2 != 0:
            hex_str = '0' + hex_str
        keybyte = binascii.unhexlify(hex_str)
        print('Key charlie 1 (16 bytes) = ', keybyte)
        break

#kalau mau convert ke hex
key_charlie_1 = keybyte
hex_key_charlie_1 = key_charlie_1.hex()
print(hex_key_charlie_1)

# Save the hexadecimal key into a .txt file
with open(r'key\key_charlie.txt', 'w') as txt_file:
    txt_file.write(hex_key_charlie_1)

print("Hex key saved to key_charlie.txt")
