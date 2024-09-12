import cv2
from ultralytics import YOLO
import time
import numpy as np

def findOrigin(frame):
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
        cv2.putText(frame, "ORIGIN [0,0]", (jFound -10 , iFound -10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        return [iFound, jFound]
    
    return None



# Loading of the model:
model_path = 'best.pt' #'C:/users/doyez/Downloads/best.pt'  
model = YOLO(model_path)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erreur: Impossible d'ouvrir la webcam")
    exit()

cv2.namedWindow('Webcam')

while True:
    ret, frame = cap.read()
    findOrigin(frame)
    if ret:            
        results = model.predict(frame, conf=0.5) 

        for result in results:
            boxes = result.boxes.xyxy.cpu().numpy()  # Coordinates
            confidences = result.boxes.conf.cpu().numpy()  # %
            class_ids = result.boxes.cls.cpu().numpy()  # ID
            
            # Draw the result:
            for box, confidence, class_id in zip(boxes, confidences, class_ids):
                x1, y1, x2, y2 = map(int, box)
                class_name = "BOX"  
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(frame, f'{class_name} {confidence:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
            # Show the image
            cv2.imshow('Webcam', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()