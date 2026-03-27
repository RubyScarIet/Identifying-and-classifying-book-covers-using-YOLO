import cv2
from ultralytics import YOLO

model = YOLO('yolov8n.pt') 

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if success:
        results = model(frame, classes=[73], conf=0.5)

        annotated_frame = results[0].plot()

        cv2.imshow("YOLOv8 Real-time Book Detection", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()