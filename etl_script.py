# -*- coding: utf-8 -*-

import psycopg2  # Cliente PostgreSQL
import requests  # Para solicitar la API
import datetime

# Configuración de la base de datos
try:
    conn = psycopg2.connect(
        host="postgres-service",
        database="mydatabase",
        user="myuser",
        password="mypassword",
        port= "5432",
        #options= "-c client_encoding=UTF8"
    )
    print("Conexión existosa")
except UnicodeDecodeError as e:
    print(f"UnicodeDecodeError: {e}")
except Exception as e:
    print(f"Ocurrió un error: {e}")

cursor = conn.cursor()

# Crear la tabla 'documentos' si no existe
cursor.execute("""
    CREATE TABLE IF NOT EXISTS documentos (
        pk_id SERIAL PRIMARY KEY,            -- Clave primaria auto-incremental
        api_id VARCHAR(255) UNIQUE NOT NULL, -- Almacena el 'id' del response, debe ser único
        fecha TIMESTAMP NOT NULL,
        nemo VARCHAR(255) NOT NULL,
        version VARCHAR(50)
    );
""")
# Configuración de parámetros para la API
fechadesde = "2024-10-01T00:00:00"
fechahasta = "2024-10-01T23:00:00"
nemo = "PARTE_POST_OPERATIVO"

# Construir la URL de la API con los parámetros
API_URL = f"https://api.cammesa.com/pub-svc/public/findDocumentosByNemoRango?fechadesde={fechadesde}&fechahasta={fechahasta}&nemo={nemo}"

# Hacer la solicitud a la API
response = requests.get(API_URL)

# Verificar que la solicitud fue exitosa
if response.status_code == 200:
    response_data = response.json()
    
    # Insertar datos en la tabla
    for item in response_data:
        api_id = item['id']  # Extraer el 'id' del API response
        fecha = datetime.datetime.strptime(item['fecha'], '%d/%m/%Y')  # Convertir fecha
        nemo = item['nemo']
        version = item['version']

        # Insertar en la base de datos
        cursor.execute("""
            INSERT INTO documentos (api_id, fecha, nemo, version)
            VALUES (%s, %s, %s, %s); 
        """, (api_id, fecha, nemo, version))
    
    # Confirmar los cambios y cerrar la conexión
    conn.commit()
    print("Datos insertados correctamente.")
    #print(f"{data}")
else:
    print(f"Error en la solicitud a la API: {response.status_code}")

# Cerrar la conexión con la base de datos
cursor.close()
conn.close()