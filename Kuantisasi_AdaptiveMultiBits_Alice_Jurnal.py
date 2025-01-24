import socket
import time
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
import math
import csv
import math
from math import log
from math import floor
from math import pow
from random import seed, randint
from tempfile import TemporaryFile
import xlrd
import openpyxl
import xlwt
from xlwt import Workbook
from numpy import zeros
import pyaes
import subprocess
import hashlib
from sys    import exit
from tempfile import TemporaryFile
import binascii

from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
from numpy import array, exp 

mulai=time.time()
start_adaptivemultibits=time.time()
# =========================================================================
# ============================== Quantization =============================

print('\n\n====================== Kuantisasi AMBQ ========================')
print('============================================================\n')

df = pd.read_csv('alice_praproses_kalman_O500.csv')
start2 = time.time()
def gray_code(n):
    def gray_code_recurse (g,n):
        k=len(g)
        if n<=0:
            return
        else:
            for i in range (k-1,-1,-1):
                char='1'+g[i]
                g.append(char)
            for i in range (k-1,-1,-1):
                g[i]='0'+g[i]
            gray_code_recurse (g,n-1)
    g=['0','1']
    gray_code_recurse(g,n-1)
    return g

map_graycode = []
n=int(4)
g = gray_code (n)

if n>=1:
  for i in range (len(g)):
    map_graycode.append(g[i],)


rangex = df['Alice_praproses'].max() - df['Alice_praproses'].min()
print("Range: %d" % (rangex))

if(rangex >=0 and rangex < 16):
  Num = abs(math.sqrt(rangex))
else:
  Num = 3 #NUM UBAH (3, 5)
print("Num: %d" % (Num))

interval = rangex/(2**Num)
print("Interval : %d" % (interval))

W = ""
for i in range(1,int(len(df['Alice_praproses']))):
  for j in range(0,int((2**Num)-1)):
    L = min(df['Alice_praproses']) + (j/interval) #UBAH DIBAGI
    U = max(df['Alice_praproses']) + ((j+1)/interval) #UBAH DIBAGI
    if L < df['Alice_praproses'][i] and U > df['Alice_praproses'][i]:
      W = W + map_graycode[j]
    

#print('panjang W : ', len(W))

# Membuat file XLS
workbook = xlwt.Workbook()
sheet = workbook.add_sheet('Sheet1')  # Buat lembar baru

# Menulis data ke file XLS
sheet.write(0, 0, 'Alice_Kuantisasi')  # Menulis judul 'Alice'

row = 1
for angka in W:
    sheet.write(row, 0, angka)
    row += 1

# Menyimpan file XLS
workbook.save('Alice_Kuantisasi_Kalman_AdaptiveMultiBits_O500_Penyadap_N_3.xls')

end_adaptivemultibits=time.time()
time_adaptivemultibits=end_adaptivemultibits-start_adaptivemultibits
#kgrkuan=len(output_filename)*(end_adaptivemultibits-start_adaptivemultibits)
#print('KGR = %f'%kgrkuan)
print('Waktu komputasi kuantisasi = {} seconds'.format(end_adaptivemultibits-start_adaptivemultibits))
print('-------------------')
print('Kuantisasi Berhasil')
print('-------------------')