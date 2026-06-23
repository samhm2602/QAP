from funciones import (
    matrizcuadrada,
    matriznocuadrada,
    subirarchivo,
    construccion,
    construccion_aleatoria,
    funcionobjetivo,
    mejora_swap,
    graficar_asignaciones,
    exportar_resultados_excel
)
import time


def menu():
    while True:
        print("\n===== MENÚ PRINCIPAL =====")
        print("1. Ingresar datos manualmente")
        print("2. Cargar datos desde archivo Excel/CSV")
        print("3. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "3":
            print("Gracias por usar el programa.")
            break

        inicio = time.time()

        if opcion == "1":
            op = input("Ingrese MC si es cuadrada o NC si no es cuadrada: ").upper()

            if op == "MC":
                mflujo, mdist = matrizcuadrada()
            elif op == "NC":
                mflujo, mdist = matriznocuadrada()
            else:
                print("Opción inválida")
                continue

        elif opcion == "2":
            mflujo, mdist = subirarchivo()

            if mflujo is None or mdist is None:
                continue

        else:
            print("Opción inválida")
            continue

        tam_flujo = len(mflujo)
        tam_dist = len(mdist)

        if tam_flujo != tam_dist:
            print("\nERROR: Las matrices deben tener el mismo tamaño.")
            continue

        for fila in mflujo:
            if len(fila) != tam_flujo:
                print("\nERROR: La matriz de flujo está mal formada.")
                continue

        for fila in mdist:
            if len(fila) != tam_dist:
                print("\nERROR: La matriz de distancia está mal formada.")
                continue

        print("\nMatriz de flujo:")
        for fila in mflujo:
            print(fila)

        print("\nMatriz de distancia:")
        for fila in mdist:
            print(fila)

        print("\nSeleccione método de construcción:")
        print("1. Mayor flujo - menor costo")
        print("2. Aleatorio")

        metodo = input("Seleccione una opción: ")

        if metodo == "1":
            asignacion = construccion(mflujo, mdist)
        elif metodo == "2":
            asignacion = construccion_aleatoria(mflujo, mdist)
        else:
            print("Método inválido")
            continue

        print("\nAsignación inicial:")
        for maquina, ubicacion in asignacion.items():
            print(f"Máquina {maquina} -> Ubicación {ubicacion}")

        costo_inicial = funcionobjetivo(mflujo, mdist, asignacion)

        print("\nValor función objetivo inicial:")
        print(costo_inicial)

        asignacion_final, costo_final = mejora_swap(mflujo, mdist, asignacion)

        print("\nAsignación final mejorada:")
        for maquina, ubicacion in asignacion_final.items():
            print(f"Máquina {maquina} -> Ubicación {ubicacion}")

        graficar_asignaciones(asignacion, asignacion_final)

        print("\nCosto final:")
        print(costo_final)

        if costo_inicial != 0:
            mejora = ((costo_inicial - costo_final) / costo_inicial) * 100
        else:
            mejora = 0

        print("\nPorcentaje de mejora:")
        print(mejora, "%")

        fin = time.time()
        tiempo_total = fin - inicio

        print("\nTiempo total de ejecución:")
        print(tiempo_total, "segundos")

        exportar = input("\n¿Desea exportar los resultados a Excel? (S/N): ").upper()

        if exportar == "S":
            exportar_resultados_excel(
                asignacion,
                costo_inicial,
                asignacion_final,
                costo_final,
                mejora,
                tiempo_total
            )

        print("\n1. Regresar al menú")
        print("2. Salir")

        regresar = input("Seleccione una opción: ")

        if regresar == "2":
            print("Gracias por usar el programa.")
            break


menu()