"""
Author: Sebastien Doyez

Use: test a model for clothes recognition.
"""

import torch
import torch.nn as nn
import cv2
import numpy as np

# Model architecture:
class LeNet5(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        self.layer1 = nn.Sequential(nn.Conv2d(1, 6, kernel_size=5, stride=1, padding=0),
                                     nn.BatchNorm2d(6),
                                     nn.ReLU(),
                                     nn.MaxPool2d(kernel_size=2, stride=2))
        self.layer2 = nn.Sequential(nn.Conv2d(6, 16, kernel_size=5, stride=1, padding=0),
                                     nn.BatchNorm2d(16),
                                     nn.ReLU(),
                                     nn.MaxPool2d(kernel_size=2, stride=2))
        self.fc = nn.Linear(400, 120)  # 400 = 16 * 5 * 5
        self.relu = nn.ReLU()
        self.fc1 = nn.Linear(120, 84)
        self.relu1 = nn.ReLU()
        self.fc2 = nn.Linear(84, num_classes)

    def forward(self, x):
        out = self.layer1(x)
        out = self.layer2(out)
        out = out.reshape(out.size(0), -1)
        out = self.fc(out)
        out = self.relu(out)
        out = self.fc1(out)
        out = self.relu1(out)
        return self.fc2(out)

labels_map={
    0: 'T-shirt',
    1: 'Trouser',
    2: 'Pullover',
    3: 'Dress',
    4: 'Coat',
    5: 'Sandal',
    6: 'Shirt',
    7: 'Sneaker',
    8: 'Bag',
    9: 'Ankle Boot',
}
# Load the model
model_path = "C:/Users/doyez/Downloads/model.pth"
model = LeNet5(num_classes=10) 
model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
model.eval() 

# For the test, we will use a webcam:
cap = cv2.VideoCapture(0)  
while True:
    ret, frame = cap.read()
    if not ret:
        print("Erreur lors de la capture vidéo")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    resized = cv2.resize(gray, (32, 32))
    tensor = torch.tensor(resized, dtype=torch.float32).unsqueeze(0).unsqueeze(0) / 255.0 

    # Prediction:
    with torch.no_grad():
        output = model(tensor)
        pred = torch.argmax(output).item() 

    prediction = labels_map.get(pred)
    cv2.putText(frame, f"Prediction: {prediction}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Webcam Feed", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
