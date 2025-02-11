import streamlit as st
import cv2
from pyzbar import pyzbar
import pyperclip
import time

def set_focus(camera, value):
    camera.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    camera.set(cv2.CAP_PROP_FOCUS, value)

def scan_barcode():
    # Change the camera index to use the front-facing camera
    front_camera_index = 0  # Adjust camera index based on your mobile device
    cap = cv2.VideoCapture(front_camera_index)

    if not cap.isOpened():
        st.error("Failed to open camera.")
        return

    # Set an initial focus value
    focus_value = 0.0
    set_focus(cap, focus_value)

    last_focus_change_time = time.time()

    while True:
        ret, frame = cap.read()

        if not ret:
            st.error("Failed to capture frame.")
            continue

        barcodes = pyzbar.decode(frame)

        for barcode in barcodes:
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            barcode_data = barcode.data.decode('utf-8')
            barcode_type = barcode.type
            text = f"{barcode_data} ({barcode_type})"
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            # Copy the barcode data to the clipboard
            pyperclip.copy(barcode_data)
            st.success(f"Detected Barcode: {barcode_data}")

        # Display the frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert colorspace for Streamlit
        st.image(frame, channels="RGB", use_column_width=True)

        # Check if it's time to change the focus
        if time.time() - last_focus_change_time > 3:
            focus_value = (focus_value + 0.5) % 1.0
            set_focus(cap, focus_value)
            last_focus_change_time = time.time()

def main():
    st.title("Mobile Barcode Scanner")
    st.markdown("Please ensure your device has a camera enabled.")

    scan_barcode()

if __name__ == "__main__":
    main()





































# # import streamlit as st
# # from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
# # import cv2
# # from pyzbar import pyzbar

# # class BarcodeScanner(VideoTransformerBase):
# #     def transform(self, frame):
# #         img = frame.to_ndarray(format="bgr24")

# #         # Detectar códigos de barras en la imagen
# #         barcodes = pyzbar.decode(img)
# #         for barcode in barcodes:
# #             x, y, w, h = barcode.rect
# #             # Dibujar un rectángulo alrededor del código de barras
# #             cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

# #             # Obtener los datos del código de barras
# #             barcode_data = barcode.data.decode('utf-8')
# #             barcode_type = barcode.type

# #             # Imprimir los datos del código de barras en la pantalla
# #             text = f"{barcode_data} ({barcode_type})"
# #             cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# #             # Mostrar los datos en Streamlit
# #             st.session_state["barcode"] = barcode_data

# #         return img

# # st.title("Barcode Scanner")

# # webrtc_ctx = webrtc_streamer(key="example", video_transformer_factory=BarcodeScanner)

# # if "barcode" in st.session_state:
# #     st.write(f"Detected Barcode : {st.session_state['barcode']}")

# # Import the required libraries
# import cv2
# import numpy as np
# from pyzbar.pyzbar import decode
# import streamlit as st

# # Initialize the camera
# cap = cv2.VideoCapture(0)

# if not cap.isOpened():
#     st.write("Error: No se pudo abrir la cámara.")
#     exit()

# while True:
#     # Capture a frame from the camera
#     ret, frame = cap.read()

#     if not ret:
#         st.write("Error: No se pudo capturar el fotograma.")
#         continue

#     # Convert the frame to grayscale
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # Decode barcodes from the grayscale frame
#     barcodes = decode(gray)

#     # Check if any barcode is detected
#     if barcodes:
#         # Extract the decoded data (assuming there's only one barcode in the frame)
#         barcode_data = barcodes[0].data.decode('utf-8')
#         st.write("Barcode Data:", barcode_data)
        
#         # Process the barcode data as needed
#         # Example: Display the barcode data on screen
#         cv2.putText(frame, "Barcode: " + barcode_data, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

#     # Display the frame
#     cv2.imshow('Barcode Scanner', frame)

#     # Check for the 'q' key to exit the loop
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release the camera and close the window
# cap.release()
# cv2.destroyAllWindows()
