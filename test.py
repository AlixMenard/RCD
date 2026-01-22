from torch.xpu import device
from ultralytics import YOLO
import cv2
import numpy as np

model = YOLO('runs/segment/yolo11m/weights/best.pt')

image1 = cv2.imread('data/pictures/cube1.jpg')

res1 = model.predict(image1,
                     agnostic_nms=True, classes=[0,3,4,5,6,7])[0]

if res1.masks is not None:
    # Get class names dictionary from the model
    names = model.names

    for mask, box in zip(res1.masks.xy, res1.boxes):
        # 1. Get the class name
        class_id = int(box.cls[0])
        class_name = names[class_id]

        # 2. Draw the mask (polygon)
        points = np.array(mask, dtype=np.int32)
        cv2.polylines(image1, [points], isClosed=True, color=(0, 255, 0), thickness=2)

        # 3. Get coordinates for the label (top-left of bounding box)
        xmax, ymax, xmini, ymini = np.max(points[:,0]), np.max(points[:,1]), np.min(points[:,0]), np.min(points[:,1])
        x, y = (xmax+xmini)//2, (ymax+ymini)//2
        cv2.putText(image1, class_name, (int(x-20), int(y+5)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

# Show the result
cv2.imshow('YOLOv8 Segmentations', image1)
cv2.imwrite('result.jpeg', image1)
cv2.waitKey(0)
cv2.destroyAllWindows()