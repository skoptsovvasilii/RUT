import cv2
import numpy as np
import time
#import serial



cap = cv2.VideoCapture(0)

img_size = [200, 360]

src = np.float32([[50, 200],
                  [280, 200],
                  [260, 120],
                  [100, 120]])

dct = np.float32([[0, img_size[0]],
                  [img_size[1], img_size[0]],
                  [img_size[1], 0],
                  [0, 0]])

src_draw = np.array(src, dtype=np.int32)

cn = 0

#ser = serial.Serial('/COM8', 9600, timeout=1.0)
#time.sleep(2)
#ser.reset_input_buffer()
#print('serial ok')

while (cv2.waitKey(1) != 27):
    ret, frame = cap.read()
    if ret == False:
        print('End video')
        break

    cn1 = 0
    time.sleep(0.1)
    rezized = cv2.resize(frame, (img_size[1], img_size[0]))
    cv2.imshow('222', rezized)
    r_channel = rezized[:,:,2]
    binary = np.zeros_like(r_channel)
    binary[(r_channel > 200)] = 1
    #cv2.imshow('22', binary)
    hls = cv2.cvtColor(rezized, cv2.COLOR_BGR2HLS)
    s_channel = rezized[:, :, 2]
    binary2 = np.zeros_like(s_channel)
    binary2[(r_channel > 160)] = 1

    allBinary = np.zeros_like(binary)
    allBinary[((binary==1)|(binary2==1))]=255
    cv2.imshow('221', allBinary)

    allBinary_visial1 = allBinary.copy()
    cv2.polylines(allBinary_visial1, [src_draw], True, 255)
    cv2.imshow('ll', allBinary_visial1)

    M = cv2.getPerspectiveTransform(src, dct)
    warp = cv2.warpPerspective(allBinary, M, (img_size[1], img_size[0]), flags = cv2.INTER_LINEAR)
    cv2.imshow('1', warp)

    histogram = np.sum(warp[warp.shape[0]//2:,:], axis=0)

    midpint = histogram.shape[0] // 2
    ind_whitestcolumpL = np.argmax(histogram[:midpint])
    ind_whitestcolumpR = np.argmax(histogram[midpint:]) + midpint

    warp_visual = warp.copy()
    cv2.line(warp_visual, (ind_whitestcolumpL, 0), (ind_whitestcolumpL, warp_visual.shape[0]),110, 2)
    cv2.line(warp_visual, (ind_whitestcolumpR, 0), (ind_whitestcolumpR, warp_visual.shape[0]),110, 2)

    cv2.imshow('123456', warp_visual)

    nwindow = 9
   # window_height = np.int(warp.shape[0] / nwindow)
    window_wight = 25
    XcenterLeftwindow  = ind_whitestcolumpL
    XcenterRigthwindow  = ind_whitestcolumpR

    left_line_index = np.array([], dtype=np.int16)
    rigth_line_index = np.array([], dtype=np.int16)

    out_img = np.dstack((warp, warp, warp))

    nonzer = warp.nonzero()
    White_pixeY = np.array(nonzer[0])
    White_pixelX = np.array(nonzer[1])


    for window in range(nwindow):
        wind_y1 = warp.shape[0]  -(window +      1) * window_wight
        wind_y2 =warp.shape[0]  -(window) * window_wight

        left_win_x1 = XcenterLeftwindow - window_wight
        left_win_x2 = XcenterLeftwindow + window_wight

        rigth_win_x1 = XcenterRigthwindow - window_wight
        rigth_win_x2 = XcenterRigthwindow + window_wight



        cv2.rectangle(out_img, (left_win_x1, wind_y1), (left_win_x2, wind_y2), (50 + window*21, 0, 0), 2)
        cv2.rectangle(out_img, (rigth_win_x1, wind_y1), (rigth_win_x2, wind_y2), (0, 0,50 + window*21), 2)
        cv2.imshow('99', out_img)

        good_left_index = ((White_pixeY>= wind_y1) & (White_pixeY <= wind_y2) & (White_pixelX >= left_win_x1) & (White_pixelX<= left_win_x2)).nonzero()[0]
        good_rigth_index = ((White_pixeY>= wind_y1) & (White_pixeY <= wind_y2) & (White_pixelX >= rigth_win_x1) & (White_pixelX<= rigth_win_x2)).nonzero()[0]

        left_line_index =  np.concatenate((left_line_index, good_left_index))
        rigth_line_index =  np.concatenate((rigth_line_index, good_rigth_index))


        if len(good_left_index) > 50:
            XcenterLeftwindow = int(np.mean(White_pixelX[good_left_index]))
        if len(good_rigth_index) > 50:
            XcenterRigthwindow = int(np.mean(White_pixelX[good_rigth_index ]))




    out_img[White_pixeY[left_line_index], White_pixelX[left_line_index]] = [255, 0, 0]
    out_img[White_pixeY[rigth_line_index], White_pixelX[rigth_line_index]] = [0, 0, 255]
    cv2.imshow('window', out_img)

    lefx =    White_pixelX[left_line_index]
    #print(lefx)
    lefty =   White_pixeY[left_line_index]
    #print(lefty)
    rigthx =  White_pixelX[rigth_line_index]
   # print(rigthx)
    rigthty = White_pixeY[rigth_line_index]
  #  print(rigthty)






    cv2.line(out_img, (180, 0), (180, warp_visual.shape[0]), (255, 255, 0), 3)

    cv2.imshow('end', out_img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        time.sleep(20)


















'''

import RPi.GPIO as gpio
import time
gpio.setmode(gpio.BOARD)

gpio.setup(7, gpio.OUT)
gpio.setup(11, gpio.OUT)
gpio.setup(13, gpio.OUT)
gpio.setup(15, gpio.OUT)
gpio.setup(16, gpio.OUT)
gpio.setup(18, gpio.OUT)
pwm = gpio.PWM(16, 100)
pwm2 = gpio.PWM(18, 100)
pwm.start(0)
pwm2.start(0)
gpio.output(7, True)
gpio.output(11, False)
gpio.output(13, True)
gpio.output(15, False)
for i in range(1, 100):
        pwm.ChangeDutyCycle(i)
        pwm2.ChangeDutyCycle(i)
        time.sleep(0.1)
pwm.stop()
pwm2.stop()
'''