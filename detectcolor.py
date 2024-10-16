import cv2
import streamlit as st
import numpy as np

# Judul aplikasi
st.title("Program Pengenalan Warna")

# Menyiapkan kamera
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Mengambil gambar dalam loop
start = st.button('Start Webcam', key='start_button')

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

# Mengaktifkan webcam saat tombol ditekan
if start:
    frame_placeholder = st.empty()  # Tempat untuk menampilkan frame

    # Tombol stop diletakkan di luar loop agar tidak duplikat
    stop = st.button('Stop Webcam', key='stop_button')  

    while not stop:  # Looping selama tombol stop belum ditekan
        ret, frame = cam.read()  # `ret` akan bernilai True jika frame berhasil dibaca

        if not ret:
            st.write("Gagal mengambil gambar dari kamera.")
            break  # Berhenti jika tidak bisa membaca frame

        # Konversi frame dari BGR ke HSV
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        height, width, _ = frame.shape

        # Koordinat tengah frame
        cx = int(width / 2)
        cy = int(height / 2)

        # Mengambil nilai warna piksel di tengah frame
        pixel_center = hsv_frame[cy, cx]
        hue = pixel_center[0]
        saturation = pixel_center[1]
        value = pixel_center[2]

        # Deteksi warna
        color = detect_color(hue, saturation, value)

        # Mendapatkan nilai BGR untuk teks dan lingkaran
        pixel_center_bgr = frame[cy, cx]
        b, g, r = int(pixel_center_bgr[0]), int(pixel_center_bgr[1]), int(pixel_center_bgr[2])

        # Tambahkan teks warna dan lingkaran di tengah frame
        cv2.putText(frame, color, (cx - 100, cy - 150), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (b, g, r), 8)
        cv2.circle(frame, (cx, cy), 10, (b, g, r), 5)

        # Konversi frame dari BGR ke RGB untuk ditampilkan di Streamlit
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Perbarui gambar pada setiap frame
        frame_placeholder.image(frame_rgb, caption="Program Pengenalan Warna", use_column_width=True)

        # Perbarui status tombol stop tanpa menduplikasinya
        stop = st.session_state.get('stop_button', False)

    # Lepas kamera setelah selesai
    cam.release()
