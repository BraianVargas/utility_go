import pyodbc
from data.env_data import *


def connectSybase():
    conn = pyodbc.connect(
        'Driver={Adaptive Server Enterprise};'
        f'Server={SERVER_HOST};'
        f'Port={SERVER_PORT};'
        f'Database={SERVER_DATABASE};'
        f'UID={SERVER_USER};'
        f'PWD={SERVER_PASSWORD};'
        'Mars_Connection=Yes;'
        'TDS_Version=8.0'
    )
    return conn
