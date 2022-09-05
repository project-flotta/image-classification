# Image Classification tool for Edge Devices

- [Motivation](#need)
- [Resources Used](#model-used)
- [**How to use**](#run)

## Need
Objection detection is of vital importance to many fields, such as autonomous driving, outdoor robotics, and computer vision. Many approaches of object detection can hardly run on the resource-constrained edge devices with the approach of applying real-time object detection on edge devices with low inference time and high accuracy. 

**Why for Edge Devices?** -
The need for on-device data analysis arises in cases where decisions based on data processing have to be made immediately. For example, there may not be sufficient time for data to be transferred to back-end servers, or there is no connectivity at all.
However, with the arrival of powerful, low-energy consumption Internet of Things devices, computations can now be executed on edge devices such as robots themselves. This has given rise to the era of deploying advanced machine learning methods at the edges of the network for “edge-based” ML.

### Model Used 
State-of-the-art lightweight Yolov4-tiny model is especially useful if you have limited compute resources in either research or deployment, and are willing to tradeoff some detection performance for speed. It will display the predicted classes as well as the image with bounding boxes drawn on top of it.

Workload Requirements 
  - Python >=3.7
  - OpenCV 4.6
  
>Docker and Kubernetses required.

## Run
  
You will need a webcam mounted to your workload or it fails with no device connected. Change the device id from 0 to 1/2/3... specific to your requirements
```yaml
 - mountPath: /dev/video0
   name: video
```

**Configurable parameters**
- `threshold = 0.25`        *confidence threshold suggested 25%*
- `timeinterval = 5`    *timeinterval for detection in seconds*
- `capture = True`      *boolean for enabling capture*
  
configuration can be provided to the workload using "`configmaps.yaml`".

**About export folder**
```shell
folder = "../export/images/"  
##The files under the export folder are for data synchronization
```

**JSON Output**
```json
{"title": "2022-09-04_16-08-58", "detected": ["tvmonitor", "laptop", "keyboard"]}
```
Using json for keeping track of detected objects specific to images.

**Customization**

Skip this if you are not training or fine-tuning anything (you simply want to forward flow a trained net)

For example, if you want to work with only 3 classes person, laptop, bag; edit `classes.txt` as follows
```shell
person
laptop
bag
```
And that's it. The algorithm will take care of the rest.

Deploy the workloads on the device.

### **Example Snapshots** 

[![Captured Snapshots example](http://img.youtube.com/vi/RHNfVsw2V7E/0.jpg)](http://www.youtube.com/watch?v=RHNfVsw2V7E) 

(Click on the image to see the video)

**Limitation and Workaround**

Currently the tiny base model detects only 80 object classes `dnn-model/classes.txt` which will be upgraded by training the model on custom datasets of most common object classes. 

## License
This project is released under the Apache 2.0 license. Please see the [LICENSE](https://github.com/dpshekhawat/image-classification/blob/main/LICENSE) file for more information.

## Contributing
We actively welcome your pull requests!