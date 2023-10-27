import pyodbc
from data.env_data import *

def connectSybase():
     conn = pyodbc.connect(
          'Driver={Adaptive Server Enterprise};'
          f'Server={server_host};'
          f'Port={server_port};'
          f'Database={server_db};'
          f'UID={server_user};'
          f'PWD={server_passwd};'
          'Mars_Connection=Yes;'
          'TDS_Version=8.0'
     )
     return conn
