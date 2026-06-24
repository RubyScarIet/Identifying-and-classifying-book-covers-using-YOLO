import os
from PIL import Image
from pillow_heif import register_heif_opener

# Kích hoạt hỗ trợ HEIC/HEIF
register_heif_opener()

# ĐƯỜNG DẪN THƯ MỤC (Kiểm tra kỹ dấu r'...' và đường dẫn)
folder_path = r'C:\Users\tinca\OneDrive\Desktop\Identifying and classifying book covers using YOLO\SourceCode\dataset\images\train'
prefix = "book_"

def universal_convert(path):
    if not os.path.exists(path):
        print(f"❌ Thư mục không tồn tại: {path}")
        return

    # Lấy tất cả các file trong thư mục (không phân biệt đuôi)
    all_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    
    max_index = 0
    unrenamed_files = []
    
    for f in all_files:
        if f.startswith(prefix) and f.lower().endswith(".jpg"):
            try:
                num_str = f[len(prefix):-4]
                num = int(num_str)
                max_index = max(max_index, num)
            except ValueError:
                unrenamed_files.append(f)
        else:
            unrenamed_files.append(f)
            
    unrenamed_files.sort()

    if not unrenamed_files:
        print("✅ Tất cả các file đã được đổi tên và chuyển đổi.")
        return

    print(f"🚀 Tìm thấy {len(unrenamed_files)} file cần xử lý. Bắt đầu ép kiểu sang JPG (tiếp tục từ số {max_index + 1})...")

    success_count = 0
    current_index = max_index + 1
    
    for filename in unrenamed_files:
        old_path = os.path.join(path, filename)
        new_name = f"{prefix}{str(current_index).zfill(2)}.jpg"
        new_path = os.path.join(path, new_name)

        try:
            # Mở file bất kể đuôi là gì
            with Image.open(old_path) as img:
                # Chuyển sang RGB để loại bỏ kênh Alpha (nếu là PNG) hoặc hệ màu CMYK/P3
                rgb_img = img.convert('RGB')
                # Lưu đè thành file .jpg mới
                rgb_img.save(new_path, "JPEG", quality=95)
            
            if old_path.lower() != new_path.lower():
                os.remove(old_path)
                
            print(f"✅ Đã chuyển: {filename} -> {new_name}")
            success_count += 1
            current_index += 1
        except Exception as e:
            print(f"⚠️ Bỏ qua {filename}: Không phải định dạng ảnh hoặc lỗi ({e})")

    print(f"\n--- HOÀN THÀNH: Đã chuyển thành công {success_count}/{len(unrenamed_files)} file sang JPG ---")

if __name__ == "__main__":
    universal_convert(folder_path)