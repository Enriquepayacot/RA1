#### Bloque de conexión al archivo en Google Drive

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

# Autenticación en Google Drive
gauth = GoogleAuth()
gauth.credentials = credentials
drive = GoogleDrive(gauth)

# ID del archivo en Google Drive
file_id = "167aC7ay09TzSf_4POtio_k6BFChsRLhf"

# Descargar el archivo
file = drive.CreateFile({'id': file_id})
file.GetContentFile("registroartroplastias.db")

st.success("Base de datos descargada correctamente")



### Bloque de gestión de la base de datos

import sqlite3
import pandas as pd

# Conectar a la base de datos SQLite
conn = sqlite3.connect("registroartroplastias.db")

# Leer el nombre de todas las tablas
tablas = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
st.subheader("Tablas en la base de datos:")
st.dataframe(tablas)

# Leer y mostrar la primera tabla (ajusta el nombre si es necesario)
nombre_tabla = tablas.iloc[0, 0] if not tablas.empty else None

if nombre_tabla:
    st.subheader(f"Contenido de la tabla '{nombre_tabla}':")
    df = pd.read_sql(f"SELECT * FROM {nombre_tabla};", conn)
    st.dataframe(df)
else:
    st.warning("No se encontraron tablas en la base de datos.")
