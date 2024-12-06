# UTN FRBA 

# CURSO DOCKER Y KUBERNETES

## Profesor: Marcos Tonina

## Actividad integradora Kubernetes v2 

# UPDATE correción:

Logré mejorar el código para que funcione la imagen buildeada del script de python. Además reemplacé el Deployment por un Job, dado que con el Deployment el pod que corre el código insertaba la data pero al terminar su ejecución creaba otro pod para repetir el proceso y obviamente tiraba un error. Con un Job de única ejecución esto no sucede.

## Descripción:

En un proyecto que se me ocurrió para mi trabajo, necesito requestear de la API de CAMMESA (Compañía Administradora del Mercado Eléctrico Mayorista de Argentina) apuntando a endpoints específico que retornan json con datos de informes, como este estilo:

```
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
```

No voy a entrar en detalles, pero necesito escribir en tablas algunas values de las keys del json.

---

***Tecnologías:***

Postgres como motor de bases de datos

Python para el desarrollo del ETL

Docker Desktop para correr el clúster on premise

***Objetos kubernetes:***

<ins>Job</ins>: para la ejecución de la imagen construida en Docker a partir del script de python (reemplace el Deployment por un Job que corre una única vez, dado que con Deployment, el pod terminaba y volvía a querer ejecutarse, )

<ins>Statefulset</ins>: para la persistencia de los datos en la bd de postgres

<ins>Service</ins>: entiendo que es la que permite la comunicación entre los pods de manera interna en el clúster más allá que puse None como valor al mismo ya que no estoy exponiendo hacia afuera

---

<ins>***Procedimiento***</ins>

<ins>Primer paso</ins>: desarrollar el código en Python

<ins>Segundo paso</ins>: buildear la imagen a partir del código

```docker buildx build -t etl-cammesa:0.1 .```

<ins>Tercer paso</ins>: buildear los objetos de kubernetes

```
Kubectl apply -f postgres-statefulset.yaml

Kubectl apply -f postgres-service.yaml

Kubectl apply -f etl-job.yaml
```

Realizado esto se crearán 2 pods, 1 service, 1 pvc y 1 pv:

```
k get all

NAME                        READY   STATUS      RESTARTS      AGE
pod/etl-cammesa-job-fw8v6   0/1     Completed   0             21h
pod/postgres-0              1/1     Running     1 (58s ago)   21h

NAME                       TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)    AGE
service/postgres-service   ClusterIP   None         <none>        5432/TCP   21h

NAME                        READY   AGE
statefulset.apps/postgres   1/1     21h

NAME                        STATUS     COMPLETIONS   DURATION   AGE
job.batch/etl-cammesa-job   Complete   1/1           4s         21h

```
```
k get pvc
NAME                          STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
postgres-storage-postgres-0   Bound    pvc-c8caa911-4809-4494-87ac-b3041fd844f3   1Gi        RWO            hostpath       <unset>                 21h
```
```
k get pv
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                                      STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
pvc-c8caa911-4809-4494-87ac-b3041fd844f3   1Gi        RWO            Delete           Bound    test-cammesa/postgres-storage-postgres-0   hostpath       <unset>                          21h
```

---

<ins>Verificación de inserción de los datos en el Persistent Volumen desde el pod de postgresql:</ins>

```
 k exec -it postgres-0 -- bash

root@postgres-0:/# psql -U myuser -d mydatabase

psql (13.18 (Debian 13.18-1.pgdg120+1))

Type "help" for help.

mydatabase=# \dt
          List of relations
 Schema |    Name    | Type  | Owner
--------+------------+-------+--------
 public | documentos | table | myuser
(1 row)

mydatabase=# select * from documentos;
 pk_id |              api_id              |        fecha        |         nemo         |            version
-------+----------------------------------+---------------------+----------------------+-------------------------------
     1 | 8654F8401BA8D96E03258BAA007D9AC1 | 2024-10-01 00:00:00 | PARTE_POST_OPERATIVO | 2024-10-02T19:51:00.000-03:00
(1 row)
```

---

***Próximos Pasos:***

Modificaré el código para extraer la data en días que no estén hardcodeados en el script y dependan de triggers utilizando la librería de *datetime* combinando con el último dato subido de la API y el último dato existente en la tabla para que itere e inserte los registros que puedan ser insertados.