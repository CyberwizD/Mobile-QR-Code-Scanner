import streamlit as st
from utils import qr_scanner

st.set_page_config(
    page_title="Mobile Authenticator", 
    page_icon=":chart_with_upwards_trend:", 
    layout="wide"
)

# st.logo(image="static/logo.png", size="small", link="https://github.com/CyberwizD/QR-Auth-System")

# Sidebar
st.sidebar.title("Mobile Authenticator")

# Streamlit UI
st.title("📷 Mobile QR Code Scanner")
st.write("Link your device by scanning the QR code to access your account.")

# Open mobile device camera
cam_btn = st.button("Open Camera")

if cam_btn:
    qr_scanner.qr_scanner()

    st.success("QR code scanned successfully!")