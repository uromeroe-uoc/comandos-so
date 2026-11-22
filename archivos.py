import os
import csv

def leer_lineas(ruta_archivo):
    """
    Función que lee las lineas de un archivo y las devuelve en un array.   
    """

    # Convertir la ruta en ruta absoluta
    ruta_archivo = os.path.abspath(ruta_archivo)

    # Abrir el archivo en modo lectura y poner cada linea en el array
    lineas = []
    archivo = open(ruta_archivo, "r") 
    for linia in archivo:
        lineas.append(linia.strip()) # .strip elimina caracteres de lineas nuevas

    archivo.close()

    return lineas

def escribir_lineas(lineas, ruta_archivo):
    """
    Función para escribir datos en un archvio.   
    `lineas` debe ser un array de texto (`string[]`)
    `ruta_archivo` debe ser un string con la ruta al archivo donde se escribiran las lineas
    """

    # Convertir la ruta en ruta absoluta
    ruta_archivo = os.path.abspath(ruta_archivo)

    # Guardar los datos en el archivo
    with open(ruta_archivo, "w", encoding="utf-8", newline="") as f:
        texto = "\n".join(lineas) + "\n" # Para que cada linea del array no necesite '\n' al final
        f.write(texto)

def escribir_csv(dict, ruta_archivo):
    """
    Función que guarda los datos en formato `dict` en un archivo.
    """

    # Convertir la ruta en ruta absoluta
    ruta_archivo = os.path.abspath(ruta_archivo)

    # Guardar los datos en el archivo
    with open(ruta_archivo, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=dict[0].keys())
        writer.writeheader()
        writer.writerows(dict)