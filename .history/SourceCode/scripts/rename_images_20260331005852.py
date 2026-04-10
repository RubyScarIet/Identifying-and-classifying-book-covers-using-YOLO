import os

# ĐƯỜNG DẪN CỦA BẠN (Kiểm tra kỹ xem có đúng folder chứa ảnh không)
folder_path = r'C:\Users\tinca\OneDrive\Desktop\Identifying and classifying book covers using YOLO\SourceCode\dataset\images\train'
prefix = "book_"

def rename_images(path):
    if not os.path.exists(path):
        print(f"❌ Lỗi: Thư mục không tồn tại tại: {path}")
        return

    # Lấy TẤT CẢ các file để kiểm tra
    all_items = os.listdir(path)
    print(f"Tổng số vật thể trong folder: {len(all_items)}")

    # Chỉ lọc ra các file ảnh (Thêm tất cả các đuôi có thể có)
    valid_extensions = ('.jpg', '.jpeg', '.png', '.jpe', '.bmp', '.webp')
    files = [f for f in all_items if f.lower().endswith(valid_extensions)]
    
    files.sort() # Sắp xếp theo tên để đổi cho đúng thứ tự
    print(f"Tìm thấy {len(files)} file ảnh hợp lệ để đổi tên.")

    count = 0
    for index, filename in enumerate(files, start=1):
        ext = os.path.splitext(filename)[1]
        new_name = f"{prefix}{str(index).zfill(2)}{ext}"
        
        old_file = os.path.join(path, filename)
        new_file = os.path.join(path, new_name)

        # Tránh trường hợp file mới trùng tên file cũ đang tồn tại
        if os.path.exists(new_file) and old_file != new_file:
            new_file = os.path.join(path, f"{prefix}{str(index).zfill(2)}_new{ext}")

        try:
            os.rename(old_file, new_file)
            print(f"✅ {filename} -> {new_name}")
            count += 1
        except Exception as e:
            print(f"❌ Lỗi file {filename}: {e}")

    print(f"\n--- ĐÃ HOÀN THÀNH: Đổi tên thành công {count}/{len(files)} ảnh ---")

if __name__ == "__main__":
    rename_images(folder_path)