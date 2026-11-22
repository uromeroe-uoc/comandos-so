
def menu():
    """Muestra el menú para seleccionar las diferentes funciones del programa."""

    ejecutar = True
    while ejecutar:
        # Mostrar las opciones
        print(" -- Seleccionar opcion -- ")
        print("1. Leer los servidores DNS")
        print("0. Salir del programa")
        print("")
        opcion = int(input("Selecciona una opcion: "))
        print("")

        # Ejecutar una función u otra según la selección
        if opcion == 0:
            exit(0)

        elif opcion == 1:
            print("Por implementar...")

        else:
            print("Opcion invalida...")

if __name__ == "__main__":
    menu()