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

#=====================================================================================================================
#============================================BCH CODE=================================================================
print("\n================================= BCH CODE ===============================\n")
start4=time.time()
workbook = xlrd.open_workbook("Alice_Kuantisasi_I10_7030_DeepLearning_New.xls", on_demand=True)
worksheet = workbook.sheet_by_name("Sheet1")
workbook1 = xlrd.open_workbook("Bob_Kuantisasi_I10_7030_DeepLearning_New.xls", on_demand=True)
worksheet1 = workbook1.sheet_by_name("Sheet1")

first_row=[]#Header
for col in range(0,worksheet.ncols):
  first_row.append(worksheet.cell_value(0,col))

a = []
for row in range (1,worksheet.nrows):
    elm = {}
    for col in range(1):
        elm = worksheet.cell_value(row,col)
    a.append(elm)
b = []
for row in range (1,worksheet1.nrows):
    elm = {}
    for col in range(1):
        elm = worksheet1.cell_value(row,col)
    b.append(elm)

alalice = []
bobob = []
deleteblok = 0
m = 5
n = 2**m-1  # codeword length (n = 2^m - 1 = 31)
k = 6  # information bits
t = 7  # correcting capability
#m = 7
# n = 2**m-1 # codeword length (n = 2^m - 1 = 31)
# k = 50 # information bits
# t = 13 # correcting capability
maks = math.floor(len(a)/k)
alice = []
bob = []
for i in range(0, int(maks)):
    alice.append(a[(k*i):(k*(i+1))])
    bob.append(b[(k*i):(k*(i+1))])
# ------------------- GF-ARITHMETIC --------------------
# ------------------------------------------------------
def gf_add(a, b):
    prod = ""
    if len(a) > len(b):
        b = '0'*(len(a) - len(b)) + b
    elif len(a) < len(b):
        a = '0'*(len(b) - len(a)) + a
    for i in range(len(a)):
        # XOR
        if a[i] == b[i]:
            prod += '0'
        else:
            prod += '1'
    return prod


def gf_mul(a, b):
    prod = '0'*(len(a) + len(b) - 1)
    for i in range(len(a)):
        for j in range(len(b)):
            # prod[i+j] ^= a[i] * b[j]
            # Multiplication
            if a[i] == '0' or b[j] == '0':
                tmp = '0'
            else:
                tmp = '1'
            # XOR
            if prod[i+j] == tmp:
                prod = prod[:i+j] + '0' + prod[i+j+1:]
            else:
                prod = prod[:i+j] + '1' + prod[i+j+1:]
    return prod


def gf_xor(a, b):
    prod = ""
    for i in range(1, len(b)):
        # XOR
        if a[i] == b[i]:
            prod += '0'
        else:
            prod += '1'
    return prod


def gf_div(a, b, mode=0):
    # mode 0: return remainder
    # mode 1: return quotient
    pick = len(b)
    q = ""       # quotient
    r = a[:pick]  # remainder
    while pick < len(a):
        if r[0] == '1':
            q += '1'
            r = gf_xor(b, r) + a[pick]
        else:
            q += '0'
            r = gf_xor('0'*pick, r) + a[pick]
        pick += 1
    if r[0] == '1':
        q += '1'
        r = gf_xor(b, r)
    else:
        q += '0'
        r = gf_xor('0'*pick, r)
    if not mode:
        return r
    return q
# ------------------- CODER/DECODER --------------------
# ------------------------------------------------------
# Encoding method: c(x) = data(x) * g(x)


def bch_encode(data, g):
    return gf_mul(data, g)
# Decoding method: polynomial division (while-loop, shifting until w <= t)


def bch_decode(c, g):
    syndrome = gf_div(c, g)
    if not weight(syndrome):
        return c
    cnt_rot = 0
    recd = c
    stp = 0
    while weight(syndrome) > t:
        ##        print('ada sindrom %d , loop ke %d'%(weight(syndrome),(stp+1)))
        recd = l_rotate(recd)
        syndrome = gf_div(recd, g)
        cnt_rot += 1
        stp += 1
        if stp > n:
            break
##    print('Done, sindrom %d'%(weight(syndrome)))
    recd = gf_add(recd, syndrome)
    recd = r_rotate(recd, cnt_rot)
    return recd
# --------------------- UTILITIES ----------------------
# ------------------------------------------------------


def l_rotate(poly, s=1):
    return poly[s:] + poly[:s]


def r_rotate(poly, s=1):
    return poly[-s:] + poly[:-s]


def weight(poly):
    return sum([int(coeff) for coeff in poly])


def polynomial(poly):
    for coeff in range(len(poly)):
        if (poly[coeff] != '0'):
            if (coeff != len(poly)-1):
                print("x^" + str(len(poly)-coeff-1) + " + ", end="")
            else:
                print("1", end="")
    print()


# ------------------------ MAIN ------------------------
# ------------------------------------------------------
global totalerrorbch
totalerrorbch = []
global parityalice
parityalice = []


def main(data, data2, z):
    global deleteblok
    seed()

    # g = "1101111100110100001110101101100111" # g(x) BCH(63,30) t=6 m=6 k=30
    g = "11001011011110101000100111"  # BCH (31,6) m=5 k=6 t=7
     #g = "10010110111" # generating polynomial g(x), of the (31,21) BCH code x^10 + x^9 + x^8 + x^6 + x^5 + x^3 + 1 t=2 m=5 k=21
    # g = "111010001" # g(x) BCH(15,7) t=2 m=4 k=7
    # g = "100010001100000101100010001010100000001100110110010101010100101011001001001101" #BCH(127,50) t=13 m=7 k=50
    # g = "110101101010110101011010110110011001111000111011011110" #bch(63,10) t=13 m=6 k=10
    c1 = bch_encode(data, g)  # codeword c(x)
    c2 = bch_encode(data2, g)

    errcode = 0
    poserrcode = []
    for i in range(n-k):
        if c1[i+k] != c2[i+k]:
            errcode = errcode+1
            poserrcode.append(i+k)
    totalerrorbch.append(errcode)
    parityalice.append(c1[k:])
    if errcode <= t:
        for i in range(errcode):
            if c2[poserrcode[i]] == '1':
                c2 = c2[:poserrcode[i]] + '0' + c2[poserrcode[i]+1:]
            else:
                c2 = c2[:poserrcode[i]] + '1' + c2[poserrcode[i]+1:]

        recd1 = bch_decode(c1, g)
        recd2 = bch_decode(c2, g)
        recd1 = gf_div(recd1, g, 1)
        recd2 = gf_div(recd2, g, 1)
        alalice.append(recd1)
        bobob.append(recd2)
    else:
        deleteblok += 1


# ----------------------- START ------------------------
# ------------------------------------------------------
for i in range(int(maks)):
    # print('\n##################### Blok ke %d #####################'%(i+1))
    dt1 = ''.join(str(e) for e in alice[i])
    dt2 = ''.join(str(e) for e in bob[i])
    main(dt1, dt2, i+1)
# for i in range(len(parityalice)):
##    print('[{}] {}'.format(i+1,parityalice[i]))
alice11 = ''.join(alalice)
bob11 = ''.join(bobob)
bitalice = list(map(int, alice11))
bitbob = list(map(int, bob11))

salah = 0
for i in range(len(bitbob)):
    if bitalice[i] != bitbob[i]:
        salah += 1

r1= len(b)
r2= len(bitbob)
errbchbefore = []
i = 0
while i < len(b):
    if (a[i] == b[i]):
        i = i+1
    else:
        errbchbefore.append(i+1)
        i = i+1
errbch=[]
for i in range(len(bitbob)):
    if (bitalice[i]==bitbob[i]):
        i=i+1
    else:
        errbch.append(i+1)

kdrbch=len(errbch)/len(bitbob)
print('BCH jumlah blok error = %d, \nJumlah blok dikoreksi = %d, \nKDR = %f' %(deleteblok,(maks-deleteblok),kdrbch))
print('Jumlah delete blok = %d dari %d blok, \nTotal bit = %d sebelumnya %d , \nTotal error = %d\n'%(deleteblok,maks,len(bitbob),maks*k,sum(totalerrorbch)))
print('Bit proses = %d'%(maks*k))
print('Blok = %d'%maks)
print('Total error = %d'%(sum(totalerrorbch)))
print('Blok koreksi = %d'%(maks-deleteblok))
print('Del blok = %d'%deleteblok)
print('JUMLAH BIT HASIL BCH CODE BOB %d'%len(bitbob))

# SAVING BCH
book=Workbook()
sheet1=book.add_sheet('HasilBCHbob')
#sheet1.write(0,0,'Alice')
sheet1.write(0,0,'Bob')
for i in range(1,len(bitalice)+1):
    #sheet1.write(i,0,float(bitalice[i-1]))
    sheet1.write(i,0,float(bitbob[i-1]))
book.save('Hasil_BCH_BOB_I10_7030_DeepLearning_New97.xls')
book.save(TemporaryFile())
end4=time.time()
waktu_kuan = 0.3623464107513428 
kgrbch=len(bitalice)*((waktu_kuan) + (end4 - start4))
print('KGR = %f'%kgrbch)
print('Waktu Proses BCH Code BOB : ', end4 - start4)
print("BCH CODE Berhasil")