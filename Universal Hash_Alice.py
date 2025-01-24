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

# =========================================================================
# ============================== UNIVERSAL HASH ===========================
print("\n================================= UNIVERSAL HASH ===============================\n")

start5=time.time()
workbook = xlrd.open_workbook("Hasil_BCH_ALICE_I10_7030_DeepLearning_New97.xls", on_demand=True)
worksheet = workbook.sheet_by_name("HasilBCHalice")
workbook1 = xlrd.open_workbook("Hasil_BCH_BOB_I10_7030_DeepLearning_New97.xls", on_demand=True)
worksheet1 = workbook1.sheet_by_name("HasilBCHbob")
first_row = []  # Header
for col in range(0, worksheet.ncols):
    first_row.append(worksheet.cell_value(0, col))
    # transform the workbook to a list of dictionnaries

# Mengambil nilai dari excel ke rss_alice
aliice = []
for row in range(1, worksheet.nrows):
    elm = {}
    for col in range(1):
        elm = worksheet.cell_value(row, col)
    aliice.append(elm)

print("Panjang Input UnivHASH ALICE %d" % len(aliice))

key = []
jumlahkeya = math.floor(len(aliice) / 128)
jumlahkey = jumlahkeya

ukuranhash = 128
aaaa = len(aliice) % 128
lenalice = len(aliice) - aaaa

for i in range(0, aaaa):
    del aliice[lenalice]

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
    aaa = aliice[(i * ukuranhash): (ukuranhash * (i + 1))]
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
    print("Jumlah KEY ALICE Sekarang : ", len(key1))

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
with open("univhash_Alice_I10_7030_New97.csv", "w", newline="") as fp:
    a = csv.writer(fp, delimiter=",")
    a.writerows(univ2)
book = Workbook()
sheet1 = book.add_sheet("UnivHASH")
sheet1.write(0, 0, "Alice")
for i in range(1, len(ax) + 1):
    sheet1.write(i, 0, int(ax[i - 1]))
book.save("Universal_Hash_Alice_I10_7030_DeepLearning_New97.xls")
end5 = time.time()
#kgruniv=len(aliice)*((endhash - starthash) + (end_jana-start_jana) + (end3 - start3))
#print('UNIVHASH KGR = %f'%(kgruniv))
print('UNIVHASH Panjang bit hasil Universal Hash alice = %d, bob= %d'%(len(ax),len(ax)))
print('UNIVHASH Jumlah hasil key yang dibangkitkan = %d'%jumlahkey)
print('Waktu Proses HASHING : ', end5 - start5)