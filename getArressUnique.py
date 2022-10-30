import numpy as np
import os
import collections
from collections import Counter

data = open('D:\Coin\checkWallet.txt', 'r').readlines()
dataList = []
for n in range(0, len(data)):
    if data[n] != "" and data[n]!="\n":
        item = data[n].split('|')[1]
        dataList.append(item.replace('\n', ''))
arrN = list(dict.fromkeys(dataList))

total = 0

if os.path.exists("D:\Coin\KetQua.txt"):
  os.remove("D:\Coin\KetQua.txt")
else:
  print("The file does not exist")

with open("D:\Coin\KetQua.txt", "a") as myfile:
    for i in range(len(arrN)):
        myfile.write(arrN[i])
        myfile.write("\n")
        total +=1

print("tong so:", total)


if os.path.exists("D:\Coin\keyTrung.txt"):
  os.remove("D:\Coin\keyTrung.txt")
else:
  print("The file does not exist")

totalDup = 0
dup = {i:dataList.count(i) for i in dataList}
with open("D:\Coin\keyTrung.txt", "a") as myfile:
  for k, v in dup.items():
    if(v>1):
      myfile.write(k)
      myfile.write('\n')
      totalDup +=v-1
print("totalDup", totalDup)
