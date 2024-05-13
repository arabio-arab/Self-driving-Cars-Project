# -*- coding: utf8 -*-
import cv2
import cv2 as cv
import numpy as np
import time
import socket
import sys
# import motor
# import servo
import time
import serial

# sr = serial.Serial("COM11", 38400, timeout=1)
# if sr.isOpen():
#     print("Port is already open")
# else:
#     sr.open()


# the first programm :1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111

def DetectLineSlope(src):
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    can = cv2.Canny(gray, 50, 200, None, 3)
    height = can.shape[0]
    rectangle = np.array([[(0, height), (120, 300), (520, 300), (640, height)]])
    mask = np.zeros_like(can)
    cv2.fillPoly(mask, rectangle, 255)
    masked_image = cv2.bitwise_and(can, mask)
    ccan = cv2.cvtColor(masked_image, cv2.COLOR_GRAY2BGR)

    line_arr = cv2.HoughLinesP(masked_image, 1, np.pi / 180, 20, minLineLength=30, maxLineGap=30)
    line_R = np.empty((0, 5), int)  
    line_L = np.empty((0, 5), int)  
    if line_arr is not None:
        line_arr2 = np.empty((len(line_arr), 5), int)
        for i in range(0, len(line_arr)):
            temp = 0
            l = line_arr[i][0]
            line_arr2[i] = np.append(line_arr[i], np.array((np.arctan2(l[1] - l[3], l[0] - l[2]) * 180) / np.pi))
            if line_arr2[i][1] > line_arr2[i][3]:
                temp = line_arr2[i][0], line_arr2[i][1]
                line_arr2[i][0], line_arr2[i][1] = line_arr2[i][2], line_arr2[i][3]
                line_arr2[i][2], line_arr2[i][3] = temp
            if line_arr2[i][0] < 320 and (abs(line_arr2[i][4]) < 170 and abs(line_arr2[i][4]) > 95):
                line_L = np.append(line_L, line_arr2[i])
            elif line_arr2[i][0] > 320 and (abs(line_arr2[i][4]) < 170 and abs(line_arr2[i][4]) > 95):
                line_R = np.append(line_R, line_arr2[i])
    line_L = line_L.reshape(int(len(line_L) / 5), 5)
    line_R = line_R.reshape(int(len(line_R) / 5), 5)

    try:
        line_L = line_L[line_L[:, 0].argsort()[-1]]
        degree_L = line_L[4]
        cv2.line(ccan, (line_L[0], line_L[1]), (line_L[2], line_L[3]), (0, 0, 255), 10, cv2.LINE_AA)
    except:
        degree_L = 0
    try:
        line_R = line_R[line_R[:, 0].argsort()[0]]
        degree_R = line_R[4]
        cv2.line(ccan, (line_R[0], line_R[1]), (line_R[2], line_R[3]), (0, 0, 255), 10, cv2.LINE_AA)
    except:
        degree_R = 0
    mimg = cv2.addWeighted(src, 1, ccan, 1, 0)
    return mimg, degree_L, degree_R


# the second program:2222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222


def thresholding(image, lower_values, upper_values):
    imageHsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    image_mask = cv.inRange(imageHsv, lower_values, upper_values)
    image_thresh = cv.bitwise_and(image, image, mask = image_mask)
    return image_mask

def warp_image(image, points, w, h):
    pt1 = np.float32(points)
    pt2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    mat = cv.getPerspectiveTransform(pt1, pt2)
    img_warp = cv.warpPerspective(image, mat, (w, h-80))
    return img_warp

def get_histogram(img, min_perc = 0.5, region = 0.3):
    hist_values = np.sum(img[int(img.shape[0]*region):,:], axis = 0)
    max_value = np.max(hist_values)
    min_thresh_value = min_perc*max_value
    index_array = np.where(hist_values >= min_thresh_value)
    base_point = np.average(index_array)
    #cv.circle(img,(base_point,img.shape[0]),20,(0,255,0),cv.FILLED)
    return int(base_point)



#cv.namedWindow("Trackbars")
cv.namedWindow("Thresh")

curveList = []

#cv.createTrackbar("gauche doite", "Trackbars", 0, 70, lambda x: None)
#cv.createTrackbar("devant", "Trackbars", 0, 70, lambda x: None)
# moteur = motor.Motor(33, 31, 29, 40, 38, 36)

def get_lane_curve(image, width=480, height=240):
    
    # lower_values = np.array((0, 0,0))
    # upper_values = np.array((179,255,118))
    lower_values = np.array((0, 0,114))
    upper_values = np.array((179,53,255))    
    w_top = 0
    h_top =140
    font = cv.FONT_HERSHEY_SIMPLEX
    w_bottom = 0
    h_bottom = 240
    points = np.float32([[w_top, h_top], [int(width-w_top), h_top], [w_bottom, h_bottom], [int(width-w_bottom), h_bottom]])
    image_thresh = thresholding(image, lower_values, upper_values)
    image_warped = warp_image(image_thresh, points, int(width), int(height))
#    # Determine the splitting point (you can adjust this based on your requirements)
#     splitting_point = image_warped.shape[0] //2  # Split at the middle horizontally

#     # # Split the image into two parts
#     # # upper_half = image_warped[:splitting_point, :]
#     image_warped = image_warped[splitting_point:, :]

    base_point = get_histogram(image_warped, 0.5, region=0)
    color = (0, 0, 255)
    mid_point= get_histogram(image_warped, 0.8, region=0.5)
    #s,m=getHistogram(image_warped, 0.45, region=0)
    #print(m)
    start_point = (mid_point, 0)
    end_point = (mid_point, int(height))
    color = (0, 0, 255)
    thickness = 2
    cv.line(image, start_point, end_point, color, thickness)
    cv.circle(image, (base_point, int(height)), 10, (255, 0, 0), cv.FILLED)
    curve = base_point-mid_point
    
    #if mid_point < int(width/2)-70: curve = -15
    #elif mid_point > int(width/2)+70: curve = 15
    norm_curve=curve
       

    if norm_curve > 25:
        cv.putText(image, f"{norm_curve} droite", (50, 50), color = (255, 255, 0), fontFace=font, thickness=2, fontScale=1)
        p2="d"
        
    elif norm_curve <-33 :
        cv.putText(image, f"{norm_curve} gauche", (50, 50), color = (255, 255, 0), fontFace=font, thickness=2, fontScale=1)
        p2="g"
    else:
        cv.putText(image, f"{norm_curve} tout droit", (50, 50), color = (255, 255, 0), fontFace=font, thickness=2, fontScale=1)
        p2="C"
    return image, image_warped, norm_curve, image_thresh,p2
        

# main function 33333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333
cap = cv2.VideoCapture(r"C:\Users\pc\Downloads\video (2).m4v")
# cap.open('http://192.168.43.1:8080/video')
# cap.open('http://100.65.0.183:8080/video')

# motor.Forward(21)
# servo.Go()
while cap.isOpened():
    
    ret, frame = cap.read()
    if ret:
            rotated_frame=frame  #cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            # frame = rotated_frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

            frame = cv2.resize(frame, (640, 360))
            font = cv.FONT_HERSHEY_SIMPLEX
            cv2.imshow('ImageWindow', DetectLineSlope(frame)[0])

            l, r = DetectLineSlope(frame)[1], DetectLineSlope(frame)[2]
            if abs(l) <= 155 or abs(r) <= 155:
                if l ==0 or r == 0:
                    if l < 0 or r < 0:
                        # servo.Turnleft()
                        # sr.write(b"g")
                        p1="g"
 
                        cv.putText( frame, f"{l,r} gauche", (50, 50), color = (255, 255, 0), fontFace=font, thickness=2, fontScale=1)

                        print('_left')
                        

                    elif l > 0 or r > 0:
                        # servo.Turnright()
                        # sr.write(b"C")
                        p1="d"
                        cv.putText( frame, f"{l,r} droite", (50, 50), color = (255, 255, 0), fontFace=font, thickness=2, fontScale=1)
                        print('_right')
                elif abs(l-15) > abs(r):  # 우회전 해야하는상황
                    # servo.Turnright()
                    # sr.write(b"d")
                    p1="d"
                    cv.putText( frame, f"{l,r} droite", (50, 50), color = (255, 255, 0), fontFace=font, thickness=2, fontScale=1)

                    print('_right')
                elif abs(r+15) > abs(l):  # 좌회전 해야하는상황
                    # servo.Turnleft()
                    # sr.write(b"g")
                    print('_left')
                    p1="g"
                    cv.putText( frame, f"{l,r} gauche", (50, 50), color = (255, 255, 0), fontFace=font, thickness=2, fontScale=1)
                else:                                   # 직진
                    # servo.Go()
                    # sr.write(b"C")
                    print('go')
                    p1="C"
                    cv.putText( frame, f"{l,r} tout droit", (50, 50), color = (255, 255, 0), fontFace=font, thickness=2, fontScale=1)

            else:
                if l > 155 or r > 155:
                    # servo.HardTurnright()

                    # sr.write(b"d")
                    p1="d"
                    cv.putText( frame, f"{l,r} droite", (50, 50), color = (255, 255, 0), fontFace=font, thickness=2, fontScale=1)
                    print('hard right')

                elif l < -155 or r < -155:
                    # servo.HardTurnleft()
                    # sr.write(b"g")
                    p1="g"
                    cv.putText( frame, f"{l,r} gauche", (50, 50), color = (255, 255, 0), fontFace=font, thickness=2, fontScale=1)
                    print('hard left')

            
            cv2.imshow('ImageWindow1111111111111arabi', frame)
            key = cv.waitKey(1)
     
        # # ret, image = cap.read()
        # rotated_frame = rotated_frame = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE)

            # if rotated_frame is None:
            #     print("Error: Unable to load image")
            # else:
            #     rotated_frame = cv.resize(rotated_frame, (480, 240))
            # image_out, img_warped, norm_curve,image_thresh ,p2= get_lane_curve(rotated_frame)
            # #  exicutio ndes command :::::::::
            # if p1==p2:
            #     if p2=="C":
            #      sr.write(b"C")

            #     elif p2=="g":
            #      sr.write(b"g") 

            #     elif p2=="d":
            #      sr.write(b"d")  

            # else:
            #     if p1=="C" and ( p2=="d" or p2=="D" ):
            #      sr.write(b"C")

            #     elif p1=="d"  or   p2=="C" :
            #      sr.write(b"d") 

            #     elif p1=="g" and p2=="C":
            #      sr.write(b"g") 

            #     elif p1=="C" and  p2=="G":
            #      sr.write(b"G")
            #     elif p2=="G":
            #      sr.write(b"G")
            #     elif p1=="C" and  p2=="g":
            #      sr.write(b"C")  
            #     # else:
            #     #     if p1=="C":
            #     #      sr.write(b"C")

            #     #     elif p1=="g":
            #     #      sr.write(b"g") 
            #     #     elif p1=="d":
            #     #      sr.write(b"d")

                    
                
                        
            # cv.imshow("ImageW", img_warped)
            # cv.imshow("image_thresh",image_thresh)
            # cv.imshow("Image_arabi_2222222", image_out)
            
            
            # #cv.imshow("Image2_", image_thresh)
            # key = cv.waitKey(1)
            # print(norm_curve)
   





















