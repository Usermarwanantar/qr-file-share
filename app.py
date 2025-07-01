import streamlit as st
import os
import qrcode
from io import BytesIO
import uuid

# Configuration de la page
st.set_page_config(page_title="Uploader & QR Code", layout="centered")

# Dossier d'upload (accessible publiquement)
UPLOAD_FOLDER = "static/uploaded"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# URL de base (à modifier si tu déploies sur Streamlit Cloud)
APP_BASE_URL = "http://localhost:8501"  # ⚠️ Remplace par ton URL réelle après déploiement

st.title("📁 Uploader un fichier et obtenir un QR Code")

# Étape 1 : Upload du fichier
uploaded_file = st.file_uploader("Sélectionnez un fichier", type=None)

if uploaded_file:
    # Générer un nom unique pour le fichier
    file_extension = os.path.splitext(uploaded_file.name)[1]
    unique_filename = f"{uuid.uuid4().hex}{file_extension}"
    save_path = os.path.join(UPLOAD_FOLDER, unique_filename)

    # Sauvegarde du fichier
    with open(save_path, "wb") as f:
        f.write(uploaded_file.read())

    # Construction de l'URL de téléchargement
    download_url = f"{APP_BASE_URL}/{save_path}"

    st.success("✅ Fichier uploadé avec succès !")
    st.markdown(f"[📥 Télécharger le fichier]({download_url})")

    # Génération du QR Code
    qr = qrcode.make(download_url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    st.image(buffer.getvalue(), caption="📱 Scannez ce QR Code", use_column_width=False)

    st.info("Partagez ce lien ou ce QR code pour que d'autres puissent télécharger le fichier.")
