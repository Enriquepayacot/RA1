import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import sqlite3
import pandas as pd
import time

###################### AUTENTICACION #######################################
# Configuración de usuarios y contraseñas
config = {
    'credentials': {
        'usernames': {
            'admin': {
                'name': 'Administrador',
                'password': stauth.Hasher(['admin123']).generate()[0]
            },
            'usuario1': {
                'name': 'Usuario Uno',
                'password': stauth.Hasher(['clave123']).generate()[0]
            }
        }
    },
    'cookie': {
        'name': 'registro_artro_cookie',
        'key': 'clave_secreta_super_segura',  # cámbiala por una propia
        'expiry_days': 1
    },
    'preauthorized': {
        'emails': []
    }
}

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Login
nombre, autenticado, usuario = authenticator.login('Iniciar sesión', 'main')


if autenticado:
    try:
        authenticator.logout('Cerrar sesión', 'sidebar')
    except KeyError:
        pass

    st.sidebar.write(f"👤 Bienvenido, {nombre}")

    st.title("Registro de Artroplastias - SOTOCAV")

    # Clave única para evitar duplicación de formularios
    unique_key = f"form_artroplastia_{int(time.time())}"

    with st.form(key=unique_key):
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
            conn = sqlite3.connect('artroplastias.db', check_same_thread=False)
            c = conn.cursor()
            c.execute('''
                INSERT INTO registros (fecha, lado, articulacion, tipo, diagnostico, implante, cirujano, centro, observaciones)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (str(fecha), lado, articulacion, tipo, diagnostico, implante, cirujano, centro, observaciones))
            conn.commit()
            conn.close()
            st.success("Registro guardado correctamente.")

    st.subheader("Registros existentes")
    conn = sqlite3.connect('artroplastias.db', check_same_thread=False)
    df = pd.read_sql_query("SELECT * FROM registros", conn)
    conn.close()
    st.dataframe(df)

else:
    st.error("Por favor, introduce un usuario y contraseña válidos")


#########################  HASTA AQUÍ LA AUTENTICACIÓN #######################################
#####################################################################################################    



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
