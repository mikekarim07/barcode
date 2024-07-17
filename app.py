# import streamlit as st
# from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
# import cv2
# from pyzbar import pyzbar

# class BarcodeScanner(VideoTransformerBase):
#     def transform(self, frame):
#         img = frame.to_ndarray(format="bgr24")

#         # Detectar códigos de barras en la imagen
#         barcodes = pyzbar.decode(img)
#         for barcode in barcodes:
#             x, y, w, h = barcode.rect
#             # Dibujar un rectángulo alrededor del código de barras
#             cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

#             # Obtener los datos del código de barras
#             barcode_data = barcode.data.decode('utf-8')
#             barcode_type = barcode.type

#             # Imprimir los datos del código de barras en la pantalla
#             text = f"{barcode_data} ({barcode_type})"
#             cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

#             # Mostrar los datos en Streamlit
#             st.session_state["barcode"] = barcode_data

#         return img

# st.title("Barcode Scanner")

# webrtc_ctx = webrtc_streamer(key="example", video_transformer_factory=BarcodeScanner)

# if "barcode" in st.session_state:
#     st.write(f"Detected Barcode : {st.session_state['barcode']}")

# Import the required libraries
import cv2
import numpy as np
from pyzbar.pyzbar import decode

# Initialize the camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: No se pudo abrir la cámara.")
    exit()

while True:
    # Capture a frame from the camera
    ret, frame = cap.read()

    if not ret:
        print("Error: No se pudo capturar el fotograma.")
        continue

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Decode barcodes from the grayscale frame
    barcodes = decode(gray)

    # Check if any barcode is detected
    if barcodes:
        # Extract the decoded data (assuming there's only one barcode in the frame)
        barcode_data = barcodes[0].data.decode('utf-8')
        st.write("Barcode Data:", barcode_data)
        
        # Process the barcode data as needed
        # Example: Display the barcode data on screen
        cv2.putText(frame, "Barcode: " + barcode_data, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Barcode Scanner', frame)

    # Check for the 'q' key to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
