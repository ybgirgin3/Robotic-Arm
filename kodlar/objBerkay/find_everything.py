#!/usr/bin/env python3
# coding: utf-8

# import the necessary packages
from termcolor import colored
from skimage import io
from numpy import interp
import numpy as np
# import pigpio
import argparse
import imutils
import time
import cv2
import os
import sys


# ilk kontrol kısmında servo sürücü kartı yerine direk olarak kendi elimizle servoları kontrol edeceğiz

# ilk etapda sadece iki tane servo motorun kontrolünü sağlayacağız
panServo = 4
tiltServo = 17

# ilk start verildiğindeki pozisyonları
# 180 derece dönebilen servolarda tam 90 derece ayarına denk gelen kısım 1500 değeri almaktadır
# 


panPos = 1500
tiltPos = 1500

"""
servo = pigpio.pi()
# panning servo
servo.set_servo_pulsewidth(panServo, servoDefaultPos)
# tilting servo
servo.set_servo_pulsewidth(tiltServo, servoDefaultPos)
"""

minMov = 1
maxMov = 10


def imShow(path):
  # import matplotlib.pyplot as plt
  import matplotlib
  from matplotlib import pyplot as plt

  # resmi direk olarak açabilmek için kullanılan 
  matplotlib.use("TkAgg")

  image = cv2.imread(path)
  height, width = image.shape[:2]
  resized_image = cv2.resize(image,(3*width, 3*height), interpolation = cv2.INTER_CUBIC)

  fig = plt.gcf()
  fig.set_size_inches(8, 8)
  plt.axis("off")
  #plt.rcParams['figure.figsize'] = [10, 5]
  plt.imshow(cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB))
  plt.show()



def controlServos(x, y, w, h, color):
    global panPos
    global tiltPos

    location = "x: {}, y: {}".format(x, y)

    # kalem benzeri bir cisim istendiğinden dolayı diş fırçası baz alındı
    # if LABELS[classIDs[i]] == sys.argv[1]:
    # if LABELS[classIDs[i]] == "toothbrush":
    # if LABELS[classIDs[i]] == "knife":
    if LABELS[classIDs[i]] != " ":
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        text = "{}: {:.4f} at {}".format(LABELS[classIDs[i]], confidences[i], location)
        # print terminal to objects
        cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        print(colored(text, "green"))
    else:
        print("no object found")


    # servoların kontrol edildiği kısım

    # int(x+(w/2)) > 360 means flame is on the right side of the frame
    if int(x+(w/2)) > 360:
        panPos = int(panPos - interp(int(x+(w/2)), (360, 640), (minMov, maxMov)))

    # int(x+(w/2)) < 280 means flame is on the left side of the frame
    elif int(x+(w/2)) < 280:
        panPos = int(panPos + interp(int(x+(w/2)), (280, 0), (minMov, maxMov)))


    if int(y+(h/2)) > 280:
        tiltPos = int(tiltPos + interp(int(y+(h/2)), (280, 480), (minMov, maxMov)))

    elif int(y+(h/2)) < 200:
        tiltPos = int(tiltPos - interp(int(y+(h/2)), (200, 0), (minMov, maxMov)))


    if not panPos > 2500 or not panPos < 550:

        servo.set_servo_pulsewidth(panServo, panPos)

        print('panServo: {}'.format(panPos))


    if not tiltPos > 2500 or tiltPos < 550:
        # servo.set_servo_pulsewidth(tiltServo, tiltPos)
        print('tiltServo: {}'.format(tiltPos))






# load the COCO class labels our YOLO model was trained on

# objNames = ["dog", "truck", "giraffe"]
# objNames = sys.argv[1]

# get image as command line argument
# frame = io.imread(sys.argv[2])
frame = cv2.imread(sys.argv[2])



labelsPath = os.path.sep.join(["yolo", "coco.names"])
LABELS = open(labelsPath).read().strip().split("\n")

# initialize a list of colors to represent each possible class label
np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
	dtype="uint8")

# derive the paths to the YOLO weights and model configuration
# 1 for yolo
# 2 for weight

configPath = os.path.sep.join(["yolo", f"yolov{sys.argv[1]}.cfg"])
weightsPath = os.path.sep.join(["yolo", f"yolov{sys.argv[1]}.weights"])

"""
if sys.argv[1] == "3":
    weightsPath = os.path.sep.join(["yolo", "yolov3.weights"])
    configPath = os.path.sep.join(["yolo", "yolov3.cfg"])

elif sys.argv[2] == "4":
    weightsPath = os.path.sep.join(["yolo", "yolov4.weights"])
    configPath = os.path.sep.join(["yolo", "yolov4.cfg"])
"""


# In[127]:



# load our YOLO object detector trained on COCO dataset (80 classes)
# and determine only the *output* layer names that we need from YOLO
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]


(W, H) = (None, None)

# if the frame dimensions are empty, grab them
if W is None or H is None:
    (H, W) = frame.shape[:2]

# construct a blob from the input frame and then perform a forward
# pass of the YOLO object detector, giving us our bounding boxes
# and associated probabilities
blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
    swapRB=True, crop=False)
net.setInput(blob)
start = time.time()
layerOutputs = net.forward(ln)
end = time.time()

# initialize our lists of detected bounding boxes, confidences,
# and class IDs, respectively
boxes = []
confidences = []
classIDs = []

# loop over each of the layer outputs
for output in layerOutputs:
    # loop over each of the detections
    for detection in output:
        # extract the class ID and confidence (i.e., probability)
        # of the current object detection
        scores = detection[5:]
        classID = np.argmax(scores)
        confidence = scores[classID]

        # filter out weak predictions by ensuring the detected
        # probability is greater than the minimum probability
        if confidence > 0.5:
            # scale the bounding box coordinates back relative to
            # the size of the image, keeping in mind that YOLO
            # actually returns the center (x, y)-coordinates of
            # the bounding box followed by the boxes' width and
            # height
            box = detection[0:4] * np.array([W, H, W, H])
            (centerX, centerY, width, height) = box.astype("int")

            # use the center (x, y)-coordinates to derive the top
            # and and left corner of the bounding box
            x = int(centerX - (width / 2))
            y = int(centerY - (height / 2))

            # update our list of bounding box coordinates,
            # confidences, and class IDs
            boxes.append([x, y, int(width), int(height)])
            confidences.append(float(confidence))
            classIDs.append(classID)

# apply non-maxima suppression to suppress weak, overlapping
# bounding boxes
idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.3)

# ensure at least one detection exists
if len(idxs) > 0:
    # loop over the indexes we are keeping
    for i in idxs.flatten():
        # extract the bounding box coordinates
        (x, y) = (boxes[i][0], boxes[i][1])
        (w, h) = (boxes[i][2], boxes[i][3])

        # draw a bounding box rectangle and label on the frame
        color = [int(c) for c in COLORS[classIDs[i]]]

        controlServos(x, y, w, h, color)
    
# resmi lokal bilgisayara kaydetmen gösterme işlemi gerçekleşmiyor
img_name = f"{sys.argv[1]}"
cv2.imwrite(f"{img_name}.png", frame)
imShow(f"{img_name}.png")


