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
    
    

## Bloque de adición de registros y actualización
def mostrar_formulario_y_tabla():
    conn = sqlite3.connect('registroartroplastias.db', check_same_thread=False)
    c = conn.cursor()

    st.title("Registro zonal de Artroplastias - SOTOCAV")

    with st.form("form_artroplastia"):
        col1, col2 = st.columns(2)

        with col1:
            fecha = st.date_input("Fecha de la cirugía")
            lado = st.selectbox("Lado", ["Derecho", "Izquierdo"])
            articulacion = st.selectbox("Articulación", ["Cadera", "Rodilla", "Hombro", "Tobillo", "Otra"])
            tipo = st.selectbox("Tipo de artroplastia", ["Total", "Parcial", "Revisión"])

        with col2:
            diagnostico = st.text_input("Diagnóstico principal")
            implante = st.text_input("Implante (marca/modelo)")
            cirujano = st.text_input("Cirujano")
            centro = st.text_input("Centro")

        observaciones = st.text_area("Observaciones", height=100)

        submitted = st.form_submit_button("Guardar registro")

        if submitted:
            c.execute('''
                INSERT INTO registros (fecha, lado, articulacion, tipo, diagnostico, implante, cirujano, centro, observaciones)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (str(fecha), lado, articulacion, tipo, diagnostico, implante, cirujano, centro, observaciones))
            conn.commit()
            st.success("Registro guardado correctamente.")

            # Subir a Google Drive
            file.SetContentFile("registroartroplastias.db")
            file.Upload()
            st.info("Base de datos subida a Drive.")

    st.subheader("Registros existentes")
    df = pd.read_sql_query("SELECT * FROM registros", conn)
    conn.close()
    st.dataframe(df)



### Llamadas finales a funciones o bloques de código
mostrar_formulario_y_tabla()
