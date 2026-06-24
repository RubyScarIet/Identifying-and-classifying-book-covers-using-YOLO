import streamlit as st
import cv2
import numpy as np
from pathlib import Path
from ultralytics import YOLO
from PIL import Image
import os

st.set_page_config(page_title="YOLO Book-Cover Detector",
                   layout="centered",
                   initial_sidebar_state="expanded")

st.markdown(
    """
    <style>
    .main {background-color: #1e1e2f; color:#e0e0e0;}
    .stButton>button{background:#4c6ef5;color:white;border-radius:8px;height:45px;}
    .stFileUploader>div{border:2px dashed #4c6ef5;border-radius:8px;}
    .stSidebar{background:#2b2b3a;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("YOLO Real-time Book-Cover Detector")
st.caption("Nhận diện bìa sách ngay trong trình duyệt - không cần cài phần mềm rời")

@st.cache_resource
def load_yolo(model_path: str) -> YOLO:
    if not Path(model_path).exists():
        st.warning(
            f"Không tìm thấy mô hình tại `{model_path}`. "
            "Sẽ tự động tải mô hình pre-trained `yolov8n.pt` để demo."
        )
        return YOLO("yolov8n.pt")
    return YOLO(str(model_path))

st.sidebar.header("Cài đặt mô hình")
default_path = "runs/train/yolo_train2/weights/best.pt"

model_path_input = st.sidebar.text_input(
    "Đường dẫn tới file .pt (tùy chọn)",
    value=default_path,
    help="Nhập đường tương đối hoặc tuyệt đối. Nếu để trống sẽ dùng pre-trained model.",
)

uploaded_pt = st.sidebar.file_uploader(
    "Hoặc kéo thả file mô hình .pt ở đây",
    type=["pt"]
)

if uploaded_pt is not None:
    tmp_path = Path("temp_uploaded_model.pt")
    tmp_path.write_bytes(uploaded_pt.getbuffer())
    model_path = str(tmp_path)
else:
    model_path = model_path_input.strip() or default_path

yolo_model = load_yolo(model_path)

source = st.radio(
    "Chọn nguồn ảnh:",
    ("Tải ảnh lên", "Dùng Camera"),
    index=0,
    help="Bạn có thể tải ảnh tĩnh hoặc chụp nhanh qua webcam."
)

if source == "Tải ảnh lên":
    uploaded_file = st.file_uploader(
        "Chọn file ảnh (JPG/PNG)", type=["jpg", "jpeg", "png"]
    )
    if uploaded_file:
        pil_img = Image.open(uploaded_file).convert("RGB")
        img_np = np.array(pil_img)[:, :, ::-1]
        results = yolo_model(img_np, conf=0.25)
        annotated = results[0].plot()
        st.subheader("Kết quả phát hiện")
        st.image(annotated, channels="BGR")
elif source == "Dùng Camera":
    cam_image = st.camera_input("Nhấn để chụp ảnh từ webcam")
    if cam_image:
        pil_img = Image.open(cam_image).convert("RGB")
        img_np = np.array(pil_img)[:, :, ::-1]
        results = yolo_model(img_np, conf=0.25)
        annotated = results[0].plot()
        st.subheader("Kết quả phát hiện")
        st.image(annotated, channels="BGR")

if "results" in locals():
    num_boxes = len(results[0].boxes)
    st.success(f"Đã phát hiện **{num_boxes}** đối tượng.")
    speed = results[0].speed.get("inference")
    if speed:
        st.info(f"Thời gian inference: **{speed:.2f} ms**")
