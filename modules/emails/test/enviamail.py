import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

smtp = smtplib.SMTP()
smtp.connect("192.9.201.5", 25)

msg = MIMEMultipart()
msg["Subject"] = "Energía San Juan S.A - Autogestión - Oficina Virtual"
msg["From"] = "ESJ Avisos <avisos@energiasanjuan.com.ar>"
msg["To"] = "bvargas@energiasanjuan.com.ar"

# Email body with embedded image
body = """
<html>
  <body>
    <p>Estimad@:</p>
    <p>Use el siguiente código de verificación para confirmar su casilla de email: 4505.</p>
    <p>Este es un paso importante del proceso de registración.</p>
    <p>Saludos Cordiales.</p>
    <p>Energía San Juan S.A.</p>
    <p><img src="cid:image"></p>
    <p>Por favor, NO responda a este mensaje, es un envío automático.</p>
  </body>
</html>
"""

msg.attach(MIMEText(body, "html"))

# Add an image attachment and set its content ID
with open("data/images/LogoWEBESJ.png", 'rb') as image_file:
    image = MIMEImage(image_file.read(), _subtype="png")
    image.add_header('Content-Disposition', 'attachment', filename="LogoWEBESJ.png")
    image.add_header('Content-ID', '<image>')
    msg.attach(image)

smtp.sendmail(msg["From"], msg["To"], msg.as_string())
smtp.close()
