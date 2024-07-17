import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import cv2
from pyzbar import pyzbar

class BarcodeScanner(VideoTransformerBase):
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")

        # Detectar códigos de barras en la imagen
        barcodes = pyzbar.decode(img)
        for barcode in barcodes:
            x, y, w, h = barcode.rect
            # Dibujar un rectángulo alrededor del código de barras
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Obtener los datos del código de barras
            barcode_data = barcode.data.decode('utf-8')
            barcode_type = barcode.type

            # Imprimir los datos del código de barras en la pantalla
            text = f"{barcode_data} ({barcode_type})"
            cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Mostrar los datos en Streamlit
            st.session_state["barcode"] = barcode_data

        return img

st.title("Barcode Scanner")

webrtc_ctx = webrtc_streamer(key="example", video_transformer_factory=BarcodeScanner)

if "barcode" in st.session_state:
    st.write(f"Detected Barcode : {st.session_state['barcode']}")

