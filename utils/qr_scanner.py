import streamlit as st
import streamlit.components.v1 as components

@st.cache_data
def qr_scanner():
  st.markdown("""
  > Open this app on your **phone browser** to scan QR codes using the phone camera.
  """)

  # HTML + JavaScript QR code scanner
  qr_code_scanner = """
  <script src="https://unpkg.com/html5-qrcode"></script>
  <div id="reader" width="600px"></div>
  <p id="result">Scanning...</p>
  <script>
  function onScanSuccess(decodedText, decodedResult) {
      const resultElem = window.parent.document.getElementById("qr-result");
      resultElem.innerText = decodedText;
  }

  const html5QrCode = new Html5Qrcode("reader");
  html5QrCode.start(
    { facingMode: "environment" },
    { fps: 10, qrbox: 250 },
    onScanSuccess
  );
  </script>
  """

  components.html(qr_code_scanner, height=500)

  # Display the scanned result in Streamlit
  st.markdown("### QR Result")

# qr_result = st.empty()
