import subprocess
import csv
import re

def obtener_adaptadores():
    """
    Funcion para obtener la configuración de red d e todos los adaptadores del dispositivo.
    """

    comando = (
        "Get-NetIPConfiguration -Detailed | Select-Object InterfaceIndex, InterfaceAlias, InterfaceDescription,"
        "@{n='MAC';e={$_.NetAdapter.LinkLayerAddress}},"
        "@{n='IPv4';e={$_.IPv4Address.IPAddress}},"
        "@{n='Gateway';e={$_.IPv4DefaultGateway.NextHop}},"
        "@{n='DNSServers';e={$_.DNSServer.ServerAddresses -join ', '}} | "
        "ConvertTo-Csv -NoTypeInformation"
    )
    res = subprocess.run(["powershell", "-Command", comando], capture_output=True, text=True)

    filas = csv.DictReader(res.stdout.splitlines())
    return list(filas)

def medir_tiempo_ip(ip, veces=5):
    """
    Mide la latencia a una IP con 'veces' pings.
    Descarta el valor más alto y promedia los restantes.
    Devuelve None si no responden todos los pings.
    """

    # Ejecutar el comando
    res = subprocess.run(["ping", "-n", str(veces), ip], capture_output=True, text=True)

    # Encontrar los tiempos en la salida. Independientemente del idioma (fuente: Claude Sonnet 5.5)
    tiempos = [int(t) for t in re.findall(r"(?:tiempo|time)[=<](\d+)", res.stdout)]

    # Si no responden todos los paquetes, no devolver nada
    if len(tiempos) < veces:
        return None 

    # Descartar el más alto y devolver el promeido restante
    tiempos.remove(max(tiempos))
    return sum(tiempos) / len(tiempos)

def contar_saltos(ip):
    """
    Funcion que cuenta los saltos para llegar a una IP.
    Devuelve los saltos o None según el resultado.
    """

    res = subprocess.run(["tracert", "-d", "-h", "30", "-w", "1000", ip], capture_output=True, text=True)

    saltos = None
    for l in res.stdout.splitlines():
        m = re.match(r"^\s*(\d+)\s", l)
        if m and l.split()[-1] == ip:
            saltos = int(m.group(1))

    return saltos

def asignar_dns(adaptador, ip):
    """
    Configura el DNS de un adaptador de red.
    """

    idx = adaptador["InterfaceIndex"]
    interno = f"Set-DnsClientServerAddress -InterfaceIndex {idx} -ServerAddresses {ip} -ErrorAction Stop"

    comando = (
        "$p = Start-Process powershell -Verb RunAs -Wait -PassThru "
        f"-ArgumentList '-NoProfile','-Command','{interno}'; "
        "exit $p.ExitCode"
    )

    res = subprocess.run(["powershell", "-NoProfile", "-Command", comando],
                         capture_output=True, text=True)

    return res.returncode == 0