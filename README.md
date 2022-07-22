# Image Classification tool for Edge Devices

## Table of contents

- [Motivation](#why-is-the-need)
- [Resources Used](#model-used)
- [**How to use**](#how-to-use)
- [[WIP]](#work-in-progress)

## Why is the need
Objection detection is of vital importance to many fields, such as autonomous driving, outdoor robotics, and computer vision. Many approaches of object detection can hardly run on the resource-constrained edge devices with the approach of applying real-time object detection on edge devices with low inference time and high accuracy. 

**Why for Edge Devices?** -
The need for on-device data analysis arises in cases where decisions based on data processing have to be made immediately. For example, there may not be sufficient time for data to be transferred to back-end servers, or there is no connectivity at all.
However, with the arrival of powerful, low-energy consumption Internet of Things devices, computations can now be executed on edge devices such as robots themselves. This has given rise to the era of deploying advanced machine learning methods at the edges of the network for “edge-based” ML.

## Model Used 
YOLOv4-tiny is especially useful if you have limited compute resources in either research or deployment, and are willing to tradeoff some detection performance for speed. It will display the predicted classes as well as the image with bounding boxes drawn on top of it.

## How to use
- Requirements (docker will take care of these)
  - Python 3.10
  - OpenCV 4.6
  - YOLOv4-tiny (.weights and .cfg)
  
You will need a webcam connected to your device that OpenCV connect to or it won't work. If you have multiple webcams connected and want to connect a specific one to use, change the device id from 0 to 1 (OpenCV uses webcam 0 by default).
```
docker run --device /dev/video0 {imagename}
```
**Configurable parameters**
- `thres = 0.25`        *confidence threshold currently 25%*
- `timeInterval = 5`    *timeinterval for capturing every 5 secs*
- `capture = True`      *start capturing if True*
- `folder = "images/"`  *path to store images*

### **Example Snapshots** 

[![Captured Snapshots example](http://img.youtube.com/vi/RHNfVsw2V7E/0.jpg)](http://www.youtube.com/watch?v=RHNfVsw2V7E)

## Limitation and Workaround
Currently the tiny base model detects only 80 object classes `dnn-model/classes.txt` which will be upgraded by training the model on custom datasets of most common object classes. 

### Improvements done
- captured image size reduced to ~100KB which was used to be ~300KB.
- improved exit strategy.

### Work in Progress
- Creating a web presentation for the captured snapshots
- Writing test cases
