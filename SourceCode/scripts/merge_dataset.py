# -*- coding: utf-8 -*-
"""merge_dataset.py

Tiện ích script để gộp tất cả các ảnh và nhãn từ tập ``val`` ngược về tập ``train``.
Sau khi chạy script này, bạn có thể gán nhãn thêm các ảnh mới vào tập ``train``
và sau đó sử dụng lại script ``split_dataset.py`` để chia lại tập validation.

Cách chạy (chạy trong thư mục gốc dự án):

```powershell
# Kích hoạt môi trường ảo trước
.\yolo_env\Scripts\activate
python scripts\merge_dataset.py
```
"""

import os
import shutil
from pathlib import Path

# ---------------------------------------------------------------------------
# Cấu hình – chỉnh sửa nếu cấu trúc thư mục dự án của bạn khác
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]  # <project>/SourceCode
DATASET_ROOT = PROJECT_ROOT / "dataset"

# Thư mục ảnh training / validation
IMG_TRAIN_DIR = DATASET_ROOT / "images" / "train"
IMG_VAL_DIR = DATASET_ROOT / "images" / "val"

# Thư mục nhãn
LAB_TRAIN_DIR = DATASET_ROOT / "labels" / "train"
LAB_VAL_DIR = DATASET_ROOT / "labels" / "val"

# ---------------------------------------------------------------------------

def move_files(src_dir: Path, dst_dir: Path):
    """Di chuyển toàn bộ file từ src_dir sang dst_dir."""
    if not src_dir.exists():
        print(f"[INFO] Thư mục {src_dir} không tồn tại, bỏ qua.")
        return 0
        
    count = 0
    for p in src_dir.iterdir():
        if p.is_file():
            shutil.move(str(p), str(dst_dir / p.name))
            count += 1
    return count

def main():
    # Đảm bảo thư mục đích tồn tại
    IMG_TRAIN_DIR.mkdir(parents=True, exist_ok=True)
    LAB_TRAIN_DIR.mkdir(parents=True, exist_ok=True)
    
    print("[INFO] Đang chuyển ảnh từ val về train...")
    img_count = move_files(IMG_VAL_DIR, IMG_TRAIN_DIR)
    
    print("[INFO] Đang chuyển nhãn từ val về train...")
    lab_count = move_files(LAB_VAL_DIR, LAB_TRAIN_DIR)
    
    print(f"[DONE] Đã di chuyển {img_count} ảnh và {lab_count} file nhãn từ val về train.")
    print("Bạn có thể bắt đầu gán nhãn thêm dữ liệu mới vào thư mục dataset/images/train.")
    print("Sau khi gán nhãn xong, hãy dùng lệnh: python scripts\\split_dataset.py để chia lại tập train/val.")

if __name__ == "__main__":
    main()
