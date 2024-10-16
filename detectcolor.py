import streamlit as st
import cv2
import numpy as np
from PIL import Image

# Judul aplikasi
st.title("Program Deteksi Warna")

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

# Mengambil input kamera dari browser
camera_input = st.camera_input("Aktifkan kamera")

if camera_input:
    # Baca gambar dari kamera
    img_pil = Image.open(camera_input)
    frame = np.array(img_pil)

    # Konversi frame dari BGR ke HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
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

    # Mendapatkan nilai RGB untuk menampilkan lingkaran dan teks warna
    pixel_center_rgb = frame[cy, cx]
    r, g, b = int(pixel_center_rgb[0]), int(pixel_center_rgb[1]), int(pixel_center_rgb[2])

    # Tambahkan teks warna dan lingkaran di tengah frame
    cv2.putText(frame, color, (cx - 100, cy - 150), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (r, g, b), 8)
    cv2.circle(frame, (cx, cy), 10, (r, g, b), 5)

    # Tampilkan video di Streamlit
    st.image(frame, caption="Deteksi Warna Video", use_column_width=True)
