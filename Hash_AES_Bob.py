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
print("\n================================= UNIV HASH ===============================\n")
start5 = time.time()

# Open workbooks and worksheets
workbook = xlrd.open_workbook("Hasil_BCH_ALICE_I10_7030_DeepLearning_New97.xls", on_demand=True)
worksheet = workbook.sheet_by_name("HasilBCHalice")
workbook1 = xlrd.open_workbook("Hasil_BCH_BOB_I10_7030_DeepLearning_New97.xls", on_demand=True)
worksheet1 = workbook1.sheet_by_name("HasilBCHbob")

# Extract data from the first worksheet
first_row = []  # Header
for col in range(0, worksheet.ncols):
    first_row.append(worksheet.cell_value(0, col))

# Mengambil nilai dari excel ke rss_alice
aliice = []
for row in range(1, worksheet.nrows):
    elm = worksheet.cell_value(row, 0)
    aliice.append(elm)

# Mengambil nilai dari excel ke rss_bob
bbob = []
for row in range(1, worksheet1.nrows):
    if row < worksheet1.nrows:
        for col in range(2):
            if col < worksheet1.ncols:
                elm = worksheet1.cell_value(row, col)
                bbob.append(elm)

print("Panjang input univhash %d" % len(aliice))

# Process the data
key = []
jumlahkeya = math.floor(len(aliice) / 128)
jumlahkey = jumlahkeya
ukuranhash = 128
aaaa = len(bbob) % 128
lenalice = len(bbob) - aaaa

for i in range(0, aaaa):
    del bbob[lenalice]

Hashtab = []
with open('Hashtable128.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        Hashtab.append(row)
Hashtable = np.array(Hashtab)

key2 = []
for i in range(jumlahkey):
    mat2 = []
    bbb = bbob[(i * ukuranhash): (ukuranhash * (i + 1))]
    print("Key-%d: Panjang data adalah %d dan ukuran HashTable yaitu %d x %d" % (i + 1, len(bbb), ukuranhash, len(bbb)))
    
    for x in range(0, len(Hashtable)):
        row = []
        total = 0
        for y in range(0, len(bbb)):
            total = total + (int(Hashtable[x][y]) * bbb[y])
            row = total % 2
        mat2.append(int(row))
    key2.append(mat2)
    print("Jumlah key bob sekarang: ", len(key2))

v = 0
bx = [0] * 128 * jumlahkey
for i in range(jumlahkey):
    for j in range(128):
        bx[v] = key2[i][j]
        v = v + 1
        
univ = []
for i in range(0, len(bx)):
    univ.append(bx[i])

univ1 = np.array(univ)
univ2 = univ1.reshape(len(bx), 1)

end4 = time.time()
print("Universal Hash Berhasil")

# Save data to csv
with open("univhash_Bob_I10_7030_New97.csv", "w", newline="") as fp:
    a = csv.writer(fp, delimiter=",")
    a.writerows(univ2)

# Save data to Excel
book = Workbook()
sheet1 = book.add_sheet("UnivHASH")
sheet1.write(0, 0, "Alice")
for i in range(1, len(bx) + 1):
    sheet1.write(i, 0, int(bx[i - 1]))
book.save("Universal_Hash_Bob_I10_7030_DeepLearning_New97.xls")

end5 = time.time()
print('UNIVHASH Panjang bit hasil Universal Hash alice = %d, bob= %d' % (len(bx), len(bx)))
print('UNIVHASH Jumlah hasil key yang dibangkitkan = %d' % jumlahkey)
print('Waktu Proses HASHING : ', end5 - start5)

# =========================================================================
# ============================== CEK NIST =================================
print('\n\n====================== CEK NIST ========================')
print('============================================================\n')

startnist = time.time()
command = "./NIST-TestBOB128"
#subprocess.Popen(command, shell=True)

indeks = []
indek = []

time.sleep(1)

with open("sudahujinist_Bob_I10_7030_New97.csv", newline="") as f:
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

startsha=time.time()
databob = []
hex1 = []
abc1 = []
for j in range(len(indek)):
    hash1 = [0] * 128
    for i in range(128):
        # print(key2[0][indek[j]][i])
        hash1[i] = key2[0][indek[j]]

    data1 = "".join(str(e) for e in hash1)
    someText1 = data1.encode("ascii")
    b1 = hashlib.sha1(someText1).hexdigest()
    hex1.append(b1)

    print('Hasil hash Bob Kunci-{} = {}'.format(indek[j]+1, hex1[j]))

book = Workbook()
sheet1 = book.add_sheet('sha128')
sheet1.write(0, 0, 'Bob')
for i in range(1, len(hex1)+1):
    sheet1.write(i, 0, hex1[i-1])
book.save('SHA128BOB_I10_7030_97.xls')
book.save(TemporaryFile())

# Di nyalain saat di rasbery
# socketsend('SHA128ALICE.xls') 
# socketrecv()

workbook = xlrd.open_workbook('SHA128BOB_I10_7030_97.xls', on_demand=True)
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
endsha=time.time()
print('Waktu Proses HASHING : ', endsha - startsha)
# =========================================================================
# ================================= AES-128 ===============================
print('\n\n===========~~~~~~~~~~~== AES ~~~~~~~~~~~~~~==============')
print('===========~~~~~~~~~~~=========~~~~~~~~~~~~~~==============\n')
start_aes=time.time()
for kuncinya in range(len(indek)):
    if(hex1[kuncinya]==hex2[kuncinya]):
        keybit = ''.join(str(e)for e in key2[indek[kuncinya]])
        keyint=int(keybit,2)
        keybyte=binascii.unhexlify('%x' % keyint)
        print('Key Bob 1 (16 bytes) = ',keybyte)
    break
for kunci in range(len(indek)):
    if(hex1[kunci]==hex2[kunci]):
        keybitt = ''.join(str(e)for e in key2[indek[kunci]])
        keyintt=int(keybitt,4)
        keybytee=binascii.unhexlify('%x' % keyintt)
        print('Key Bob 2 (32 bytes) = ',keybytee)
        print ('\n=================CTR=============')
        # A 128 bit (32 byte) key
        plaintext = "TES PESAN"
        plaintextt = "PESAN KEDUA"
        plaintexttt = "PESAN KETIGA"
        plaintextttt = "PESAN KEEMPAT"
        plaintexttttt = "PESAN KELIMA"
        print ('Plaintext 1 = ',plaintext)
        print ('Plaintext 2 = ',plaintextt)
        print ('Plaintext 3 = ',plaintexttt)
        print ('Plaintext 4 = ',plaintextttt)
        print ('Plaintext 5 = ',plaintexttttt)
        aesctr = pyaes.AESModeOfOperationCTR(keybyte)
        aesctrr = pyaes.AESModeOfOperationCTR(keybytee)
        #==========Kunci 1==========
        ciphertext = aesctr.encrypt(plaintext)
        ciphertextt = aesctr.encrypt(plaintextt)
        ciphertexttt = aesctr.encrypt(plaintexttt)
        ciphertextttt = aesctr.encrypt(plaintextttt)
        ciphertexttttt = aesctr.encrypt(plaintexttttt)
        #========== Kunci 2 ==========
        cipherttext = aesctrr.encrypt(plaintext)
        cipherteextt = aesctrr.encrypt(plaintextt)
        cipherteeexttt = aesctrr.encrypt(plaintexttt)
        cipherteeeextttt = aesctrr.encrypt(plaintextttt)
        cipherteeeeexttttt = aesctrr.encrypt(plaintexttttt)
        #sendtext(ciphertext)
        time.sleep(3)
        print ('==========Kunci 1==========')
        print ('Ciphertext 1 key 1 = ',ciphertext)
        print ('Ciphertext 2 key 1 = ',ciphertextt)
        print ('Ciphertext 3 key 1 = ',ciphertexttt)
        print ('Ciphertext 4 key 1 = ',ciphertextttt)
        print ('Ciphertext 5 key 1 = ',ciphertexttttt)
        print ('==========Kunci 2==========')
        print ('Ciphertext 1 key 2 = ',cipherttext)
        print ('Ciphertext 2 key 2 = ',cipherteextt)
        print ('Ciphertext 3 key 2 = ',cipherteeexttt)
        print ('Ciphertext 4 key 2 = ',cipherteeeextttt)
        print ('Ciphertext 5 key 2 = ',cipherteeeeexttttt)
        print ('==========Proses selesai=============')
        break
    elif(hex1[kuncinya]!=hex2[kuncinya] and (kuncinya+1)<(len(indek)+1)):
        print('Hash untuk kunci ke-%d tidak valid, maka pakai kunci selanjutnya (Kunci ke-%d)'%(indek[kuncinya]+1,indek[kuncinya]+1))
    else:
        print('Hash untuk kunci ke-%d tidak valid, ulangi proses dari awal (Pengukuran)'%(indek[kuncinya]+1))
        break
end_aes=time.time()
time_aes=end_aes-start_aes
print('Waktu Proses Enkripsi : ', time_aes)
end=time.time()
#print('Waktu Proses Keseluruhan Sistem : ', end - start1)