from torchvision import transforms
from PIL import Image
import torch
from torchvision import models
import torch.nn as nn
from ultralytics import YOLO
import cv2
import os
import shutil
import numpy as np

def isdent(img):
    # Preprocessing pipeline
    preprocess = transforms.Compose([
        transforms.Resize((260, 260)),  
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])

    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

    # Rebuild classifier
    model = models.efficientnet_b2(pretrained=False)
    in_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(in_features, 2)

    # Load weights
    state_dict = torch.load("efficientnet_b2_denty.pth", map_location=device)
    model.load_state_dict(state_dict)
    model.to(device)
    model.eval()

    # Load YOLO
    model_yolo = YOLO("yolo11m.pt")

    if isinstance(img, Image.Image):  # PIL
        w, h = img.size
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)  # convert PIL→OpenCV
    else:  # already NumPy (OpenCV)
        h, w = img.shape[:2]



    results = model_yolo(img)

    best_box, best_area = None, 0

    # Get biggest car detection
    for result in results:
        for box in result.boxes:
            cls_id = int(box.cls[0])
            label = result.names[cls_id]

            if label == "car":
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                area = (x2 - x1) * (y2 - y1)

                if area > best_area:
                    best_area = area
                    best_box = (x1, y1, x2, y2)

    # Crop if car found
    if best_box:
        x1, y1, x2, y2 = best_box
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w - 1, x2), min(h - 1, y2)
        img = img[y1:y2, x1:x2]
    else:
        return {"error": "[NO CAR]"}

    # Convert to PIL for transforms
    # Convert to PIL for transforms
    img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    # Split into 4 equal parts (2×2 grid)
    w, h = img.size
    regions = [
        img.crop((0, 0, w//2, h//2)),       # top-left
        img.crop((w//2, 0, w, h//2)),       # top-right
        img.crop((0, h//2, w//2, h)),       # bottom-left
        img.crop((w//2, h//2, w, h)),       # bottom-right
    ]

    class_names = ["clean", "dusty"]
    is_dusty = False
    results = []

    for region in regions:
        input_tensor = preprocess(region).unsqueeze(0).to(device)

        with torch.no_grad():
            outputs = model(input_tensor)
            probs = torch.softmax(outputs, dim=1)
            pred_class = torch.argmax(probs, dim=1).item()

        conf = probs[0][pred_class].item()
        results.append((class_names[pred_class], conf))

        if class_names[pred_class] == "dusty":
            is_dusty = True

    # Best region (highest confidence)
    best_class, best_conf = max(results, key=lambda x: x[1])

    # Final decision
    if is_dusty:
        return {"is_dent": "dent", "is_dent_score": best_conf}
    else:
        return {"is_dent": "no dent", "is_dent_score": best_conf}
    # f"Prediction: no dent (confidence: {best_conf:.2f}) (from regions: {results})"
