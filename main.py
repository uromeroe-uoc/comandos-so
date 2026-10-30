from archivos import leer_lineas, guardar_csv, escribir_lineas
from comandos import ping, obtener_adaptadores, datos_adaptador
from datetime import datetime


def lanzar_pings():
    """Lee IPs en un archivo de texto y las comprueba meidante pings"""

    # Obtener la ruta del archivo y leer sus IPs
    ruta = input("Escribe la ruta relativa o absoluta del archivo: ")
    lista = leer_lineas(ruta)

    # Mostrar IPs
    print(f"IPs obtenidas: {lista}")

    # Comprobar IPs
    for ip in lista:
        print(f"  {ip}", end='', flush=True) # end='' vacío para actualizar en la misma linea el resultado (ver bibliografía)
        if ping(ip):
            print(" - OK")
        else:
            print(" - Sin respuesta")


def registrar_mac():
    """
    Muestra las direcciones MAC de los adaptadores disponibles y las almacena en un archivo .csv.   
    Además registra la fecha y hora de creación del archivo.
    """

    # Obtener los adaptadores y mostrarlos
    adaptadores = obtener_adaptadores()
    datos_csv = []
    idx = 0
    for a in adaptadores:
        datos = datos_adaptador(a["tipo"])
        print(f"{idx}. ({datos['tipo']}) {datos['nombre']} - {datos['mac']}")

        # Guardar los datos para el csv
        datos_csv.append({"tipo": datos["tipo"], "nombre": datos["nombre"], "mac": datos["mac"], "tiempo": datetime.now()})

        idx += 1

    # Guardar los datos en el csv
    columnas = ["tipo", "nombre", "mac", "tiempo"]
    guardar_csv(columnas, datos_csv, "./informacion_localRomero.csv")


def configuracion_adaptador():
    """
    Muestra un submenú con los adaptadores de red disponibles. En elegir uno, muestra su IP, máscara y puerta de enlace.
    Además, guardará esa información en un documento de texto.
    """

    # Obtener los adaptadores disponibles
    adatpadores = obtener_adaptadores()
    idx = 0
    for a in adatpadores:
        print(f"{idx}. ({a['tipo']}) {a['nombre']}")
        idx += 1

    # Seleccionar un adaptador
    opcion = int(input("Selecciona un adaptador: "))
    datos = datos_adaptador(adatpadores[opcion]['tipo'])

    # Mostrar los datos
    print("")
    print(f"IP: {datos["ip"]}")
    print(f"Mascara: {datos["mascara"]}")
    print(f"Puerta de enlace: {datos["gateway"]}")

    # Exportar los datos
    lineas = []
    lineas.append(str(datos['ip']))
    lineas.append(str(datos['mascara']))
    lineas.append(str(datos['gateway']))

    escribir_lineas(lineas, "./adaptadorRomero.txt")


def menu():
    """Muestra el menú para seleccionar las diferentes funciones del programa."""

    # Mostrar las opciones
    print(" -- Seleccionar opcion -- ")
    print("1. Lanzar ping a una lista de IP")
    print("2. Mostrar MAC de los adaptadores instalados")
    print("3. Exportar la configuración de red de un adaptador")
    print("0. Salir del programa")
    print("")
    opcion = int(input("Selecciona una opcion: "))
    print("")

    # Ejecutar una función u otra según la selección
    if opcion == 0:
        exit(0)

    elif opcion == 1:
        lanzar_pings()

    elif opcion == 2:
        registrar_mac()

    elif opcion == 3:
        configuracion_adaptador()

    else:
        print("Opcion invalida...")
        print("")
        menu()

    # Cuando se acabe de ejecutar cualquier opcion, salir.
    exit(0)


# Ejecutar el menú si se ejecuta el archivo sin importar
if __name__ == "__main__":
    menu()