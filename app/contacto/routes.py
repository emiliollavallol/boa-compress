from flask import request, render_template, redirect
from . import contacto_bp
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()
@contacto_bp.route('/', methods=['GET'])
def mostrar_formulario():
    return render_template("contacto.html")

@contacto_bp.route('/enviar-contacto', methods=['POST'])
def enviar_contacto():
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    mensaje = request.form.get('mensaje')

    # Configuración
    remitente = os.getenv("EMAIL_REMITENTE")
    contrasena = os.getenv("EMAIL_CONTRASENA")
    destinatario = os.getenv("EMAIL_DESTINATARIO")

    asunto = f"Consulta de {nombre}"
    cuerpo = f"Nombre: {nombre}\nEmail: {email}\n\nMensaje:\n{mensaje}"

    msg = EmailMessage()
    msg.set_content(cuerpo)
    msg['Subject'] = asunto
    msg['From'] = remitente
    msg['To'] = destinatario

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(remitente, contrasena)
            smtp.send_message(msg)
        return render_template("contacto_exito.html")
    except Exception as e:
        print("Error al enviar el correo:", e)
        return render_template("contacto_error.html")
