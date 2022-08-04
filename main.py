# Object Detection for Edge Devices

import cv2
import os
import time
from datetime import datetime

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
thres = os.getenv("THRES",0.25)        # confidence threshold
timeInterval = os.getenv("TIMEINT",5)    # time interval for capturing
capture = os.getenv("CAPTURE",True)      # capture if True
folder = "images/"  # path to store images


# Object Detection
def objdetect(frame, thres):
    (class_ids, scores, bboxes) = model.detect(
            frame, confThreshold=thres, nmsThreshold=0.4
    )
    for class_id, score, bbox in zip(class_ids, scores, bboxes):
        (x, y, w, h) = bbox
        class_name = classes[class_id]

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


# cap.isOpened() to check cap object has started capturing the frame.
while cap.isOpened() and capture:
    # Get Frames
    ret, frame = cap.read()

    if ret:
        # Error Handling
        try:
            if not os.path.exists(folder):
                os.mkdir(folder)
        except PermissionError as pe:
            print("Cannot create folder "+str(pe))
            break
        else:
            objdetect(frame, thres)
        
        # Saving images to specified folder.
        filename = "{}.jpeg".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        cv2.imwrite(os.path.join(folder, filename), frame)

        # Suspend execution for set time interval.
        time.sleep(timeInterval)
    else:
        break

cap.release()
cv2.destroyAllWindows()