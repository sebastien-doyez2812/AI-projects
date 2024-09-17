# -----------------------------------------------------------
# Script Name    : run.py
# Author         : Sébastien Doyez
# Creation Date  : 15/09/2024
# Version        : 1.0
# Description    : Python script containing a Machine Learning model, able
# to detect a box, calculate coordinates and send it to robot. 
#
# Copyright (c) 2024, Sébastien DOYEZ
# All rights reserved.
#
# License:
# This code is distributed under the MIT license.
# You are free to use, modify, and distribute it, provided that
# you keep this copyright notice. The software is provided "as is,"
# without any warranty of any kind.
# -----------------------------------------------------------

import cv2
from ultralytics import YOLO
import time
import numpy as np
import serial
import math as m

graduation = 29.8
port = 'COM5'
repere = [] #[[coord_orig], [y], [x]]
target = []
posAxeRobot = [-7, 14.8]
l0 = 15.5
l1 = 11.5
l2 = 17.5
correcteur_t1 = 15

def MGD(xr, yr):
    print("xr = ", xr)
    print("yr = ", yr)
    print("interieur acos= " , (xr**2 + yr**2 - (l1**2 + l2**2))/(2*l1*l2))
    theta2 = m.acos((xr*xr + yr*yr - (l1*l1 + l2*l2))/(2*l1*l2))
    theta1 = m.asin((yr*(l1+l2*m.cos(theta2)) - xr*l2*m.sin(theta2))/ (xr*xr + yr*yr))
    return(theta1, theta2)



def testRobotConnected(port_robot):
    try:
        ser = serial.Serial(port_robot, baudrate=9600, timeout=1)
        ser.close()
        print("Robot connected")
        return True
    except:
        print("Error: Robot not connected")
        return False


def calculAngle(pt):
    # Theta 1:
    theta1 = m.atan((pt[1]- posAxeRobot[1])/(pt[0]))
    (theta2, theta3) = MGD(m.sqrt((pt[0] + 7)**2 + (pt[1] - 14.8)**2), -16)#MGD(2-10.5, m.sqrt((pt[0] + 7)**2 + (pt[1] - 14.8)**2))
    
    # Theta 3:    
    return (theta1, theta2, theta3)

def calculCoordinates(xr, yr):
    Xd = graduation *(repere[0][0] - xr)/(repere[0][0] - repere[2][0]) #Xd = 29.8 * (Xr - X0)/ (X1 - X0)
    Yd = graduation *(repere[0][1] - yr)/(repere[0][1] - repere[1][1]) #Yd = 29.8 * (Yr - Y0)/ (Y1 - Y0)
    return [Xd, Yd]

def pixelCentral(pt1, pt2):
    Xc = int(pt1[0] + (pt2[0]- pt1[0])/2) # = X1 + (X2-X1) /2
    Yc = int(pt1[1] + (pt2[1]- pt1[1])/2) # = Y1 + (Y2-Y1) /2
    return (Xc, Yc)


def sendData(theta1, theta2, theta3):
    print("angle a envoyé:", theta1, theta2, theta3)
    list_data = str([theta1, theta2, theta3])+"\n"
    arduino.write(list_data.encode())
    arduino.write(b'\n')
    print("Donnée envoyé!")
    time.sleep(10)

def findOrigin(frame):
    # a verifier
    coordinates = []
    for i in range(frame.shape[0]):
        for j in range(frame.shape[1]):
            if frame[i, j, 2] > 90 and frame[i, j, 0] < 50 and frame[i, j, 1] < 50:
                coordinates.append([i, j])
    
    if len(coordinates) != 0: 
        coordinates = np.array(coordinates)
        
        min_i = np.min(coordinates[:, 0])
        max_i = np.max(coordinates[:, 0])
        min_j = np.min(coordinates[:, 1])
        max_j = np.max(coordinates[:, 1])
        
        iFound = int((min_i + max_i) / 2)
        jFound = int((min_j + max_j) / 2)
        cv2.circle(frame, (jFound, iFound), 5, (255, 0, 0), -1)
        cv2.putText(frame, "ORIGIN [0,0]", (jFound -50 , iFound +55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        return [iFound, jFound]
    
    return None


def click_event_calibration(event, x, y, flags, param):
    global repere
    if event == cv2.EVENT_LBUTTONDOWN:
        repere.append((x, y))

# Check if the robot is connected:
robotEnable = testRobotConnected(port)

if robotEnable :
    arduino = serial.Serial(port='COM5', baudrate= 9600, timeout= 1)
    # Loading of the model:
    model_path = 'C:/Users/doyez/Documents/AI-projects/DIY_Robotic_arm_and_AI/best.pt' 
    model = YOLO(model_path)

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Webcam not connect")
        exit()

    cv2.namedWindow('Webcam')

    cv2.setMouseCallback("Webcam", click_event_calibration)

    while True:
        ret, frame = cap.read()
        if ret and (len(repere) == 3 ):            
            results = model.predict(frame, conf=0.5) 
            
            # Draw the frame:
            cv2.circle(frame, (repere[0][0], repere[0][1]), 5, (0, 0, 255), -1)  # Dessiner un cercle rouge
            cv2.arrowedLine(frame, repere[0], repere[1], (255, 0, 0), 2)
            cv2.arrowedLine(frame, repere[0], repere[2], (255, 0, 0), 2)
            cv2.putText(frame, "ORIGIN [0,0]", (repere[0][0] -25 , repere[0][1] + 22), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
            
            for result in results:
                boxes = result.boxes.xyxy.cpu().numpy()  # Coordinates
                confidences = result.boxes.conf.cpu().numpy()  # %
                class_ids = result.boxes.cls.cpu().numpy()  # ID
                
                # Draw the result:
                for box, confidence, class_id in zip(boxes, confidences, class_ids):
                    x1, y1, x2, y2 = map(int, box)
                    class_name = "BOX"  
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv2.putText(frame, f'{class_name} {confidence*100:.2f}{"%"}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                    
                    # Calculate the central point:
                    [Xc, Yc]= pixelCentral([x1,y1], [x2,y2])
                    [Xd, Yd] = calculCoordinates(Xc, Yc)
                    cv2.putText(frame, f"({round(Xd, 1)}, {round(Yd, 1)})", (Xc- 30, Yc + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                    """
                    (theta1, theta2, theta3) = calculAngle((Xd,Yd))
                    theta1 = m.degrees(theta1) + 90 + correcteur_t1
                    theta2 = m.degrees(theta2) 
                    theta3 = m.degrees(theta3) +25
                    print(theta1, theta2, theta3)
                    sendData(theta1, theta2, theta3)
                    break
                    """
        # Show the image
        cv2.imshow('Webcam', frame)
        if cv2.waitKey(1) & 0xFF == ord('y'):
            (theta1, theta2, theta3) = calculAngle((Xd,Yd))
            theta1 = m.degrees(theta1) + 90 + correcteur_t1
            theta2 = m.degrees(theta2) 
            theta3 = m.degrees(theta3) +25
            print(theta1, theta2, theta3)
            sendData(theta1, theta2, theta3)
            break            
        """ans = input("Detection accurate? (Y/N)")
        if ans == "N" or ans == "n":
            break

        else:
            (theta1, theta2, theta3) = calculAngle((Xd,Yd))
            theta1 = m.degrees(theta1) + 90 + correcteur_t1
            theta2 = m.degrees(theta2) 
            theta3 = m.degrees(theta3) +25
            print(theta1, theta2, theta3)
            sendData(theta1, theta2, theta3)
            break            
        """
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()