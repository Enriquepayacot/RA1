import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import sqlite3
import pandas as pd
import time
import smtplib
from email.message import EmailMessage



def enviar_base_de_datos_por_email():
    remitente = "registroartroplastias@gmail.com"
    contraseña = "elmhpfaxqarkbudg"  # contraseña de aplicación, sin espacios
    destinatario = "registroartroplastias2@gmail.com"

    asunto = "Copia actualizada de artroplastias.db"
    cuerpo = "Se adjunta la última versión de la base de datos después de añadir un nuevo registro."

    msg = EmailMessage()
    msg["From"] = remitente
    msg["To"] = destinatario
    msg["Subject"] = asunto
    msg.set_content(cuerpo)

    with open("artroplastias.db", "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="octet-stream",
            filename="artroplastias.db"
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(remitente, contraseña)
        smtp.send_message(msg)



# -------------------- FUNCIÓN PRINCIPAL --------------------

def mostrar_formulario_y_tabla():
    conn = sqlite3.connect('artroplastias.db', check_same_thread=False)
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
            enviar_base_de_datos_por_email()  # ← Esta línea

    st.subheader("Registros existentes")
    df = pd.read_sql_query("SELECT * FROM registros", conn)
    conn.close()
    st.dataframe(df)


# -------------------- AUTENTICACIÓN --------------------

config = {
    'credentials': {
        'usernames': {
            'admin': {
                'name': 'Administrador',
                'password': '$2b$12$P1n.Mf1biv.t5cBHUtXYNum7bvUkGWjKKyy6km2BweZ03QmPGsosC'
            },
            'usuario1': {
                'name': 'Usuario Uno',
                'password': '$2b$12$DRDKiYlpYG9q4mJWadeHU.dm107Wuap2KCk6LxLQTQ27afOn63j1m'
            }
        }
    },
    'cookie': {
        'name': 'registro_artro_cookie',
        'key': 'clave_secreta_super_segura',
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

nombre, autenticado, usuario = authenticator.login('Iniciar sesión', 'main')

if autenticado:
    try:
        authenticator.logout('Cerrar sesión', 'sidebar')
    except KeyError:
        pass

    st.sidebar.write(f"👤 Bienvenido, {nombre}")
    mostrar_formulario_y_tabla()

else:
    st.error("Por favor, introduce un usuario y contraseña válidos")
