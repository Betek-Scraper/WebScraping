import os
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

# Configura tu cuenta de correo desde las variables de entorno
GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")
EMAIL_ADDRESS1 = os.getenv("EMAIL_ADDRESS1")

# Función para enviar un correo
def enviar_correo(destinatario, asunto, mensaje):
    msg = MIMEMultipart()
    msg['From'] = GMAIL_ADDRESS
    msg['To'] = destinatario
    msg['Subject'] = asunto
    msg.attach(MIMEText(mensaje, 'plain'))

    try:
        # Conectar al servidor SMTP de Gmail con SSL
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_ADDRESS, GMAIL_PASSWORD)
            server.sendmail(GMAIL_ADDRESS, destinatario, msg.as_string())
            print(f'Correo enviado a {destinatario}.')
    except Exception as e:
        print(f'Error al enviar correo: {e}')

# Función para enviar correos a todos los candidatos
def enviar_emails():
    # Verificar si el archivo de coincidencias existe
    if not os.path.exists('Mejores_Coincidencias_Ingles_Ajustado.xlsx'):
        raise FileNotFoundError("El archivo 'Mejores_Coincidencias_Ingles_Ajustado.xlsx' no se encuentra. Asegúrate de que se haya generado.")

    # Cargar el archivo de coincidencias
    best_matches_df = pd.read_excel('Mejores_Coincidencias_Ingles_Ajustado.xlsx')

    # Enviar correos a cada candidato
    for _, row in best_matches_df.iterrows():
        nombre_candidato = row['Candidate']
        # correo_candidato = row['Candidate Email']  # Cambiar a la dirección real del candidato en producción
        correo_candidato = EMAIL_ADDRESS1
        titulo_vacante = row['Best Matched Job Title']
        descripcion_vacante = row['Job Description']
        link_postulacion = row['Apply Link']

        # Crear el mensaje de correo
        mensaje = f"""Hola {nombre_candidato},

Hemos encontrado una vacante que podría interesarte.

Título del puesto: {titulo_vacante}
Descripción: {descripcion_vacante}
Link para aplicar: {link_postulacion}

¡Buena suerte!
"""
        # Enviar el correo
        enviar_correo(correo_candidato, "Oportunidad de empleo que podría interesarte", mensaje)

    print("Correos enviados exitosamente.")
