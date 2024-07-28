   
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_email(destinatario, asunto, cuerpo):
    remitente = "arielonnis@gmail.com"
    contraseña = "vdby oept wutr gjyd"  # Usa la contraseña de aplicación generada acá >> https://myaccount.google.com/apppasswords

    mensaje = MIMEMultipart()
    mensaje['From'] = remitente
    mensaje['To'] = destinatario
    mensaje['Subject'] = asunto
    mensaje.attach(MIMEText(cuerpo, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as servidor:
            servidor.starttls()
            servidor.login(remitente, contraseña)
            texto = mensaje.as_string()
            servidor.sendmail(remitente, destinatario, texto)
        print("Listo! email enviado papu!")
    except Exception as e:
        print(f"Error al enviar el email: {e}")

destinatario = "arielonnis@gmail.com"
asunto = "Prueba de email desde Python"
cuerpo = "Lorem Ipsum es simplemente el texto de relleno de las imprentas y archivos de texto. Lorem Ipsum ha sido el texto de relleno estándar de las industrias desde el año 1500, cuando un impresor (N. del T. persona que se dedica a la imprenta) desconocido usó una galería de textos y los mezcló de tal manera que logró hacer un libro de textos especimen. No sólo sobrevivió 500 años, sino que tambien ingresó como texto de relleno en documentos electrónicos, quedando esencialmente igual al original. Fue popularizado en los 60s con la creación de las hojas Letraset, las cuales contenian pasajes de Lorem Ipsum, y más recientemente con software de autoedición, como por ejemplo Aldus PageMaker, el cual incluye versiones de Lorem Ipsum."

enviar_email(destinatario, asunto, cuerpo)