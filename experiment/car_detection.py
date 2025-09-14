import cv2
import os
import shutil
from ultralytics import YOLO

# Load a pretrained YOLOv8/YOLO11 model
model = YOLO("yolo11m.pt")   # or "yolov8m.pt"

# Paths
source_folder = "dataset/чистота/грязныйдоп"
destination_folder = "dataset/чистота/yolo_dirt"

os.makedirs(destination_folder, exist_ok=True)

# Iterate over all files in the source folder
for filename in os.listdir(source_folder):
    if not filename.lower().endswith(('mpo', 'dng', 'bmp', 'tif', 'jpg', 'tiff', 'pfm', 'jpeg', 'heic', 'webp', 'png')):
        continue

    image_path = os.path.join(source_folder, filename)
    results = model(image_path)

    image = cv2.imread(image_path)
    h, w = image.shape[:2]

    best_box = None
    best_area = 0

    # Check detections
    for result in results:
        for box in result.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]

            if label == "car":
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                area = (x2 - x1) * (y2 - y1)

                if area > best_area:
                    best_area = area
                    best_box = (x1, y1, x2, y2)

    # If at least one car was detected → crop the biggest one
    if best_box is not None:
        x1, y1, x2, y2 = best_box
        # Ensure the crop is inside image bounds
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w - 1, x2), min(h - 1, y2)

        cropped = image[y1:y2, x1:x2]
        save_path = os.path.join(destination_folder, filename)
        cv2.imwrite(save_path, cropped)
        print(f"[OK] Car cropped → {save_path}")

    else:
        # No car detected → copy original image
        save_path = os.path.join(destination_folder, filename)
        shutil.copy(image_path, save_path)
        print(f"[NO CAR] Copied original → {save_path}")
