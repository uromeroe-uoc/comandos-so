from archivos import escribir_csv, leer_lineas
from comandos import asignar_dns, contar_saltos, medir_tiempo_ip, obtener_adaptadores

def mostrar_ip_txt():
    """
    Muestra las IP que hay dentro de un archivo de texto.
    """

    # Obtener la ruta del archivo
    archivo = input("Indica dónde está el archvio con las IPs: ")
    ips = leer_lineas(archivo)

    # Mostrar todas las IPs almacenadas en el archivo
    print("IPs encontradas: ")
    for ip in ips:
        print(f" - {ip}")

def mostrar_config_red():
    """
    Muestra las configuraciones de red de los diferentes adaptadores y lo registra en un documento.
    """

    # Obtener la info de los adaptadores
    adapt = obtener_adaptadores()

    # Mostrar los adaptadores
    for a in adapt:
        print(a["InterfaceDescription"])
        print(f" - IP: {a['IPv4']}")
        print(f" - MAC: {a['MAC']}")
        print(f" - Gateway: {a['Gateway']}")
        print(f" - DNS: {a['DNSServers']}")
        print("")

    # Guardar los datos en el documento
    escribir_csv(adapt, "configuracionlocal_Romero.txt")

def seleccionar_adaptador():
    """
    Funcion que selecciona un adaptador de red y además muestra sus DNS configurados.
    Devuelve el adaptador seleccionado (dict) o None si la selección es inválida.
    """

    # Obtener los adaptadores
    adapt = obtener_adaptadores()

    # Seleccionar el adaptador
    for idx, a in enumerate(adapt):
        print(f" - {idx}. {a['InterfaceDescription']}")

    try:
        opcion = int(input("Selecciona una opcion: "))
        seleccionado = adapt[opcion]
    except (ValueError, IndexError):
        print("Opcion invalida...")
        return None

    # Mostrar sus servidores DNS
    print("")
    print(f"Servidores DNS: {seleccionado['DNSServers']}")
    print("")

    # Devolver el adaptador seleccionado
    return seleccionado

def configurar_dns(adaptador):
    """
    Función para comprobar la velocidad entre los DNS de un archivo y los de un adaptador de red.
    En caso de encontrar un DNS más rápido que el activo, se configurará el más rápido.
    """

    # Obtener las IPs de los DNS del archivo
    archivo = input("Indica dónde está el archvio con las IPs: ")
    ips = leer_lineas(archivo)

    # Añadir a la lista las IPs del adaptador de red
    if adaptador == None:
        print("No hay ningún adaptador seleccionado, no se usarán sus DNS para la comprobación")
    else:
        print("Se usarán también los DNS del adaptador seleccionado para la comprobación")
        ips.extend(adaptador["DNSServers"].split(", "))

    # Medir cada tiempo de cada IP
    resultados = []
    for i in ips:
        print(f"Midiendo '{i}'...")
        tiempo = medir_tiempo_ip(i)    
        resultados.append({ "ip": i, "tiempo": tiempo })

    # Descartamos los que no hayan respondido adecuadamente
    validos = []
    for r in resultados:
        if r["tiempo"] is not None:
            validos.append(r)

    # Ordenamos por tiempo de forma ascendente (fuente: Claude Sonnet 5.5)
    validos.sort(key=lambda r: r["tiempo"])

    # Si hay tiempos empatados, comprobamos por saltos para ordenar
    mejor_tiempo = validos[0]["tiempo"]
    empatados = []
    for v in validos:
        if v["tiempo"] == mejor_tiempo:
            empatados.append(v)

    if len(empatados) > 1:
        print("Comprobando saltos para las DNS empatadas...")
        for e in empatados:
            e["saltos"] = contar_saltos(e["ip"])

        # Ordenamos los empatados por saltos
        empatados.sort(key=lambda r: (r["saltos"] is None, r["saltos"] or 0))

    # Mostrar ganador
    ganador = empatados[0]
    print("")
    print(f"DNS ganadora: {ganador['ip']}")

    # Asignar DNS en el dispositivo
    if adaptador == None:
        print("No se configura el adaptador ya que no se ha seleccionado")
    else:
        if asignar_dns(adaptador, ganador["ip"]) == 1:
            print("DNS configurada correctamente")
        else:
            print("Ha habido un error configurando el DNS")

    print("")

def menu():
    """Muestra el menú para seleccionar las diferentes funciones del programa."""

    # Guardar el adaptador seleccionado (ej. 7 en adelante)
    adaptador = None

    ejecutar = True
    while ejecutar:
        # Mostrar las opciones
        print(" -- Seleccionar opcion -- ")
        print("1. Leer los servidores DNS")
        print("2. Mostrar la configuración de red")
        print("3. Seleccionar un adaptador de red")
        print("4. Configurar el DNS más rápido")
        print("0. Salir del programa")
        print("")
        try:
            opcion = int(input("Selecciona una opcion: "))
        except ValueError:
            print("Opcion invalida...")
            continue

        print("")

        # Ejecutar una función u otra según la selección
        if opcion == 0:
            ejecutar = False

        elif opcion == 1:
            mostrar_ip_txt()

        elif opcion == 2:
            mostrar_config_red()

        elif opcion == 3:
            adaptador = seleccionar_adaptador()

        elif opcion == 4:
            configurar_dns(adaptador)

        else:
            print("Opcion invalida...")

    exit(0)

if __name__ == "__main__":
    menu()