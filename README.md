## API Municipios Argentina

Este proyecto tiene como objetivo crear una comunicación entre un cliente y un servidor mediante
una API Sincronica, la cual será realizada con Python y la librería FastApi. El servidor se encargará de almacenar una base de datos
JSON seleccionada, y procesará las consultas y modificaciones realizadas sobre
ella. Por su parte, el cliente será responsable de realizar las consultas y
modificaciones necesarias.

Base de datos seleccionada: municipios.json:
URL:https://infra.datos.gob.ar/catalog/modernizacion/dataset/7/distribution/7.4/downl
oad/municipios.json

La misma representa la lista de las entidades que representan la división político
administrativa de tercer orden de la República Argentina, en base a datos del
Instituto Geográfico Nacional (IGN). Incluye comunas, juntas vecinales y demás
formas de gobierno local en formato JSON.

## Archivos incluidos: 

`servidor.py`: Archivo python que contiene el código del servidor de la API.

`cliente.py`: Archivo python que contiene el código del cliente.


## Procedimiento para utilziar la API (en dos PC de la misma red).

1. Descargar o clonar el repositorio en tu máquina local.

2. Abrir la terminal en la carpeta donde se encuentre `servidor.py`

3.  Corremos el comando `uvicorn servidor:app --host 0.0.0.0` . El mismo inicia
un servidor web utilizando Uvicorn y especifica que el servidor debe
escuchar en todas las interfaces de red disponibles.

4. Una vez hecho esto, tendremos que saber cual es la dirección IP de nuestra
PC que almacena al servidor. Para averiguar la misma, tenemos varias
opciones, una de ellas es correr el comando `ipconfig` en la terminal de windows.
Supongamos que la IPv4 de la PC que almacena el servidor es 192.168.1.5.

5. Para comunicarnos mediante `cliente.py`, debemos ejecutar el archivo python
y pasarle como argumento la IP de la pc que almacena el servidor.
Por ejemplo: `Python3 cliente.py 192.168.1.5`

7. Allí, ya podremos hacerle consultar e interactuar con la API

8. Si queremos comunicarnos mediante el navegador, abrimos DOCS.
La URL será: `http://192.168.1.5:8000/docs`














