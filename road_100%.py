import cv2
import torch
#import tracker
import numpy as np
import math
from tkinter import*
from tkinter.ttk import *
import time
import math


class Tracker:
    def __init__(self):
        # Store the center positions of the objects
        self.center_points = {}
        # Keep the count of the IDs
        # each time a new object id detected, the count will increase by one
        self.id_count = 0


    def update(self, objects_rect):
        # Objects boxes and ids
        objects_bbs_ids = []

        # Get center point of new object
        for rect in objects_rect:
            x, y, w, h = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            # Find out if that object was detected already
            same_object_detected = False
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])

                if dist < 35:
                    self.center_points[id] = (cx, cy)
#                    print(self.center_points)
                    objects_bbs_ids.append([x, y, w, h, id])
                    same_object_detected = True
                    break

            # New object is detected we assign the ID to that object
            if same_object_detected is False:
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1

        # Clean the dictionary by center points to remove IDS not used anymore
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center

        # Update dictionary with IDs not used removed
        self.center_points = new_center_points.copy()
        return objects_bbs_ids



model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
cap = cv2.VideoCapture(0)


def POINTS(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:

        colorsBGR = [x, y]
        print(colorsBGR)


cv2.namedWindow('FRAME')
cv2.setMouseCallback('FRAME', POINTS)

tracker = Tracker()
window = Tk()

window.title('GFG')


weight, height = 1020, 800

k_cirle = 250
k_rec = 50

canvas = Canvas(window, width=weight, height=height)
canvas.pack()
while True:
    time.sleep(0.1)
    ret, frame = cap.read()
    frame = cv2.resize(frame, (weight, height))
    result = model(frame)
    canvas.delete('all')

    detect_rec = canvas.create_rectangle(650, 70, 980, 130, fill='red', bg=None, width=2)
    detect_text = canvas.create_text(800, 100, text='БРАТЬ НЕЛЬЗЯ', fill='white', font=('Purisa', 20))


    canvas.create_oval(weight//2-k_cirle, height-k_cirle, weight//2+k_cirle, height+k_cirle, fill='green')
    canvas.create_rectangle(weight//2-k_rec, height-k_rec, weight//2+k_rec, height, fill='red')

    parametrs = []
    parametrs_xy = []
    cn = 1000
    for  index, row in result.pandas().xyxy[0].iterrows():
        if row['name'] in ['vase', 'bottle']:
            k = ((row['xmin']-weight//2)**2+(np.mean(row['ymax']-row['ymin'])- height-k_rec)**2)**0.5
            if k<cn:
                cn = k
                parametrs_xy = [row['xmin'], row['ymin'], row['xmax'], row['ymax']]
                parametrs = [weight//2, height-k_rec, (row['xmax']+ row['xmin'])//2, (row['ymax'] + row['ymin'])//2]
                print(parametrs)


            print(index)
            print()


            print(row)
            canvas.create_rectangle(row['xmin'], row['ymin'], row['xmax'], row['ymax'])
    if len(parametrs) > 0:

        canvas.create_line(parametrs[0], parametrs[1], parametrs[2], parametrs[3], fill='blue', width=1)
        if ((parametrs[2]-weight//2)**2+(parametrs[3]-height)**2)**0.5<k_cirle:
            canvas.create_text(800, 200, text=f'манип. {str(math.degrees(math.asin((parametrs[2]-parametrs[0])/((parametrs[2]-parametrs[0])**2+(height-parametrs[3])**2)**0.5)))}', fill='black',  font=('Purisa', 15))
            canvas.itemconfig(detect_rec, fill='green')
        a = math.degrees(math.asin((height-parametrs[3])/((parametrs[0]-parametrs[2])**2+(height-parametrs[3])**2)**0.5))-90
        if parametrs[2] <= parametrs[0]:
            a = abs(a)

        canvas.create_text(800, 300, text=f'{a}', font=('Purisa', 15))

    frame = np.squeeze(result.render())
    cv2.imshow('FRAME', frame)

    window.update()

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
window.mainloop()

