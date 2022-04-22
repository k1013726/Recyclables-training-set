def emptydir(dirname):  #清空資料夾
    if os.path.isdir(dirname):  #資料夾存在就刪除
        shutil.rmtree(dirname)
        sleep(2)  #需延遲,否則會出錯
    os.mkdir(dirname)  #建立資料夾

import glob
import os, shutil
from time import sleep
from bs4 import BeautifulSoup as bs

classes = ['Bottle','Beverage Pack','Cans','plastic','Paper container','paper']  #分類標籤

print('開始建立訓練資料！')
emptydir('yolodata')  #建立訓練資料夾
imgfiles = glob.glob('vocdata\\images\\*.jpg')  #讀取圖形檔
#複製圖形檔
for fimg in imgfiles:
    fname = fimg.split('\\')[-1]  #取得檔名
    shutil.copyfile(fimg, 'yolodata\\' + fname)  #複製檔案
#轉換voc為yolo標記
lbfiles = glob.glob('vocdata\\annotations\\*.xml')  #讀取標記檔
for flb in lbfiles:
    fxml = open(flb) 
    content = fxml.read()  #讀取voc標記
    sp = bs(content, 'html.parser')  #轉為BeautifulSoup格式
    imgW = float(sp.find('width').text)  #圖形寬度
    imgH = float(sp.find('height').text)  #圖形高度 
    objs = sp.find_all('object')
    out = ''
    for obj in objs:
        name = obj.find('name').text  #標記
        xmin = float(obj.find('xmin').text)  #左上角x坐標
        ymin = float(obj.find('ymin').text)  #左上角y坐標
        xmax = float(obj.find('xmax').text)  #右下角x坐標
        ymax = float(obj.find('ymax').text)  #右下角y坐標
        x = (xmin + (xmax - xmin) / 2) / imgW  #中心點x坐標比例
        y = (ymin + (ymax - ymin) / 2) / imgH  #中心點y坐標比例
        w = (xmax - xmin) / imgW  #圖形寬度比例
        h = (ymax - ymin) / imgH  #圖形高度比例
        out += str(classes.index(name)) + ' ' + str(x) + ' ' + str(y) + ' ' + str(w) + ' ' + str(h) + '\n'
    fname = flb.replace('vocdata\\annotations', 'yolodata').replace('.xml', '.txt')  #存檔路徑
    ftxt = open(fname, 'w')
    ftxt.write(out)  #寫入檔案

fxml.close()
ftxt.close()
print('建立訓練資料完成！')
    
