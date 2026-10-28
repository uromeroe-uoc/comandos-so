import os
import csv

def leer_lineas(ruta_archivo):
    """
    Función que lee IPs de un archivo y las devuelve en un array.   
    Las IPs deben estar formateadas una por línea y se espera una ruta en formato Windows.
    """

    # Convertir la ruta en ruta absoluta (ver bibliografia)
    ruta_archivo = os.path.abspath(ruta_archivo)

    # Abrir el archivo en modo lectura y poner cada linea en el array
    lineas = []
    archivo = open(ruta_archivo, "r") 
    for linia in archivo:
        lineas.append(linia.strip()) # .strip elimina caracteres de lineas nuevas (ver bibliografía)

    archivo.close()

    return lineas

def guardar_csv(columnas, datos, ruta_archivo):
    """
    Funcion que guarda datos en un archivo CSV. Los datos deben ser un array de diccionarios.   
    Ejemplo de datos:   
    ```
    columnas = ["nombre", "mac"]
    datos = [   
        {"nombre": "Ethernet", "mac": "9C-6B-00-B4-C9-B6"},   
        {"nombre": "Wi-Fi", "mac": "AA-BB-CC-DD-EE-FF"},   
    ]
    ```
    """

    # Convertir la ruta en ruta absoluta (ver bibliografia)
    ruta_archivo = os.path.abspath(ruta_archivo)

    # Guardar los datos como CSV en el archivo (ver bibliografía)
    with open(ruta_archivo, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columnas)
        writer.writeheader()
        writer.writerows(datos)