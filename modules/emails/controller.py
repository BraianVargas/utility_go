import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def envia_mail_codigo(destinatario, codigo):
    smtp = smtplib.SMTP()
    smtp.connect("192.9.201.5", 25)

    msg = MIMEMultipart()
    msg["Subject"] = "Energía San Juan S.A - Autogestión - Oficina Virtual"
    msg["From"] = "ESJ Avisos <avisos@energiasanjuan.com.ar>"
    msg["To"] = destinatario  # Use the provided recipient

    # Email body with embedded image as a footer and styles
    body = f"""
    <html style="width:350px;">
    <body>
        <p>Estimad@:</p>
        <p>Use el siguiente código de verificación para confirmar su cuenta:</p>
        <p style="font-size:46px; margin-left:8em; padding:2em;"><strong>{codigo}</strong></p>
        <p>Este es un paso importante del proceso de registración.</p>
        <p>Saludos Cordiales.</p>
        <img src="cid:image" style="width: 100px;">
    </body>
    <footer>
        <p style="font-size: 12px;">Por favor, NO responda a este mensaje, es un envío automático.</p>
    </footer>
    </html>
    """

    msg.attach(MIMEText(body, "html"))

    # Add an image attachment and set its content ID
    with open("data/images/LogoWEBESJ.png", 'rb') as image_file:
        image = MIMEImage(image_file.read(), _subtype="png")
        image.add_header('Content-Disposition', 'attachment', filename="LogoWEBESJ.png")
        image.add_header('Content-ID', '<image>')
        msg.attach(image)

    try:
        smtp.sendmail(msg["From"], destinatario, msg.as_string())  # Use the provided recipient
        smtp.close()
        return True
    except:
        return False
