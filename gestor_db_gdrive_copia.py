import streamlit as st
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials

# Crear credenciales directamente desde st.secrets
scope = ['https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    dict(st.secrets["gdrive"]),
    scopes=scope
)

# Autenticación
gauth = GoogleAuth()
gauth.credentials = credentials
drive = GoogleDrive(gauth)

# ID del archivo en Google Drive
file_id = "167aC7ay09TzSf_4POtio_k6BFChsRLhf"

# Descargar el archivo
file = drive.CreateFile({'id': file_id})
file.GetContentFile("registroartroplastias.db")

st.success("Base de datos descargada correctamente")
