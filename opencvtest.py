# MIT License
# Copyright (c) 2019 JetsonHacks
# See license
# Using a CSI camera (such as the Raspberry Pi Version 2) connected to a
# NVIDIA Jetson Nano Developer Kit using OpenCV
# Drivers for the camera and OpenCV are included in the base image

import cv2
import numpy as np

import os

import robocon	# add

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


def show_camera():

    phase_number = 0

    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    print(gstreamer_pipeline(flip_method=0))
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    if cap.isOpened():
        window_handle = cv2.namedWindow("CSI Camera", cv2.WINDOW_AUTOSIZE)
        # Window
        while cv2.getWindowProperty("CSI Camera", 0) >= 0:
            ret_val, img = cap.read()

		#add

#            height = img.shape[0]
#            width = img.shape[1]
#            print(height)	#720
#            print(width)	#1280

            result = makeMask(img)
            result = img #kill mask

            ball_imgBox = img[0: 200, 540:740]
            ball_color = detectColor(ball_imgBox)


            if phase_number % 3 == 2 and ball_color == 'null':
                print('null')
            else:
                robocon.selectPhase(phase_number % 3, ball_color)
                phase_number+=1


            cv2.rectangle(result, (640-100,0), (640+100,200), (0, 0, 255), 1) # square drowing
            cv2.putText(result, ball_color, (640,250), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255),thickness = 1)	#text drowing
#            cv2.rectangle(img, (0,0),(width/2,height/2), (0, 0, 255), 1 )

		#add end

#            cv2.imshow("CSI Camera", img)	#comment out
            cv2.imshow("CSI Camera", result)	#add

            # This also acts as
            keyCode = cv2.waitKey(30) & 0xFF
            # Stop the program on the ESC key
            if keyCode == 27:
                cv2.imwrite('test.jpg', img)
                break
        cap.release()
        cv2.destroyAllWindows()

        # add
        image = cv2.imread('test.jpg')

#        result = cv2.bitwise_and(img, img, mask=img_mask)
        cv2.imwrite('result.jpg', result)
        #add end

    else:
        print("Unable to open camera")

def detectColor(imgBox):
    b = imgBox.T[0].flatten().mean()
    g = imgBox.T[1].flatten().mean()
    r = imgBox.T[2].flatten().mean()
    color = 'null'
#    if(b< 150 and g< 80 and r< 50):
    if(b< 255 and g< 150 and r< 10):
        color = 'blue'
#    elif(b< 120 and g< 150 and r< 255):
    elif(b< 120 and g< 150 and r< 255 and r>100):
        color = 'red'
    print('b:{:.2f} g:{:.2f} r:{:.2f}'.format(b,g,r))
    return color

def makeMask(img):
    bgrLower = np.array([0, 0, 0])	# BGR
#    bgrUpper = np.array([150, 80, 50])	# Blue
    bgrUpper = np.array([50, 50, 150])	# Red

    img_mask = cv2.inRange(img, bgrLower, bgrUpper)	#mask
    result = cv2.bitwise_and(img, img, mask=img_mask)
    return result


if __name__ == "__main__":
    show_camera()
