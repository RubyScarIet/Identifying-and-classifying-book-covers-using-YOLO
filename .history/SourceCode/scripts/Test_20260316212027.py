import os

path = "C:/Users/tinca/OneDrive/Desktop/Identifying and classifying book covers using YOLO/SourceCode/dataset"
if os.exists(path):
    print("✅ Đường dẫn chính xác!")
    print(f"Danh sách thư mục con: {os.listdir(path)}")
else:
    print("❌ Không tìm thấy đường dẫn. Hãy kiểm tra lại!")