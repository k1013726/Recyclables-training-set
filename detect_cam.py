#opencv 版本需為 4.x
import cv2
import numpy as np

net = cv2.dnn.readNetFromDarknet("cfg/yolov3.cfg","yolov3.weights")  #讀取模型
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]  #輸出圖形規格
classes = [line.strip() for line in open("data/coco.names")]  #分類標籤
colors = [(255,0,0), (0,255,0), (0,0,255), (127,0,255), (0,125,255)]  #框選顏色

cap = cv2.VideoCapture(0)   #打開攝影機
while(True):
    ret, img = cap.read()   #讀取影像
    height, width, channels = img.shape 
    blob = cv2.dnn.blobFromImage(img, 1/255.0, (416, 416), (0, 0, 0), True, crop=False)  #圖形預處理以符合輸入圖片規格
    net.setInput(blob)  #圖片輸入模型
    outs = net.forward(output_layers)  #偵測結果
    
    class_ids = []  #存標籤索引
    confidences = []  #存信心指數
    boxes = []  #存矩形坐標
        
    for out in outs:
        for detection in out:
            tx, ty, tw, th, confidence = detection[0:5]  #取得坐標及信心資料
            scores = detection[5:]
            class_id = np.argmax(scores)  #取得標籤索引
            if confidence > 0.3:  #信心指數大於0.3才算
                center_x = int(tx * width)
                center_y = int(ty * height)
                w = int(tw * width)
                h = int(th * height)
                # 取得箱子方框座標
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.3, 0.4)  #消除重疊框選
    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[class_ids[i]%5]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 1)
            cv2.putText(img, label, (x, y - 5), font, 1, color, 2)
    cv2.imshow('win', img)
    if cv2.waitKey(10) == 27:  #按ESC鍵結束迴圈
        break

cap.release()
cv2.destroyAllWindows()





