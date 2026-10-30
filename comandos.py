import subprocess
import csv
import socket
import struct


def ping(ip):
    """Lanza un ping a la IP especificada y devuelve el estado de la conexión."""

    res = subprocess.run(["ping", ip], capture_output=True)
    
    # Comporbando desde cmd usando %errorlevel% ping devuelve 0 o 1 dependiendo del éxito del comando
    return 0 if bool(res.returncode) else 1


def obtener_adaptadores():
    """
    Devuelve un array de diccionarios con el tipo y nombre de cada adaptador de red del dispositivo.   
    Ejemplo:   
    ```
    [
        { "tipo": "Ethernet", "nombre": "Realtek PCIe GbE Family Controller" },
        { "tipo": "Wi-Fi", "nombre": "Intel PRO/Wireless 2011B LAN Access Point" },
    ]
    ```
    """

    # Obtener los adaptadores
    comando = "Get-NetAdapter | Select-Object Name, InterfaceDescription | ConvertTo-Csv -NoTypeInformation"
    res = subprocess.run(["powershell", "-Command", comando], capture_output=True, text=True)

    # Leer el CSV de los adaptadores
    adaptadores = []
    lector = csv.DictReader(res.stdout.splitlines())
    for fila in lector:
        adaptadores.append({"tipo": fila["Name"], "nombre": fila["InterfaceDescription"]})

    # Devolver los datos de los adaptadores
    return adaptadores


def datos_adaptador(tipo):
    """
    Devuelve un diccionario con los datos del adaptador seleccionado.   
    Ejemplo:   
    ```
    {
        "tipo": "Ethernet", 
        "nombre": "Realtek PCIe GbE Family Controller",
        "mac": "aa-bb-cc-dd-ee-ff",
        "ip": "192.168.1.10",
        "mascara": "255.255.255.0"
        "gateway": "192.168.1.1",
    }
    ```
    """

    datos = {}

    # Obtener los datos
    comando = (
        f"Get-NetIPConfiguration -Detailed -InterfaceAlias '{tipo}' | "
        "Select-Object InterfaceAlias, InterfaceDescription, "
        "@{n='MAC';e={$_.NetAdapter.LinkLayerAddress}}, "
        "@{n='IPv4';e={$_.IPv4Address.IPAddress}}, "
        "@{n='Gateway';e={$_.IPv4DefaultGateway.NextHop}} | "
        "ConvertTo-Csv -NoTypeInformation"
    )
    res = subprocess.run(["powershell", "-Command", comando], capture_output=True, text=True)

    fila = next(csv.DictReader(res.stdout.splitlines()))
    datos["tipo"] = fila["InterfaceAlias"]
    datos["nombre"] = fila["InterfaceDescription"]
    datos["mac"] = fila["MAC"]
    datos["ip"] = fila["IPv4"]
    datos["gateway"] = fila["Gateway"]

    # Obtener la mascara, ya que el anterior comando no la devuelve
    comando = f"Get-NetIPAddress -IPAddress '{fila['IPv4']}' | Select-Object PrefixLength"
    res = subprocess.run(["powershell", "-Command", comando], capture_output=True, text=True)

    mascara = str(res.stdout.splitlines()[3]).strip()
    mascara = int(mascara)
    host_bits = 32 - int(mascara)
    mascara = socket.inet_ntoa(struct.pack('!I', (1 << 32) - (1 << host_bits)))

    datos["mascara"] = str(mascara)

    # Devolver los datos
    return datos