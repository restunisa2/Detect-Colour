import cv2
import streamlit as st
import numpy as np

# Judul aplikasi
st.title("Program Pengenalan Warna")

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

# Input dari kamera
camera_input = st.camera_input("Ambil Gambar")

if camera_input:
    # Baca gambar dari input
    image = cv2.imdecode(np.frombuffer(camera_input.read(), np.uint8), 1)

    # Konversi gambar dari BGR ke HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    height, width, _ = image.shape

    # Koordinat tengah gambar
    cx = int(width / 2)
    cy = int(height / 2)

    # Mengambil nilai warna piksel di tengah gambar
    pixel_center = hsv_image[cy, cx]
    hue = pixel_center[0]
    saturation = pixel_center[1]
    value = pixel_center[2]

    # Deteksi warna
    color = detect_color(hue, saturation, value)

    # Mendapatkan nilai BGR untuk teks dan lingkaran
    pixel_center_bgr = image[cy, cx]
    b, g, r = int(pixel_center_bgr[0]), int(pixel_center_bgr[1]), int(pixel_center_bgr[2])

    # Tambahkan teks warna dan lingkaran di tengah gambar
    cv2.putText(image, color, (cx - 100, cy - 150), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (b, g, r), 8)
    cv2.circle(image, (cx, cy), 10, (b, g, r), 5)

    # Konversi gambar dari BGR ke RGB untuk ditampilkan di Streamlit
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Tampilkan gambar dan warna yang terdeteksi
    st.image(image_rgb, caption="Gambar dari Kamera", use_column_width=True)
    st.write(f"Warna terdeteksi: {color}")
