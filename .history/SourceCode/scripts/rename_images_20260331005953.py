import os
from pillow_heif import register_heif_opener

# Kích hoạt bộ đọc file HEIC cho thư viện Pillow
register_heif_opener()

# ĐƯỜNG DẪN CỦA BẠN
folder_path = r'C:\Users\tinca\OneDrive\Desktop\Identifying and classifying book covers using YOLO\SourceCode\dataset\images\train'
prefix = "book_"

def rename_images(path):
    if not os.path.exists(path):
        print(f"❌ Không tìm thấy thư mục: {path}")
        return

    # Danh sách các đuôi file ảnh chấp nhận (Đã thêm .heic)
    valid_extensions = ('.jpg', '.jpeg', '.png', '.jpe', '.bmp', '.webp', '.heic', '.mov')
    
    # Lọc file
    files = [f for f in os.listdir(path) if f.lower().endswith(valid_extensions)]
    files.sort() 

    print(f"🚀 Tìm thấy {len(files)} ảnh (bao gồm HEIC). Đang xử lý...")

    count = 0
    for index, filename in enumerate(files, start=1):
        ext = os.path.splitext(filename)[1].lower()
        
        # Tạo tên mới
        new_name = f"{prefix}{str(index).zfill(2)}{ext}"
        
        old_file = os.path.join(path, filename)
        new_file = os.path.join(path, new_name)

        # Tránh ghi đè nếu file mới trùng tên file cũ
        if os.path.exists(new_file) and old_file != new_file:
            new_file = os.path.join(path, f"{prefix}{str(index).zfill(2)}_temp{ext}")

        try:
            os.rename(old_file, new_file)
            print(f"✅ {filename} -> {new_name}")
            count += 1
        except Exception as e:
            print(f"❌ Lỗi tại {filename}: {e}")

    print(f"\n--- THÀNH CÔNG: Đã đổi tên {count}/{len(files)} file ---")

if __name__ == "__main__":
    rename_images(folder_path)