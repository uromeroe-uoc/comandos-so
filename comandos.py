import subprocess
import csv

def ping(ip):
    """Lanza un ping a la IP especificada y devuelve el estado de la conexión."""

    res = subprocess.run(["ping", ip], capture_output=True)
    
    # Comporbando desde cmd usando %errorlevel% ping devuelve 0 o 1 dependiendo del éxito del comando
    return 0 if bool(res.returncode) else 1

def obtener_adaptadores():
    """
    Devuelve en un array de diccionarios toda la información sobre los adaptadores de red del dispositivo.   
    Datos devueltos de ejemplo:
    ```
    [   
        {"tipo": "Ethernet", "nombre": "Realtek PCIe GbE Family Controller", "mac": "9C-6B-00-B4-C9-B6"},
        {"tipo": "Wi-Fi", "nombre": "Intel(R) Wi-Fi 6 AX201 160MHz", "mac": "A4-C3-F0-12-34-56"}
    ]
    ```
    """

    res = subprocess.run(["getmac", "/FO", "csv", "/V"], capture_output=True, text=True, check=True)
    adaptadores = []

    # Leer cada linea del CSV devuelto
    lector = csv.DictReader(res.stdout.splitlines())
    for fila in lector:
        adaptadores.append({"tipo": fila["Connection Name"], "nombre": fila["Network Adapter"], "mac": fila["Physical Address"]})

    return adaptadores