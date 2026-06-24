"""
fix_orientation.py
------------------
Tự động xoay lại ảnh bị sai chiều dựa vào metadata EXIF của điện thoại.
Xử lý toàn bộ ảnh trong thư mục dataset/images/train/
"""

import os
from PIL import Image, ExifTags

# ==== CẤU HÌNH ====
folder_path = os.path.join(
    os.path.dirname(__file__),
    "..", "dataset", "images", "train"
)
# ==================

def get_exif_orientation(img):
    """Đọc giá trị Orientation từ EXIF."""
    try:
        exif = img._getexif()
        if exif is None:
            return None
        for tag, value in exif.items():
            if ExifTags.TAGS.get(tag) == "Orientation":
                return value
    except Exception:
        return None
    return None

def fix_orientation(img):
    """Xoay ảnh về đúng chiều dựa theo EXIF Orientation."""
    orientation = get_exif_orientation(img)

    rotation_map = {
        3: 180,
        6: 270,
        8: 90,
    }
    flip_map = {
        2: Image.FLIP_LEFT_RIGHT,
        4: Image.FLIP_TOP_BOTTOM,
        5: Image.FLIP_LEFT_RIGHT,
        7: Image.FLIP_LEFT_RIGHT,
    }
    rotate_after_flip = {
        5: 90,
        7: 270,
    }

    if orientation in rotation_map:
        img = img.rotate(rotation_map[orientation], expand=True)
    elif orientation in flip_map:
        img = img.transpose(flip_map[orientation])
        if orientation in rotate_after_flip:
            img = img.rotate(rotate_after_flip[orientation], expand=True)

    return img

def process_folder(folder):
    files = [f for f in os.listdir(folder) if f.lower().endswith('.jpg')]
    fixed = 0
    skipped = 0

    print(f"🔍 Tìm thấy {len(files)} file JPG. Bắt đầu kiểm tra orientation...\n")

    for filename in sorted(files):
        filepath = os.path.join(folder, filename)
        try:
            with Image.open(filepath) as img:
                orientation = get_exif_orientation(img)
                if orientation in (3, 6, 8, 2, 4, 5, 7):
                    fixed_img = fix_orientation(img.copy())
                    # Lưu lại, xóa EXIF để tránh bị xoay lại lần sau
                    fixed_img.save(filepath, "JPEG", quality=95)
                    print(f"✅ Đã sửa ({orientation}→1): {filename}")
                    fixed += 1
                else:
                    skipped += 1
        except Exception as e:
            print(f"⚠️  Bỏ qua {filename}: {e}")

    print(f"\n--- HOÀN THÀNH: Đã sửa {fixed} ảnh, {skipped} ảnh không cần sửa ---")

if __name__ == "__main__":
    process_folder(folder_path)
