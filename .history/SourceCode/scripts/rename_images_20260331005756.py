import os

# 1. Đường dẫn đến thư mục chứa ảnh của bạn
# Bạn hãy thay đổi đường dẫn này cho đúng với máy của mình
folder_path = r'C:\Users\tinca\OneDrive\Desktop\Identifying and classifying book covers using YOLO\SourceCode\dataset\images\train'

# 2. Tiền tố bạn muốn đặt cho ảnh (ví dụ: book_)
prefix = "book_"

def rename_images(path):
    # Lấy danh sách tất cả file trong thư mục
    files = [f for f in os.listdir(path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.jpe'))]
    
    # Sắp xếp để đổi tên theo thứ tự
    files.sort()

    print(f"Tìm thấy {len(files)} ảnh. Đang tiến hành đổi tên...")

    for index, filename in enumerate(files, start=1):
        # Lấy phần mở rộng của file (ví dụ: .jpg)
        extension = os.path.splitext(filename)[1]
        
        # Tạo tên mới dạng book_01.jpg (zfill(2) để có số 0 ở trước: 01, 02...)
        new_name = f"{prefix}{str(index).zfill(2)}{extension}"
        
        # Đường dẫn cũ và mới
        old_file = os.path.join(path, filename)
        new_file = os.path.join(path, new_name)

        try:
            os.rename(old_file, new_file)
            print(f"Đã đổi: {filename} -> {new_name}")
        except Exception as e:
            print(f"Lỗi khi đổi tên file {filename}: {e}")

    print("--- Hoàn thành đổi tên! ---")

if __name__ == "__main__":
    rename_images(folder_path)