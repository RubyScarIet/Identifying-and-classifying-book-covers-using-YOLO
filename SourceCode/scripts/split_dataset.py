# -*- coding: utf-8 -*-
"""split_dataset.py

Tiện ích script để chuyển ngẫu nhiên một phần phần trăm các ảnh training (cùng file nhãn tương ứng)
được lưu trong ``dataset/images/train`` và ``dataset/labels/train`` sang thư mục ``val``.

Cách chạy (chạy trong thư mục gốc dự án):

```powershell
# Kích hoạt môi trường ảo trước
.\\yolo_env\\Scripts\\activate
python scripts\\split_dataset.py --ratio 0.30   # ví dụ: tách 30% dữ liệu
```

Script an toàn khi chạy nhiều lần – nó chỉ di chuyển các file còn ở thư mục ``train``.
"""

import os
import random
import shutil
from pathlib import Path
import argparse

# ---------------------------------------------------------------------------
# Cấu hình – chỉnh sửa nếu cấu trúc thư mục dự án của bạn khác
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]  # <project>/SourceCode
DATASET_ROOT = PROJECT_ROOT / "dataset"

# Thư mục ảnh training / validation
IMG_TRAIN_DIR = DATASET_ROOT / "images" / "train"
IMG_VAL_DIR = DATASET_ROOT / "images" / "val"

# Thư mục nhãn (YOLO: mỗi ảnh một file .txt)
LAB_TRAIN_DIR = DATASET_ROOT / "labels" / "train"
LAB_VAL_DIR = DATASET_ROOT / "labels" / "val"

# Tỷ lệ phần trăm dữ liệu training muốn chuyển sang validation (0 < SPLIT_RATIO < 1)
parser = argparse.ArgumentParser(description="Chia ngẫu nhiên dữ liệu training thành tập validation.")
parser.add_argument('--ratio', type=float, default=0.20,
                    help='Tỷ lệ dữ liệu chuyển sang validation, ví dụ: 0.20 cho 20%.')
args = parser.parse_args()
SPLIT_RATIO = args.ratio
# ---------------------------------------------------------------------------

def ensure_dirs():
    """Tạo các thư mục validation nếu chúng chưa tồn tại."""
    IMG_VAL_DIR.mkdir(parents=True, exist_ok=True)
    LAB_VAL_DIR.mkdir(parents=True, exist_ok=True)


def get_image_files():
    """Trả về danh sách tên file ảnh (có phần mở rộng) trong thư mục train.
    Chỉ xét các phần mở rộng ảnh thông thường.
    """
    extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}
    return [p.name for p in IMG_TRAIN_DIR.iterdir() if p.suffix.lower() in extensions]


def move_pair(img_name: str):
    """Di chuyển một ảnh và file nhãn tương ứng (nếu có) từ train sang val.
    ``img_name`` phải bao gồm phần mở rộng, ví dụ ``book_001.jpg``.
    """
    src_img = IMG_TRAIN_DIR / img_name
    dst_img = IMG_VAL_DIR / img_name
    shutil.move(str(src_img), str(dst_img))

    # File nhãn có cùng tên nhưng phần mở rộng .txt
    label_name = Path(img_name).stem + ".txt"
    src_label = LAB_TRAIN_DIR / label_name
    if src_label.is_file():
        dst_label = LAB_VAL_DIR / label_name
        shutil.move(str(src_label), str(dst_label))
    else:
        print(f"[WARN] Không tìm thấy file nhãn cho {img_name} – chỉ di chuyển ảnh.")


def main():
    ensure_dirs()
    images = get_image_files()
    total = len(images)
    if total == 0:
        print("[INFO] Không có ảnh training – không thực hiện chia.")
        return

    n_move = int(total * SPLIT_RATIO)
    if n_move == 0:
        print("[INFO] Tỷ lệ chia quá nhỏ cho kích thước dữ liệu hiện tại.")
        return

    # Chọn ngẫu nhiên các file cần di chuyển – ``random.sample`` đảm bảo không trùng lặp
    to_move = random.sample(images, n_move)
    print(f"[INFO] Đang di chuyển {n_move} / {total} ảnh ({SPLIT_RATIO*100:.0f}%%) sang tập validation.")
    for img in to_move:
        move_pair(img)

    # Tổng kết
    remaining = get_image_files()  # ảnh còn lại trong train
    print("[DONE] Hoàn thành chia dữ liệu.")
    print(f"  Ảnh còn lại trong train : {len(remaining)}")
    print(f"  Ảnh trong validation   : {n_move}")

if __name__ == "__main__":
    main()

