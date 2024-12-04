# -*- coding: utf-8 -*-

import psycopg2  # Cliente PostgreSQL
import requests  # Para solicitar la API

# Configuración de la base de datos
conn = psycopg2.connect(
    host="postgres-service",
    database="mydatabase",
    user="myuser",
    password="mypassword",
    port= "5432",
    client_encoding="UTF8"
)

cursor = conn.cursor()

# Crear la tabla 'documentos' si no existe
cursor.execute("""
    CREATE TABLE IF NOT EXISTS documentos (
        id VARCHAR(255) NOT NULL,
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

print(response)

# Verificar que la solicitud fue exitosa
if response.status_code == 200:
    data = response.json()
    
    # Insertar datos en la tabla
    for item in data:
        cursor.execute("""
            INSERT INTO documentos (id, fecha, nemo, version)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """, (item['id'], item['fecha'], item['nemo'], item['version']))
    
    # Confirmar los cambios y cerrar la conexión
    conn.commit()
    print("Datos insertados correctamente.")
else:
    print(f"Error en la solicitud a la API: {response.status_code}")

# Cerrar la conexión con la base de datos
cursor.close()
conn.close()
