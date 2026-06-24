import os

path = "dataset"

if os.path.exists(path):
    print("Đường dẫn chính xác!")
    print(f"Danh sách thư mục con: {os.listdir(path)}")
else:
    print("Không tìm thấy đường dẫn. Hãy kiểm tra lại!")