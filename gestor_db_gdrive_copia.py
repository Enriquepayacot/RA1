import streamlit as st
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os
import json

# Guardar los secrets en un archivo temporal JSON
creds_path = "/tmp/creds.json"
with open(creds_path, "w") as f:
    json.dump(st.secrets["gdrive"], f)

# Autenticación
gauth = GoogleAuth()
gauth.LoadCredentialsFile(creds_path)
gauth.LocalWebserverAuth() if not gauth.access_token else None
gauth.ServiceAuth()
drive = GoogleDrive(gauth)

# ID del archivo (lo puedes obtener una vez desde el navegador)
file_id = "1FS7GuToutM42HiSiG2qsITAjnXsWkvnh"

# Descargar el archivo
file = drive.CreateFile({'id': file_id})
file.GetContentFile("registroartroplastias.db")

st.success("Base de datos descargada correctamente")

# (Opcional) Subir cambios de nuevo
# file.SetContentFile("registroartroplastias.db")
# file.Upload()
# st.success("Archivo actualizado en Google Drive")
