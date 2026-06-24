# Identifying and Classifying Book Covers using YOLO

## 1. Giới thiệu dự án (Project Introduction)
Dự án **"Identifying and Classifying Book Covers using YOLO"** được phát triển nhằm mục đích nhận diện và phân loại bìa sách một cách tự động và chính xác sử dụng mô hình phát hiện đối tượng YOLOv8. 
Ứng dụng có thể hỗ trợ hiệu quả trong việc quản lý thư viện, số hóa tài liệu và nhận diện thông tin sách theo thời gian thực thông qua camera hoặc ảnh chụp tĩnh.

Dự án tích hợp một giao diện trực quan được xây dựng bằng **Streamlit**, cho phép người dùng dễ dàng tương tác, tải lên ảnh hoặc sử dụng webcam để kiểm tra mô hình nhận diện ngay trên trình duyệt mà không cần cài đặt thêm phần mềm phức tạp.

## 2. Hướng dẫn cài đặt và chạy chương trình (Installation and Execution)

### Yêu cầu hệ thống
- Python 3.8+ (Khuyến nghị dùng Python 3.10 hoặc 3.11)
- Trình quản lý gói `pip`

### Các bước cài đặt

**Bước 1: Di chuyển vào thư mục mã nguồn của dự án**
Mở terminal (hoặc Command Prompt) và đi đến thư mục `SourceCode`:
```bash
cd "Identifying and classifying book covers using YOLO/SourceCode"
```

**Bước 2: (Khuyến nghị) Tạo và kích hoạt môi trường ảo (Virtual Environment)**
```bash
python -m venv yolo_env
# Trên Windows:
yolo_env\Scripts\activate
# Trên macOS/Linux:
source yolo_env/bin/activate
```

**Bước 3: Cài đặt các thư viện phụ thuộc**
Sử dụng file `requirements.txt` để cài đặt đầy đủ các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

### Hướng dẫn chạy chương trình

**⚠️ Lưu ý quan trọng:** Tất cả các lệnh dưới đây bắt buộc phải được chạy từ bên trong thư mục `SourceCode` để các đường dẫn tương đối hoạt động chính xác.

Dự án cung cấp 2 cách thức chính để trải nghiệm mô hình nhận diện:

**Cách 1: Chạy giao diện Web trực quan (Phù hợp với kiểm tra ảnh tĩnh và mô hình)**
Đây là giao diện thân thiện trên trình duyệt, cho phép người dùng dễ dàng tải ảnh hoặc đổi mô hình.
1. Tại terminal (đang ở thư mục `SourceCode`), chạy lệnh:
   ```bash
   streamlit run scripts/app_streamlit.py
   ```
2. Trình duyệt sẽ tự động mở tại `http://localhost:8501`.
3. Bạn có thể chọn **Tải ảnh lên** hoặc **Chụp ảnh qua Camera** để mô hình phân tích. 
*(Lưu ý: Giao diện web chụp từng ảnh tĩnh, không stream video liên tục).*

**Cách 2: Chạy nhận diện Real-time (Luồng video trực tiếp cực mượt)**
Cách này sử dụng trực tiếp OpenCV để bật cửa sổ phần mềm, quét và nhận diện liên tục không có độ trễ.
1. Tại terminal, chạy lệnh:
   ```bash
   python scripts/realtime_detection.py
   ```
2. Một cửa sổ phần mềm "YOLO Real-time Detection" sẽ hiện lên. 
3. Đưa bìa sách qua lại trước camera để thấy các khung nhận diện di chuyển liên tục.
4. Nhấn phím **`q`** trên bàn phím để tắt.

**Kiểm tra & Nâng cao:**
- **Kiểm tra đường dẫn dữ liệu:** Chạy lệnh `python scripts/Test.py`.
- **Huấn luyện mô hình mới:** Chạy lệnh `python scripts/train_and_show.py`.
- **Xử lý dữ liệu:** Sử dụng các file `split_dataset.py`, `merge_dataset.py`, `rename_images.py` trong thư mục `scripts/`.