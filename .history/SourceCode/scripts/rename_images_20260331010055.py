import os
from PIL import Image
from pillow_heif import register_heif_opener

# Kích hoạt bộ đọc file HEIC
register_heif_opener()

# ĐƯỜNG DẪN THƯ MỤC ẢNH CỦA BẠN
folder_path = r'C:\Users\tinca\OneDrive\Desktop\Identifying and classifying book covers using YOLO\SourceCode\dataset\images\train'
prefix = "book_"

def convert_and_rename(path):
    if not os.path.exists(path):
        print(f"❌ Không tìm thấy thư mục: {path}")
        return

    # Lấy tất cả file có đuôi ảnh, bao gồm cả HEIC
    valid_extensions = ('.heic', '.jpg', '.jpeg', '.png', '.jpe')
    files = [f for f in os.listdir(path) if f.lower().endswith(valid_extensions)]
    files.sort()

    print(f"🚀 Bắt đầu xử lý {len(files)} file...")

    for index, filename in enumerate(files, start=1):
        old_file_path = os.path.join(path, filename)
        new_name = f"{prefix}{str(index).zfill(2)}.jpg"
        new_file_path = os.path.join(path, new_name)

        try:
            with Image.open(old_file_path) as img:
                # Chuyển sang hệ màu RGB (HEIC thường dùng hệ màu khác)
                rgb_img = img.convert('RGB')
                # Lưu thành JPG chất lượng cao (95)
                rgb_img.save(new_file_path, "JPEG", quality=95)
            
            # Sau khi chuyển xong, nếu file cũ không phải là file mới thì xóa file cũ đi cho gọn
            if old_file_path.lower() != new_file_path.lower():
                os.remove(old_file_path)
                
            print(f"✅ Đã chuyển: {filename} -> {new_name}")
        except Exception as e:
            print(f"❌ Lỗi tại {filename}: {e}")


if __name__ == "__main__":
    convert_and_rename(folder_path)