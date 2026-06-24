# -*- coding: utf-8 -*-
"""show_results.py

Script để chạy validation và hiển thị kết quả (metric, đồ thị) từ một mô hình YOLO đã được huấn luyện.

Cách dùng (chạy trong thư mục gốc dự án):

```powershell
# Kích hoạt môi trường ảo
.\yolo_env\Scripts\activate

# Chạy validation với mô hình mặc định (thường là file best.pt sau khi train)
python scripts\show_results.py

# Hoặc chỉ định rõ đường dẫn weights và thư mục lưu kết quả
python scripts\show_results.py --weights runs\train\yolo_train\weights\best.pt --data data.yaml --name yolo_val
```
"""

import argparse
from pathlib import Path
from ultralytics import YOLO

def parse_args():
    parser = argparse.ArgumentParser(description="Đánh giá mô hình YOLO và hiển thị kết quả.")
    parser.add_argument("--weights", type=str, default="runs/train/yolo_train/weights/best.pt",
                        help="Đường dẫn tới file weights đã train (mặc định: runs/train/yolo_train/weights/best.pt).")
    parser.add_argument("--data", type=str, default="data.yaml",
                        help="Đường dẫn tới file data.yaml mô tả dataset (mặc định: data.yaml trong thư mục gốc).")
    parser.add_argument("--project", type=str, default="runs/val",
                        help="Thư mục gốc lưu các run validation.")
    parser.add_argument("--name", type=str, default="yolo_val",
                        help="Tên thư mục lưu kết quả trong runs/val/.")
    return parser.parse_args()

def main():
    args = parse_args()
    project_root = Path(__file__).resolve().parents[1]

    weights_path = Path(args.weights)
    if not weights_path.is_absolute():
        weights_path = project_root / weights_path
    if not weights_path.is_file():
        print(f"[LỖI] Không tìm thấy file weights tại: {weights_path}")
        print("Hãy đảm bảo bạn đã train xong và đường dẫn file .pt là chính xác.")
        return

    data_path = Path(args.data)
    if not data_path.is_absolute():
        data_path = project_root / data_path
    if not data_path.is_file():
        print(f"[LỖI] Không tìm thấy file dữ liệu: {data_path}")
        return

    # Khởi tạo mô hình YOLO với weights đã train
    print(f"[INFO] Tải mô hình từ {weights_path}...")
    model = YOLO(str(weights_path))

    project_path = str(project_root / args.project)

    # Chạy validation
    print("[INFO] Bắt đầu đánh giá (validation) trên tập val...")
    val_results = model.val(data=str(data_path), project=project_path, name=args.name)

    # In tóm tắt kết quả
    print("\n--- TÓM TẮT KẾT QUẢ VALIDATION ---")
    if hasattr(val_results, "results_dict"):
        metric = val_results.results_dict
        mAP50 = metric.get('metrics/mAP50(B)', 0)
        mAP50_95 = metric.get('metrics/mAP50-95(B)', 0)
        precision = metric.get('metrics/precision(B)', 0)
        recall = metric.get('metrics/recall(B)', 0)
        
        print(f"mAP@0.5: {mAP50:.4f}")
        print(f"mAP@0.5:0.95: {mAP50_95:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
    else:
        print("Không thể trích xuất metric tự động.")

    print("\nKết quả validation (ảnh, đồ thị, ma trận nhầm lẫn...) đã được lưu tại:")
    val_dir = Path(project_path) / args.name
    print(f"  {val_dir}")
    print("Bạn có thể mở các file PNG (như confusion_matrix.png, val_batch0_pred.jpg) trong thư mục này để xem chi tiết.")

if __name__ == "__main__":
    main()
