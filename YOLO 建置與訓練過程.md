## YOLO 建置與訓練過程

1. 將標記過的標記檔(.xml)放進vocdata/annotations資料夾內(標記使用labelimg)
2. 將有標記的原始圖片放進vocdata/Images內

1. 先執行"1\_voc2yolo.py"程式

    - 目的是將原本的voc格式轉換成yolo所需要的格式

1. 再來執行"2\_makecfg.py"程式(YOLOV4 執行 2\_makecfg-v4.py)
2. 將所有資料壓縮成.zip檔

  

## Google colab

1. 需要調整為GPU模式和連結雲端資料夾資料
2. 將壓縮過後的資料夾上傳至Colab Notebooks

```python
!git clone https://github.com/AlexeyAB/darknet.git
%cd darknet
!sed -i "s/GPU=0/GPU=1/g" Makefile
!sed -i "s/CUDNN=0/CUDNN=1/g" Makefile
!sed -i "s/OPENCV=0/OPENCV=1/g" Makefile
```

```
!make
%cd /content
!ln -s "/content/drive/My Drive/Colab Notebooks" /godrive
!cp /godrive/"壓縮檔名稱"/content
!unzip "壓縮檔名稱"
%cd "壓縮檔名稱"/
!sed -i "s/subdivisions=4/subdivisions=8/g" cfg/yolov3-obj.cfg
!/content/darknet/darknet detector train cfg/obj.data cfg/yolov3-obj.cfg darknet53.conv.74 -dont_show
```

  

如果需要訓練yolo v4，darknet53.conv.74(預處理)需要換成yolov4.conv.137  

檢測訓練成果可以執行 detect\_cam.py