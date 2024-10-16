import cv2
import streamlit as st
import numpy as np
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer

# Judul aplikasi
st.title("Program Deteksi Warna Real-Time")

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

# Class untuk memproses frame video secara real-time
class ColorDetection(VideoTransformerBase):
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")

        # Konversi frame dari BGR ke HSV
        hsv_frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        height, width, _ = img.shape

        # Koordinat tengah frame
        cx = int(width / 2)
        cy = int(height / 2)

        # Mengambil nilai warna piksel di tengah frame
        pixel_center = hsv_frame[cy, cx]
        hue = pixel_center[0]
        saturation = pixel_center[1]
        value = pixel_center[2]

        # Deteksi warna berdasarkan HSV
        color = detect_color(hue, saturation, value)

        # Mendapatkan nilai BGR untuk menampilkan teks dan lingkaran
        pixel_center_bgr = img[cy, cx]
        b, g, r = int(pixel_center_bgr[0]), int(pixel_center_bgr[1]), int(pixel_center_bgr[2])

        # Tambahkan teks warna dan lingkaran di tengah frame
        cv2.putText(img, color, (cx - 100, cy - 150), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (b, g, r), 8)
        cv2.circle(img, (cx, cy), 10, (b, g, r), 5)

        return img

# Komponen WebRTC untuk streaming video
webrtc_streamer(key="example", video_transformer_factory=ColorDetection)
