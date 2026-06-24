# -*- coding: utf-8 -*-
"""train_and_show.py

Script tiện ích để **huấn luyện** mô hình YOLO (Ultralytics) và **hiển thị** kết quả huấn luyện.

- Hỗ trợ truyền các tham số qua dòng lệnh (đường dẫn dữ liệu, mô hình, epochs, batch, imgsize, …).
- Sau khi train, tự động chạy validation và lưu/hiển thị đồ thị loss & mAP.
- Kết quả (hình ảnh) được lưu trong thư mục `runs/train/<name>/` và `runs/val/<name>/`.

Cách dùng (chạy trong thư mục gốc dự án):

```powershell
# Kích hoạt môi trường ảo
.\\yolo_env\\Scripts\\activate

# Train với mô hình nano, 100 epochs, tỷ lệ train/val 80-20 (mặc định)
python scripts\\train_and_show.py --model yolov8n.yaml --epochs 100 --batch 16

# Train với mô hình medium và tỉ lệ 30% validation
python scripts\\train_and_show.py --model yolov8m.yaml --epochs 150 --batch 8 --ratio 0.30
```
"""

import argparse
import os
from pathlib import Path

# Thư viện Ultralytics YOLO (cần cài đặt qua pip install ultralytics)
from ultralytics import YOLO

try:
    import wandb
except ImportError:
    wandb = None


def parse_args():
    parser = argparse.ArgumentParser(description="Huấn luyện mô hình YOLO và hiển thị kết quả.")
    parser.add_argument("--data", type=str, default="data.yaml",
                        help="Đường dẫn tới file data.yaml mô tả dataset (mặc định: data.yaml trong thư mục gốc).")
    parser.add_argument("--model", type=str, default="yolov8n.yaml",
                        help="Mô hình tiền huấn luyện (yaml) của Ultralytics, ví dụ: yolov8n.yaml, yolov8s.yaml, …")
    parser.add_argument("--epochs", type=int, default=100,
                        help="Số epoch để train (mặc định 100).")
    parser.add_argument("--batch", type=int, default=16,
                        help="Kích thước batch (mặc định 16).")
    parser.add_argument("--imgsz", type=int, default=640,
                        help="Kích thước ảnh đầu vào (mặc định 640).")
    parser.add_argument("--ratio", type=float, default=0.20,
                        help="Tỷ lệ phần trăm dữ liệu training chuyển sang validation (0-1).")
    parser.add_argument("--name", type=str, default="yolo_train",
                        help="Tên thư mục lưu kết quả trong runs/train/.")
    parser.add_argument("--project", type=str, default="runs/train",
                        help="Thư mục gốc lưu các run train.")
    return parser.parse_args()


def split_dataset_if_needed(ratio: float, project_root: Path):
    """Nếu tỉ lệ validation không phải 0.20 (giá trị mặc định), chạy script split_dataset.py.
    Thư mục `scripts` được giả định nằm trong `project_root`.
    """
    if abs(ratio - 0.20) < 1e-6:
        return  # không cần thay đổi, đã là 20%
    split_script = project_root / "scripts" / "split_dataset.py"
    if not split_script.is_file():
        print(f"[WARN] Không tìm thấy {split_script} – bỏ qua việc chia lại dataset.")
        return
    cmd = f"python {split_script} --ratio {ratio}"
    print(f"[INFO] Chạy: {cmd}")
    os.system(cmd)


def main():
    args = parse_args()

    # Đường dẫn tới thư mục gốc dự án (SourceCode)
    project_root = Path(__file__).resolve().parents[1]  # <project>/SourceCode

    # Nếu người dùng muốn thay đổi tỉ lệ train/val thì gọi script split_dataset.py
    split_dataset_if_needed(args.ratio, project_root)

    # Đọc file data.yaml – nếu đường dẫn tương đối thì tính theo project_root
    data_path = Path(args.data)
    if not data_path.is_absolute():
        data_path = project_root / data_path
    if not data_path.is_file():
        raise FileNotFoundError(f"Không tìm thấy file dữ liệu {data_path}")

    # Khởi tạo mô hình YOLO từ file yaml (có thể là yolov8n.yaml, yolov8s.yaml, …)
    model_path = args.model
    if not Path(model_path).is_absolute():
        # Nếu người dùng truyền tên mô hình chuẩn của Ultralytics, không cần đường dẫn
        model = YOLO(model_path)  # Ultralytics sẽ tự tìm trong ~/.ultralytics/models
    else:
        model = YOLO(model_path)

    project_path = str(project_root / args.project)

    # Khởi tạo wandb nếu có
    if wandb is not None:
        try:
            wandb.init(project="yolo_book_covers", name=args.name, config=vars(args))
            print("[INFO] Đã khởi tạo Weights & Biases (wandb).")
        except Exception as e:
            print(f"[WARN] Không thể khởi tạo wandb: {e}")

    # Thực hiện train
    print("[INFO] Bắt đầu huấn luyện …")
    results = model.train(
        data=str(data_path),
        epochs=args.epochs,
        batch=args.batch,
        imgsz=args.imgsz,
        project=project_path,
        name=args.name,
        device=None,  # tự động chọn GPU nếu có
        save=True,   # lưu weights ở mỗi epoch
        
        # --- THÊM DATA AUGMENTATION CHO BÌA SÁCH ---
        degrees=15.0,      # Xoay ngẫu nhiên (tối đa 15 độ) vì sách có thể bị nằm nghiêng
        shear=5.0,         # Kéo xiên ảnh (mô phỏng góc chụp nghiêng của điện thoại)
        scale=0.5,         # Phóng to / thu nhỏ ảnh (+/- 50%)
        perspective=0.001, # Hiệu ứng phối cảnh 3D (rất quan trọng khi chụp sách thực tế)
        fliplr=0.0,        # KHÔNG lật ngang ảnh (Bìa sách có chữ, nếu lật ngược chữ model sẽ bị nhiễu)
        mosaic=1.0,        # Ghép 4 ảnh thành 1 (mặc định của YOLO, rất tốt)
        mixup=0.1          # Trộn ngẫu nhiên các ảnh với nhau (giảm overfitting hiệu quả)
    )

    # In tóm tắt kết quả cuối cùng
    print("\n--- HOÀN TẤT HUẤN LUYỆN ---")
    print(f"Model: {args.model}")
    print(f"Epochs: {args.epochs}")
    print(f"Kết quả train đã được lưu tại: {Path(args.project) / args.name}")
    print("Để đánh giá mô hình trên tập validation và xem các biểu đồ, hãy chạy script:")
    print("       python scripts\\show_results.py")
    
    print(f"\n[INFO] Để theo dõi bằng TensorBoard, hãy mở một terminal mới, kích hoạt môi trường và chạy:")
    print(f"       tensorboard --logdir=\"{Path(project_root) / args.project}\"")
    
    if wandb is not None:
        wandb.finish()

if __name__ == "__main__":
    main()
