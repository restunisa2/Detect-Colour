import cv2
import streamlit as st
import numpy as np

# Judul aplikasi
st.title("Program Deteksi Warna pada Video")

# Fungsi untuk mendeteksi warna
def detect_color(hue, saturation, value):
    if saturation < 3:
        return "PUTIH"
    elif value < 50:
        return "HITAM"
    elif 3 < saturation < 40:
        return "ABU-ABU"
    elif hue < 5:
        return "MERAH"
    elif hue < 20:
        return "ORANGE"
    elif hue < 30:
        return "KUNING"
    elif hue < 70:
        return "HIJAU"
    elif hue < 125:
        return "BIRU"
    elif hue < 145:
        return "UNGU"
    elif hue < 170:
        return "PINK"
    else:
        return "MERAH"

# Mengaktifkan webcam
cam = cv2.VideoCapture(0)

# Atur resolusi kamera
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Memulai streaming video
start = st.button('Mulai Video', key='start_video')
frame_placeholder = st.empty()  # Placeholder untuk video

# Tombol untuk menghentikan video
stop = False

if start:
    while not stop:
        ret, frame = cam.read()  # Membaca frame dari kamera
        if not ret:
            st.write("Tidak dapat mengakses kamera.")
            break
        
        # Konversi frame dari BGR ke HSV
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        height, width, _ = frame.shape

        # Mengambil warna piksel di tengah frame
        cx = int(width / 2)
        cy = int(height / 2)
        pixel_center = hsv_frame[cy, cx]
        hue = pixel_center[0]
        saturation = pixel_center[1]
        value = pixel_center[2]

        # Deteksi warna
        color = detect_color(hue, saturation, value)

        # Tampilkan deteksi warna pada video
        pixel_center_bgr = frame[cy, cx]
        b, g, r = int(pixel_center_bgr[0]), int(pixel_center_bgr[1]), int(pixel_center_bgr[2])
        cv2.putText(frame, color, (cx - 100, cy - 150), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (b, g, r), 8)
        cv2.circle(frame, (cx, cy), 10, (b, g, r), 5)

        # Konversi frame ke RGB untuk ditampilkan di Streamlit
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Tampilkan video dalam Streamlit
        frame_placeholder.image(frame_rgb, caption="Streaming Video", use_column_width=True)

        # Cek apakah pengguna menekan tombol "Hentikan Video"
        stop = st.button('Hentikan Video', key='stop_video')

# Setelah berhenti, lepas kamera
cam.release()


