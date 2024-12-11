import cv2
import numpy as np
import time
cap = cv2.VideoCapture('road_line.mp4')
img_size = [200, 360]
src = np.float32([[0, 0],
                  [0, 200],
                  [360, 200],
                  [360, 0]])

dct = np.float32([[0, img_size[0]],
                  [img_size[1], img_size[0]],
                  [img_size[1], 0],
                  [0, 0]])
src_draw = np.array(src, dtype=np.int32)
cn = 0
while (cv2.waitKey(1) != 27):
    ret, frame = cap.read()
    if ret == False:
        print('End video')
        break
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    cn1 = 0
    time.sleep(0.1)
    rezized = cv2.resize(frame, (img_size[1], img_size[0]))
    cv2.imshow('222', rezized)
    r_channel = rezized[:,:,2]
    binary = np.zeros_like(r_channel)
    binary[(r_channel > 170)] = 0
    #cv2.imshow('22', binary)
    hls = cv2.cvtColor(rezized, cv2.COLOR_BGR2HLS)
    s_channel = rezized[:, :, 2]
    binary2 = np.ones_like(s_channel)
    binary2[(r_channel > 170)] =0
    allBinary = np.ones_like(binary)
    allBinary[((binary==1)|(binary2==1))]=255
    cv2.imshow('221', allBinary)
    for e in range(0, 180, 20):
        cn = 0
        max_x = []
        x = []
        for i in allBinary[e][:180]:
            if i == 255 or i == 100:
                x.append(cn)
            else:
                 if len(max_x) < len(x):
                     max_x = x
                     x = []
                 else:
                     x = []
            cn += 1
        cv2.rectangle(allBinary, (max_x[0], e+1), (max_x[-1], e+18), 100, 2)
        cn = 180
        max_y = []
        y = []
        for i in allBinary[e][180:]:
            if i == 255 or i == 100:
                y.append(cn)
            else:
                 if len(max_y) < len(y):
                     max_y = y
                     y = []
                 else:
                     y = []
            cn += 1
        cv2.rectangle(allBinary, (max_y[0], e+1), (max_y[-1], e+18), 100, 2)
        cv2.line(allBinary, (max_x[-1]+abs(max_x[-1] - max_y[0])//2, e+1), (max_x[-1]+abs(max_x[-1] - max_y[0])//2, e+18), 225, 2)
    cv2.line(allBinary, (180, 0), (180, 180), 111, 2)
    cv2.imshow('line_rec', allBinary)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        time.sleep(20)

print("ajdlasjdlkmas")