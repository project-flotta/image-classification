# Object Detection for Edge Devices

import cv2
import os
from os import path
import time
from datetime import datetime

# Opencv DNN
net = cv2.dnn.readNet("dnn_model/yolov4-tiny.weights", "dnn_model/yolov4-tiny.cfg")
model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(320, 320), scale=1/255)

# Load Class list
classes = []
with open("dnn_model/classes.txt", "r") as f:
    for class_name in f.readlines():
        class_name = class_name.strip()
        classes.append(class_name)

#print("Objects list")
#print("classes")

# Initialize camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

start_time = time.time()

# Configurations
thres = 0.25        # confidence threshold
timeInterval = 5    # timeinterval for capturing
capture = True      # capture if True
folder = "images/"  # path to store images

if not os.path.exists(folder):
    os.mkdir(folder)

# Font/Box style used for labelling object detected
font = cv2.FONT_HERSHEY_PLAIN
font_scale = 1
thick = 2

while True:
    if cap.isOpened():
        # Get Frames
        ret, frame = cap.read()
        if ret:
            # Object Detection
            (class_ids, scores, bboxes) = model.detect(frame, confThreshold = thres, nmsThreshold=.4)
            for class_id, score, bbox in zip(class_ids, scores, bboxes):
                (x, y, w, h) = bbox
                class_name = classes[class_id]

                cv2.putText(frame, class_name.capitalize(), (x,y - 10), font, font_scale, (0, 200, 50), thick)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 200, 50), thick)
            # Uncomment below lines to see real time feed of object detection
            #cv2.imshow("ObjectDetection", frame)
            #cv2.waitKey(1)
            if int(round(time.time()-start_time, 2)) >= timeInterval:
                filename = "{}.png".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
                cv2.imwrite(os.path.join(folder,filename), frame)
                start_time = time.time()
        if capture != True:
            break

cap.release()
cv2.destroyAllWindows()