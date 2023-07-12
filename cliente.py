from colorama import Fore, Style
import requests
import sys
import json
import os

#Selecciona el primer argumento que será la IP de la PC donde se aloja el servidor.
ip = sys.argv[1]

#Menu
def menu():
    print('\nSe trabajará con la Base de datos ---Muncipios.json---')
    print(Fore.GREEN + "\n======= MENÚ OPCIONES =======" + Style.RESET_ALL)
    print("1. Obtener características de un municipio o comuna")
    print("2. Obtener información de una provincia")
    print("3. Cargar un registro")
    print("4. Descargar municipios.json")
    print("5. Eliminar municipios.json")
    print("6. Eliminar municipio o comuna")
    print("0. Salir")


def obtener_caracteristicas():
    nombre = input("Debe ingresar el nombre del municipio o comuna. \n"
    "Puede ingresar el nombre completo (ej: Municipio Mercedes)\n"
    "Puede ingresar solo el nombre (ej: Mercedes)\n"
    "Nombre: ")
    provincia = input("Ingrese el nombre de la provincia a la que pertenece el municipio/comuna: ")
    url = f"http://{ip}:8000/datos?nombre_municipio={nombre}&provincia={provincia}"
    response = requests.get(url)
    if response.status_code == 200:
        print('\n\n', response.text)
    else:
        print("\n\nError al obtener las características")


def obtener_informacion_provincia():
    nombre = input("Ingrese el nombre de la provincia: ")
    opcion = int(input("Hay cuatro(4) opciones disponibles: \n"
    "Opción 1: devuelve todos los municipios de la provincia ingresada\n"
    "Opción 2: devuelve todas las comunas de la provincia ingresada\n"
    "Opción 3: devuelve todos los municipios y comunas de la provincia ingresada\n"
    "Opción 4: devuelve la cantidad de municipios y comunas de la provincia ingresada\n"
    "Ingrese la opción (1-4): "))
    url = f"http://{ip}:8000/datos_provincia?nombre={nombre}&opcion={opcion}"
    response = requests.get(url)
    if response.status_code == 200:
        print('\n\n',response.text)
    else:
        print("\n\nError al obtener la información de la provincia")


def cargar_registro():
    nombre = input("Ingrese el nombre del municipio o comuna: ")
    n_provincia = input("Ingrese el nombre de la provincia: ")
    categoria = input("Ingrese la categoría (Municipio/Comuna): ")
    fuente = input("Ingrese la fuente (opcional): ")
    url = f"http://{ip}:8000/cargar?nombre={nombre}&n_provincia={n_provincia}&categoria={categoria}&fuente={fuente}"
    response = requests.post(url)
    if response.status_code == 200:
        print("\n\nRegistro cargado exitosamente")
    else:
        print("\n\nError al cargar el municipio o comuna")




def descargar_municipios_json():
    direccion_cliente = os.getcwd()
    url = f"http://{ip}:8000/descarga"
    response = requests.put(url)
    
    if response.status_code == 200:
        contenido = response.json()
        
        with open("municipios.json", 'w') as archivo:
            json.dump(contenido, archivo)
            
        print("\n\nArchivo JSON descargado y guardado correctamente en:", direccion_cliente)
    else:
        print("\n\nError al descargar el archivo JSON:", response.text)





def eliminar_archivo_municipios_json():
    direccion_cliente = os.getcwd()
    url = f"http://{ip}:8000/eliminar_archivo?direccion={direccion_cliente}"
    response = requests.delete(url)
    
    if response.status_code == 200:
            ruta_archivo = os.path.join(direccion_cliente, 'municipios.json')
            os.remove(ruta_archivo)
            print("\n\nArchivo JSON eliminado correctamente.")
    else:
        print("\n\nError al eliminar el archivo JSON:", response.text)


def eliminar_municipio():
    nombre_municipio = input("Ingrese el nombre del municipio o comuna a eliminar: ")
    nombre_provincia = input("Ingrese el nombre de la provincia a la que pertenece: ")
    url = f"http://{ip}:8000/eliminar_municipio?nombre_municipio={nombre_municipio}&nombre_provincia={nombre_provincia}"
    response = requests.delete(url)
    if response.status_code == 200:
        print("\n\nMunicipio o comuna eliminado con éxito.")
    else:
        print("\n\nError al eliminar el municipio o comuna")




# Main
while True:
    menu()
    opcion = input("Ingrese una opción: ")
    if opcion == '0':
        break
    elif opcion == '1':
        obtener_caracteristicas()
    elif opcion == '2':
        obtener_informacion_provincia()
    elif opcion == '3':
        cargar_registro()
    elif opcion == '4':
        descargar_municipios_json()
    elif opcion == '5':
        eliminar_archivo_municipios_json()
    elif opcion == '6':
        eliminar_municipio()
    else:
        print("Opción inválida. Intente nuevamente.")

