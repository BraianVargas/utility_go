import os
import base64
import requests
from datetime import datetime

BASE_PATH = "https://www.energiasanjuan.com.ar/"

def descargar_archivo(url, nombre_archivo):
    response = requests.get(url)
    if response.status_code == 200:
        with open(nombre_archivo, 'wb') as archivo:
            archivo.write(response.content)
        print(f"Archivo descargado como {nombre_archivo}")
    else:
        print(f"No se pudo descargar el archivo. Código de estado: {response.status_code}")


def pdf_to_base64(pdf_path):
    final_url = BASE_PATH + pdf_path
    print(final_url)
    response = requests.get(final_url)
    if response.status_code == 200:
        with open(response, "rb") as pdf_file:
            print("open")
            # Lee el contenido del archivo PDF
            pdf_content = pdf_file.read()
            # Convierte el contenido a base64
            pdf_base64_code = base64.b64encode(pdf_content).decode("utf-8")
    return pdf_base64_code

# base_path="\\192.9.202.6\home\samba\produccion\web_esj"
# # base_path="www.energiasanjuan.comn.ar"
# pdf_path = "/facturas/t1/7465_20231219/133469866.pdf"
# response_path = pdf_path.split('/')

# pdf_path = os.path.join(base_path,*response_path)

# pdf_path="https://www.energiasanjuan.com.ar/facturas/t1/7465_20231219/133469866.pdf"

# print(pdf_path)
# input()


# filename = str(f"temp.pdf")
# descargar_archivo(pdf_path, filename)

# res = pdf_to_base64('temp.pdf')
# print(res)