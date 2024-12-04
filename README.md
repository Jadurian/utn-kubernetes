UTN FRBA 

CURSO DOCKER Y KUBERNETES

Profesor: Marcos Tonina

Actividad integradora Kubernetes

Descripción:

Profesor Marcos disculpas por no poder haber entregado algo que funcione, espero poder realizarlo en el transcurso de la semana.
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

Deployment: para la ejecución de la imagen construida en Docker a partir del script de python

Statefulset: para la persistencia de los datos en la bd de postgres

Service: entiendo que es la que permite la comunicación entre los pods de manera interna en el clúster más allá que puse None como valor al mismo


Primer paso: desarrollar el código en Python

Segundo paso: buildear la imagen a partir del código

docker buildx build -t etl-cammesa:latest .

Tercer paso: buildear los objetos de kubernetes

Kubectl apply -f postgres-statefulset.yaml

Kubectl apply -f postgres-service.yaml

Kubectl apply -f etl-deployment.yaml

Cuando realizo un “k get all” me retorna que existe un error en el pod que debería correr el código, pero tanto el servicio y el statefulset parecieran estar bien ya que puedo entrar al pod donde vive el postgres.

Si realizo un k describe al pod del código figura:

    State:          Waiting
      Reason:       CrashLoopBackOff
    Last State:     Terminated
      Reason:       Error

Y si realizo un “k logs” al pod, arroja:

<Response [200]>
Traceback (most recent call last):
  File "/app/etl_script.py", line 46, in <module>
    cursor.execute("""
psycopg2.errors.InvalidColumnReference: there is no unique or exclusion constraint matching the ON CONFLICT specification

