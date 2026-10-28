from archivos import leer_lineas, guardar_csv
from comandos import ping, obtener_adaptadores
from datetime import datetime as dt

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
    for a in adaptadores:
        print(f"{a['tipo']}: {a['nombre']} - {a['mac']}")

        # Añadir la hora y fecha para el csv
        a["creacion"] = str(dt.now().isoformat())

    # Guardar los datos en un archivo
    campos = ["tipo", "nombre", "mac", "creacion"]
    guardar_csv(campos, adaptadores, "./informacion_localRomero.csv")

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
        print("Por implementar...")

    else:
        print("Opcion invalida...")
        print("")
        menu()

    # Cuando se acabe de ejecutar cualquier opcion, salir.
    exit(0)

# Ejecutar el menú si se ejecuta el archivo sin importar
if __name__ == "__main__":
    menu()