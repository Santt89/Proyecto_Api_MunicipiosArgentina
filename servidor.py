import requests
import json
from fastapi import FastAPI
import uvicorn
import os

#URL de la base json.
url = 'https://infra.datos.gob.ar/catalog/modernizacion/dataset/7/distribution/7.4/download/municipios.json'

# Realizar la solicitud GET para obtener el contenido de la URL
response = requests.get(url)

municipios_json = response.json()

#Creamos la api
app = FastAPI()


#GET1
@app.get("/datos")

#Devolvera las caracteristicas del Municipio o comuna ingresado.
def info(nombre_municipio : str , provincia: str):
  for municipio in municipios_json['municipios']:
    #Podemos ingresar el nombre completo: 'Municipio Pérez' o solo el nombre de la ciudad o comuna: 'Pérez' 
    if (municipio['nombre_completo'] == nombre_municipio or municipio['nombre'] == nombre_municipio) and (municipio['provincia']['nombre'] == provincia)  :
      return ' ; '.join([
                'Nombre: ' + municipio['nombre_completo'],
                'Provincia: ' + municipio['provincia']['nombre'],
                'Categoria: ' + municipio['categoria'],
                'Fuente: ' + municipio['fuente']
            ])
  return 'No se encontro ninguna comuna ni municipio'



#GET2
@app.get("/datos_provincia")

#Dependiendo de la opcion devolverá lo siguiente:
#opcion 1 devulve todos los municipios de la provincia ingresada
#opcion 2 devuelve todas las comunas de la provincia ingresada
#opcion 3 devuelve todos los municipios y comunas de la provincia ingresada
#opcion 4 devuelve la cantidad de municipios y comunas de la provincia ingresada

def info_prov(nombre : str , opcion : int):

  #Devuelve todos los municipios
  if opcion == 1:
    municipios = [] # Lista para almacenar los municipios
    for municipio in  municipios_json['municipios']:
      if municipio['categoria'] == 'Municipio' and municipio['provincia']['nombre'] == nombre:
        municipios.append(('Nombre: ', municipio['nombre_completo'], 'Provincia:', municipio['provincia']['nombre'], 'Fuente:', municipio['fuente'], 'Categoria:', municipio['categoria']))
    
    if len(municipios) == 0:
       return ('No se encontro ningun municipio en la provincia: ', nombre)
    return municipios


  #Devuelve todas las comunas
  elif opcion == 2:
    comunas = []  # Lista para almacenar las comunas
    for municipio in municipios_json['municipios']:
        if municipio['categoria'] == 'Comuna' and municipio['provincia']['nombre'] == nombre:
            comunas.append(('Nombre: ', municipio['nombre_completo'], 'Provincia:', municipio['provincia']['nombre'], 'Fuente:', municipio['fuente'], 'Categoria:', municipio['categoria']))
    if len(comunas) == 0:
       return 'No se encontro ninguna comuna en la provincia: ', nombre
    return comunas
  

  #Devuelve todos los municipios y comunas
  elif opcion == 3:
    ambos = [] # Lista para almacenar tanto los municipios como las comunas
    for municipio in  municipios_json['municipios']:
          if municipio['provincia']['nombre'] == nombre:
            ambos.append(('Nombre: ', municipio['nombre_completo'], 'Provincia:', municipio['provincia']['nombre'], 'Fuente:', municipio['fuente'], 'Categoria:', municipio['categoria']))       
    if len(ambos) == 0:
       return 'No se encontro ninguna comuna ni municipio en: ', nombre
    return ambos
  
    #Devuelve la cantidad de municipios y comunas que hay en la provincia
  elif opcion == 4:
    comunas = []
    municipios = []
    for municipio in municipios_json['municipios']:
        if municipio['categoria'] == 'Comuna' and municipio['provincia']['nombre'] == nombre:
          comunas.append(municipio)
        if municipio['categoria'] == 'Municipio' and municipio['provincia']['nombre'] == nombre:
          municipios.append(municipio)
    #En caso que ambas listas quedan vacias, quiere decir que la provincia ingresada no es valida.
    if len(comunas) == 0 and len(municipios) == 0:
     return 'Nombre de provincia inválido.'
    return 'Municipios: ', len(municipios) , 'Comunas: ',len(comunas)
  

  else:
    return 'Ingrese una provincia válida'






#POST
@app.post('/cargar')
#Cargaremos un registro a nuestra base de datos
def carga(nombre, n_provincia, categoria, fuente = None):
    provincia = {}
    provincia['nombre'] = n_provincia

    # Crear el nuevo municipio
    nuevo_municipio = {
        "nombre_completo": nombre,
        'provincia': provincia,
        "fuente": fuente,
        "categoria": categoria
    }

    #Agregar el nuevo municipio a la lista de municipios
    municipios_json['municipios'].append(nuevo_municipio)

    # Actualizar los campos total y cantidad
    municipios_json['total'] += 1
    municipios_json['cantidad'] += 1






#PUT
@app.put('/descarga')
def descarga():
    return municipios_json





#DELETE1
@app.delete('/eliminar_archivo')
def eliminar_archivo(direccion: str):
    nombre_archivo = 'municipios.json'
    ruta_archivo = os.path.join(direccion, nombre_archivo)

    if os.path.exists(ruta_archivo):
       return {"message": "Archivo eliminado correctamente."}
    else:
       return {"message": "No se encontró el archivo en la dirección especificada."}



#DELETE2
@app.delete('/eliminar_municipio')
def eliminar_municipio(nombre_municipio, nombre_provincia):
    municipios = municipios_json['municipios']

    # Buscar el municipio por nombre y provincia
    indice_municipio = None
    for i, municipio in enumerate(municipios):
        if municipio['nombre_completo'] == nombre_municipio and municipio['provincia']['nombre'] == nombre_provincia:
            indice_municipio = i
            break
        
    # Eliminar el municipio si se encontró
    if indice_municipio is not None:
        municipios.pop(indice_municipio)
        municipios_json['cantidad'] -= 1
        municipios_json['total'] -= 1
        print('Municipio o comuna eliminado con éxito.')



