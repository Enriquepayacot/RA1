import streamlit as st
import sqlite3
import pandas as pd

# Conexión a la base de datos local
conn = sqlite3.connect('artroplastias.db', check_same_thread=False)
c = conn.cursor()

st.title("Registro zonal de Artroplastias - VERSION EN PRUEBAS")

# Formulario
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

# Mostrar registros
st.subheader("Registros existentes")
df = pd.read_sql_query("SELECT * FROM registros", conn)
st.dataframe(df)
