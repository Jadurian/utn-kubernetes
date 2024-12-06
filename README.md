UTN FRBA 

CURSO DOCKER Y KUBERNETES

Profesor: Marcos Tonina

Actividad integradora Kubernetes v2

Descripción:

En un proyecto que se me ocurrió para mi trabajo, necesito requestear de la API de CAMMESA (Compañía Administradora del Mercado Eléctrico Mayorista de Argentina) apuntando a endpoints específico que retornan json con datos de informes, como este estilo:

{
    "id": "8654F8401BA8D96E03258BAA007D9AC1",
    "fecha": "01/10/2024",
    "nemo": "PARTE_POST_OPERATIVO",
    "titulo": "Parte control post-operativo",
    "comentario": "2",
    "hora": "19:51",
    "adjuntos": [
      {
        "id": "PO241001.zip",
        "campo": "$FILE",
        "nombre": "PO241001-(02/10/2024 19:51:56 ZW3).zip"
      }
    ],
    "version": "2024-10-02T19:51:00.000-03:00"
  }

No voy a entrar en detalles, pero necesito escribir en tablas algunas values de las keys del json.

Tecnologías:

Postgres como motor de bases de datos

Python para el desarrollo del ETL

Docker Desktop para correr el clúster on premise

Objetos kubernetes:

Job: para la ejecución de la imagen construida en Docker a partir del script de python

Statefulset: para la persistencia de los datos en la bd de postgres

Service: entiendo que es la que permite la comunicación entre los pods de manera interna en el clúster más allá que puse None como valor al mismo

Primer paso: desarrollar el código en Python

Segundo paso: buildear la imagen a partir del código

docker buildx build -t etl-cammesa:latest .

Tercer paso: buildear los objetos de kubernetes

Kubectl apply -f postgres-statefulset.yaml

Kubectl apply -f postgres-service.yaml

Kubectl apply -f etl-job.yaml