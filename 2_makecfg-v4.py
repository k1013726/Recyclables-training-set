def emptydir(dirname):  #清空資料夾
    if os.path.isdir(dirname):  #資料夾存在就刪除
        shutil.rmtree(dirname)
        sleep(2)  #需延遲,否則會出錯
    os.mkdir(dirname)  #建立資料夾


import glob
import os, shutil
import wget
from time import sleep
import random


batch = 24 #設定每批次處理的資料數量。
subdivisions = 4  #設定每批次資料分幾次處理。
classname = ['Bottle','Beverage Pack','Cans','plastic','Paper container','paper']  #分類標籤
train = 'cfg/train.txt'  #建立訓練資料檔路徑
valid = 'cfg/valid.txt'  #建立驗證資料檔路徑
names = 'cfg/obj.names'  #分類標籤名稱檔
backup = 'cfg/weights'  #儲存訓練模型資料夾
validratio = 0.1  #設定驗證資料佔全部資料數量的比例


print('開始建立設定資料！')



#下載預訓練檔
if not os.path.exists("yolov4.conv.137"): #若預訓練檔不存在就下載
    wget.download('https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.conv.137') #下載檔案


emptydir('cfg')  #建立<cfg>資料夾存放訓練組態資料結構
emptydir(backup)  #在<cfg>資料夾中建立<weights>資料夾存放訓練後的權重檔。



#建立<obj.data>，darknet系統利用此檔內容讀取訓練組態資料結構進行訓練
classes = len(classname)  #分類標籤數量
f = open('cfg/obj.data', 'w')
out = 'classes = ' + str(classes) + '\n'
out += 'train = ' + train + '\n'
out += 'valid = ' + valid + '\n'
out += 'names = ' + names + '\n'
out += 'backup = ' + backup + '\n'
f.write(out)



#建立標籤檔
f = open(names, 'w') #建立<cfg/obj.names>檔
out =''
for cla in classname:
    out += cla + '\n'
f.write(out)



#建立訓練及驗證資料檔
imgfiles = glob.glob('yolodata/*.jpg')  #讀取圖形檔
for i in range(len(imgfiles)):
    imgfiles[i] = imgfiles[i].replace('\\', '/')
    
validnum = int(len(imgfiles) * validratio)  #根據驗證資料比例變數值計算驗證資料數量。
validlist = random.sample(imgfiles, validnum)  #取出驗證資料
f = open(valid, 'w')
out =''

for val in validlist:
    out += val + '\n'

f.write(out)
f = open(train, 'w')
out =''

for tra in imgfiles:
    if tra not in validlist:  #不是驗證資料就是訓練資料
        out += tra + '\n'
f.write(out)



#建立組態檔
cfglist = ['yolov4-obj.cfg'] #將兩個組態檔按名稱建立陣列以便能用迴圈處理
for cfgfile in cfglist:
    shutil.copyfile(cfgfile, 'cfg\\' + cfgfile)  #複製檔案
    f = open('cfg\\' + cfgfile, 'r')  #讀取檔案內容
    content = f.read()

    #替換資料
    content = content.replace('[[batch]]', str(batch))
    content = content.replace('[[subdivisions]]', str(subdivisions))
    content = content.replace('[[classes]]', str(classes))
    content = content.replace('[[filters]]', str((classes+5)*3))
    f = open('cfg\\' + cfgfile, 'w')
    f.write(content)                          

f.close()

print('建立設定資料完成！')