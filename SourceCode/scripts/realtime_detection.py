# -*- coding: utf-8 -*-
"""realtime_detection.py

Giao diện đơn giản cho phát hiện đối tượng thời gian thực sử dụng mô hình YOLOv8 đã được huấn luyện.

- Tải checkpoint tốt nhất từ quá trình huấn luyện (`runs/train/yolo_train/weights/best.pt`).
- Ghi hình từ webcam mặc định (chỉ mục 0).
- Thực hiện suy luận trên mỗi khung hình và vẽ các bounding box.
- Hiển thị kết quả trong cửa sổ OpenCV (`YOLO Real‑time Detection`).
- Nhấn **q** để thoát.

Script này nhẹ, chỉ yêu cầu các thư viện `opencv‑python` và `ultralytics` đã có trong môi trường dự án.
"""

import argparse
import sys
from pathlib import Path

import cv2
from ultralytics import YOLO


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Real‑time YOLO detection from webcam.")
    parser.add_argument(
        "--model",
        type=str,
        default="runs/train/yolo_train/weights/best.pt",
        help="Path to the YOLO weight file (default: best checkpoint from training).",
    )
    parser.add_argument(
        "--camera",
        type=str,
        default="0",
        help="Webcam index (0, 1) or IP stream URL (http://...).",
    )
    parser.add_argument(
        "--size",
        type=int,
        default=640,
        help="Resize width for inference (height is computed to keep aspect ratio).",
    )
    parser.add_argument(
        "--conf",
        type=float,
        default=0.25,
        help="Confidence threshold for detection (default: 0.25). Lower it to see more objects.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # Xác định đường dẫn mô hình – cho phép đường tương đối từ thư mục gốc dự án hoặc đường tuyệt đối.
    model_path = Path(args.model)
    # Xác định thư mục gốc của dự án (SourceCode) – vì thư mục runs đã được di chuyển vào đây
    project_root = Path(__file__).resolve().parents[1]
    if not model_path.is_absolute():
        model_path = project_root / model_path
    if not model_path.is_file():
        sys.exit(f"[ERROR] Model file not found: {model_path}")

    # Tải mô hình YOLO
    model = YOLO(str(model_path))

    # Xử lý input camera
    cam_source = args.camera
    if cam_source.isdigit():
        cam_source = int(cam_source)

    # Mở webcam (Dùng DSHOW cho Windows để hỗ trợ Virtual Camera qua cáp Type-C tốt hơn)
    if isinstance(cam_source, int):
        cap = cv2.VideoCapture(cam_source, cv2.CAP_DSHOW)
        if not cap.isOpened():
            cap = cv2.VideoCapture(cam_source)
    else:
        cap = cv2.VideoCapture(cam_source)

    if not cap.isOpened():
        sys.exit(f"[ERROR] Cannot open webcam. Check the camera index or device drivers for: {cam_source}")

    print("[INFO] Press 'q' in the video window to quit.")

    window_name = "YOLO Real-time Detection"
    # Thiết lập cửa sổ có thể thay đổi kích thước
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[WARN] Frame capture failed, stopping.")
            break

        # Thay đổi kích thước ảnh để tăng tốc suy luận đồng thời giữ tỷ lệ khung hình
        height = int(frame.shape[0] * args.size / frame.shape[1])
        resized = cv2.resize(frame, (args.size, height))

        # Thực hiện suy luận – kết quả là danh sách, lấy phần tử đầu tiên, áp dụng ngưỡng tin cậy
        results = model(resized, conf=args.conf)
        # `plot()` trả về ảnh đã vẽ các bounding box
        annotated = results[0].plot()

        cv2.imshow(window_name, annotated)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
