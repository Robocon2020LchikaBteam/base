# MIT License
# Copyright (c) 2019 JetsonHacks
# See license
# Using a CSI camera (such as the Raspberry Pi Version 2) connected to a
# NVIDIA Jetson Nano Developer Kit using OpenCV
# Drivers for the camera and OpenCV are included in the base image

import cv2
import numpy as np

import time
import os

import robocon	# add


RED_HSV_RANGE_MIN_1 = [0, 130, 30]
RED_HSV_RANGE_MAX_1 = [2, 255, 255]
RED_HSV_RANGE_MIN_2 = [100, 90, 30]
RED_HSV_RANGE_MAX_2 = [179, 255, 255]
BLUE_HSV_RANGE_MIN = [55, 70, 10]
BLUE_HSV_RANGE_MAX = [100, 255, 255]

DETECT_AREA_XMIN = 540	#width 1280
DETECT_AREA_XMAX = 740
DETECT_AREA_YMIN = 200
DETECT_AREA_YMAX = 600

# gstreamer_pipeline returns a GStreamer pipeline for capturing from the CSI camera
# Defaults to 1280x720 @ 60fps
# Flip the image by setting the flip_method (most common values: 0 and 2)
# display_width and display_height determine the size of the window on the screen


def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
    framerate=60,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


def detectColor(imgBox):
    # https://qiita.com/Zumwalt/items/4d9bc15608483fa77476
    # BGRからHSVに変換
    imgBoxHsv = cv2.cvtColor(imgBox,cv2.COLOR_BGR2HSV)
    h = imgBoxHsv.T[0].flatten().mean()
    s = imgBoxHsv.T[1].flatten().mean()
    v = imgBoxHsv.T[2].flatten().mean()

    value_hsv = [h, s, v]
    color_red=color_blue=0

    for i in range(3):
        if(value_hsv[i] > RED_HSV_RANGE_MIN_1[i] and value_hsv[i] < RED_HSV_RANGE_MAX_1[i]):
            color_red += 1
        elif(value_hsv[i] > RED_HSV_RANGE_MIN_2[i] and value_hsv[i] < RED_HSV_RANGE_MAX_2[i]):
            color_red += 1 
        if(value_hsv[i] > BLUE_HSV_RANGE_MIN[i] and value_hsv[i] < BLUE_HSV_RANGE_MAX[i]):
            color_blue += 1

    print('h:{:.2f} s:{:.2f} v:{:.2f}'.format(h,s,v))

    color = 'null'
    if color_red >= 3:
        color = 'red'
    elif color_blue == 3:
        color = 'blue'

    return color

def makeMask(img):
    bgrLower = np.array([0, 0, 0])	# BGR
#    bgrUpper = np.array([150, 80, 50])	# Blue
    bgrUpper = np.array([50, 50, 150])	# Red

    img_mask = cv2.inRange(img, bgrLower, bgrUpper)	#mask
    result = cv2.bitwise_and(img, img, mask=img_mask)
    return result

WINDOW_NAME = 'Camera Test'

def Watch_camera():
    cam = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER) #add
    ball_color = 'null'
    ii = 0

    while True:
        ret, img = cam.read()
        if ret != True:
            break

        if(ii>100):    #時間で色味変わるので入れた
            ball_imgBox = img[DETECT_AREA_YMIN: DETECT_AREA_YMAX, DETECT_AREA_XMIN:DETECT_AREA_XMAX]
            ball_color = detectColor(ball_imgBox)

            cv2.rectangle(img, (DETECT_AREA_XMIN,DETECT_AREA_YMIN), (DETECT_AREA_XMAX,DETECT_AREA_YMAX), (0, 0, 255), 1) # square drowing
            cv2.putText(img, ball_color, (640,250), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255),thickness = 1)	#text drowing

        cv2.imshow(WINDOW_NAME, img)

        key = cv2.waitKey(10)
        if key == 27 or ball_color != 'null': # ESC
            break
        
        ii += 1

    cam.release()
    cv2.destroyAllWindows()

    return ball_color


def main():
    robocon.selectPhase(0,0)	#ini
    robocon.selectPhase(1,0)	#stop
    while True:
	    b_color = Watch_camera()
	    robocon.selectPhase(2,b_color)


if __name__ == "__main__":
	main()
#    show_camera()

