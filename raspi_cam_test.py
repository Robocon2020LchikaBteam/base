# coding: utf-8
# raspicam on jetson nano test
import cv2


# RED_HSV_RANGE_MIN_1 = [0, 130, 30]
# RED_HSV_RANGE_MAX_1 = [2, 255, 255]
RED_HSV_RANGE_MIN_1 = [0, 130, 30]
RED_HSV_RANGE_MAX_1 = [2, 255, 255]
RED_HSV_RANGE_MIN_2 = [100, 90, 30]
RED_HSV_RANGE_MAX_2 = [179, 255, 255]
BLUE_HSV_RANGE_MIN = [55, 70, 10]
BLUE_HSV_RANGE_MAX = [100, 255, 255]

DETECT_AREA_XMIN = 850
DETECT_AREA_XMAX = 1000
DETECT_AREA_YMIN = 200
DETECT_AREA_YMAX = 600


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
WINDOW_NAME = 'Camera Test'

def main():


    cam = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER) #add

#    cam = cv2.VideoCapture(GST_STR, cv2.CAP_GSTREAMER) #coment out

    while True:
        ret, img = cam.read()
        if ret != True:
            break

        # imgBox = img[0: 200, 540:740]
        imgBox = img[DETECT_AREA_YMIN: DETECT_AREA_YMAX, DETECT_AREA_XMIN:DETECT_AREA_XMAX]
        ball_color = detectColor(imgBox)

        # cv2.rectangle(img, (640-100,0), (640+100,200), (0, 0, 255), 1) # square drowing
        cv2.rectangle(img, (DETECT_AREA_XMIN,DETECT_AREA_YMIN), (DETECT_AREA_XMAX,DETECT_AREA_YMAX), (0, 0, 255), 1) # square drowing
        cv2.putText(img, ball_color, (640,250), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255),thickness = 1)	#text drowing

        cv2.imshow(WINDOW_NAME, img)

        key = cv2.waitKey(10)
        if key == 27: # ESC
            break

    cam.release()
    cv2.destroyAllWindows()

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


if __name__ == "__main__":
    main()
