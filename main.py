# Object Detection for Edge Devices

import cv2
import os
import time
from datetime import datetime
import json

# Opencv DNN
net = cv2.dnn.readNet("dnn_model/yolov4-tiny.weights", "dnn_model/yolov4-tiny.cfg")
model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(320, 320), scale=1 / 255)

# Load Class list
classes = []

with open("dnn_model/classes.txt", "r") as f:
    for class_name in f.readlines():
        class_name = class_name.strip()
        classes.append(class_name)

# Initialize camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Configurations
threshold = float(os.getenv("THRES",0.35))  # confidence threshold
timeinterval = int(os.getenv("TIMEINT",5))  # time interval for capturing
capture = bool(os.getenv("CAPTURE",True))  # capture if True
folder = "../export/images/"  # path to store images


# Object Detection
def object_detect(frame, threshold):
    detected = []
    (class_ids, scores, bboxes) = model.detect(
            frame, confThreshold=threshold, nmsThreshold=0.4
    )
    for class_id, score, bbox in zip(class_ids, scores, bboxes):
        (x, y, w, h) = bbox
        class_name = classes[class_id]
        
        if class_name not in detected:
            detected.append(class_name)

        cv2.putText(
            frame,
            class_name.capitalize(),
            (x, y - 10),
            cv2.FONT_HERSHEY_PLAIN,
            fontScale=1,
            color=(0, 200, 50),
            thickness=2,
        )

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            color=(0, 200, 50),
            thickness=2,
        )

    return detected


def write_metadata(title, detected, folder):
    data = {
        "title": title,
        "detected": detected
    }
    name = f"{title}.json"
    with open(os.path.join(folder, name), "w") as file:
        json.dump(data, file)


def save_data(detected, folder):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{timestamp}.jpeg"
    cv2.imwrite(os.path.join(folder, filename), frame)
    write_metadata(timestamp, detected, folder)


try:
    if not os.path.exists(folder):
        os.mkdir(folder)
except PermissionError as pe:
    print(f"Cannot create folder {pe}")
else:
    while cap.isOpened() and capture:
        # Get Frames
        ret, frame = cap.read()

        if ret:
            detected = object_detect(frame, threshold)
            
            if len(detected) != 0:
                save_data(detected, folder)
            # Suspend execution for set time interval.
            time.sleep(timeinterval)
        else:
            break

cap.release()