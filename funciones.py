import pandas as pd
import matplotlib.pyplot as plt
import random

def preparar_matriz(matriz):
    filas = len(matriz)
    columnas = len(matriz[0])
    tam = max(filas, columnas)

    for fila in matriz:
        while len(fila) < tam:
            fila.append(0)

    while len(matriz) < tam:
        matriz.append([0] * tam)

    for i in range(tam):
        matriz[i][i] = 0

    return matriz


def matrizcuadrada():
    print("\nNOTA:")
    print("La diagonal principal se asigna automáticamente con valor 0.")
    print("No es necesario ingresar flujo o distancia de una máquina consigo misma.")
    tm = int(input("Ingrese el tamaño de la matriz: "))

    mflujo = []
    mdist = []

    print("\nIngrese la matriz de flujo")
    for i in range(tm):
        fila = []
        for j in range(tm):
            if i == j:
                fila.append(0)
            else:
                valor = int(input(f"Ingrese el flujo [{i}][{j}]: "))
                fila.append(valor)
        mflujo.append(fila)

    print("\nIngrese la matriz de distancia")
    for i in range(tm):
        fila = []
        for j in range(tm):
            if i == j:
                fila.append(0)
            else:
                valor = int(input(f"Ingrese la distancia [{i}][{j}]: "))
                fila.append(valor)
        mdist.append(fila)

    return mflujo, mdist


def matriznocuadrada():
    print("\nNOTA:")
    print("La diagonal principal se asigna automáticamente con valor 0.")
    print("No es necesario ingresar flujo o distancia de una máquina consigo misma.")
    filas = int(input("Ingrese el número de filas: "))
    columnas = int(input("Ingrese el número de columnas: "))

    mflujo = []
    mdist = []

    print("\nIngrese la matriz de flujo")
    for i in range(filas):
        fila = []
        for j in range(columnas):
            if i == j:
                fila.append(0)
            else:
                valor = int(input(f"Ingrese el flujo [{i}][{j}]: "))
                fila.append(valor)
        mflujo.append(fila)

    print("\nIngrese la matriz de distancia")
    for i in range(filas):
        fila = []
        for j in range(columnas):
            if i == j:
                fila.append(0)
            else:
                valor = int(input(f"Ingrese la distancia [{i}][{j}]: "))
                fila.append(valor)
        mdist.append(fila)

    mflujo = preparar_matriz(mflujo)
    mdist = preparar_matriz(mdist)

    return mflujo, mdist


def subirarchivo():
    print("\nFORMATO REQUERIDO")
    print("Excel: un archivo .xlsx con dos hojas.")
    print("Hoja 1: Flujo")
    print("Hoja 2: Distancia")

    print("\nCSV: se necesitan dos archivos.")
    print("Archivo 1: matriz de flujo")
    print("Archivo 2: matriz de distancia")

    print("\n1. Subir archivo Excel")
    print("2. Subir archivos CSV")
    print("3. Regresar al menú principal")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        archivo = input("Ingrese la ruta del archivo Excel: ")

        flujo_df = pd.read_excel(archivo, sheet_name=0, header=None)
        distancia_df = pd.read_excel(archivo, sheet_name=1, header=None)

        mflujo = flujo_df.values.tolist()
        mdist = distancia_df.values.tolist()

        mflujo = preparar_matriz(mflujo)
        mdist = preparar_matriz(mdist)

        return mflujo, mdist

    elif opcion == "2":
        archivo_flujo = input("Ingrese la ruta del CSV de flujo: ")
        archivo_distancia = input("Ingrese la ruta del CSV de distancia: ")

        flujo_df = pd.read_csv(archivo_flujo, header=None)
        distancia_df = pd.read_csv(archivo_distancia, header=None)

        mflujo = flujo_df.values.tolist()
        mdist = distancia_df.values.tolist()

        mflujo = preparar_matriz(mflujo)
        mdist = preparar_matriz(mdist)

        return mflujo, mdist

    elif opcion == "3":
        return None, None

    else:
        print("Opción inválida")
        return None, None


def construccion(mflujo, mdist):
    n = len(mflujo)

    suma_flujos = []
    for i in range(n):
        suma_flujos.append(sum(mflujo[i]))

    suma_distancias = []
    for i in range(n):
        suma_distancias.append(sum(mdist[i]))

    instalaciones = sorted(
        range(n),
        key=lambda x: suma_flujos[x],
        reverse=True
    )

    ubicaciones = sorted(
        range(n),
        key=lambda x: suma_distancias[x]
    )

    asignacion = {}

    for i in range(n):
        asignacion[instalaciones[i]] = ubicaciones[i]

    return asignacion


def funcionobjetivo(mflujo, mdist, asignacion):
    n = len(mflujo)
    costo = 0

    for i in range(n):
        for j in range(n):
            ui = asignacion[i]
            uj = asignacion[j]

            costo += mflujo[i][j] * mdist[ui][uj]

    return costo


def mejora_swap(mflujo, mdist, asignacion):
    mejor_asignacion = asignacion.copy()
    mejor_costo = funcionobjetivo(mflujo, mdist, mejor_asignacion)

    n = len(mejor_asignacion)

    while True:
        mejor_vecino = mejor_asignacion.copy()
        mejor_vecino_costo = mejor_costo

        for i in range(n):
            for j in range(i + 1, n):
                nueva_asignacion = mejor_asignacion.copy()

                nueva_asignacion[i], nueva_asignacion[j] = (
                    nueva_asignacion[j],
                    nueva_asignacion[i]
                )

                nuevo_costo = funcionobjetivo(
                    mflujo,
                    mdist,
                    nueva_asignacion
                )

                if nuevo_costo < mejor_vecino_costo:
                    mejor_vecino_costo = nuevo_costo
                    mejor_vecino = nueva_asignacion

        if mejor_vecino_costo < mejor_costo:
            mejor_costo = mejor_vecino_costo
            mejor_asignacion = mejor_vecino
        else:
            break

    return mejor_asignacion, mejor_costo
def graficar_asignaciones(asignacion_inicial, asignacion_final):
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.set_title("Comparación de Asignaciones QAP")
    ax.axis("off")

    def dibujar_asignacion(asignacion, x_inicio, titulo):
        ax.text(x_inicio + 1, 1.1, titulo, fontsize=14, fontweight="bold", ha="center")

        y = 0

        for maquina, lugar in asignacion.items():
            ax.text(x_inicio, y, f"M{maquina + 1}",
                    bbox=dict(boxstyle="round", facecolor="white"),
                    ha="center", va="center", fontsize=12)

            ax.text(x_inicio + 2, y, f"Lugar {lugar + 1}",
                    bbox=dict(boxstyle="round", facecolor="white"),
                    ha="center", va="center", fontsize=12)

            ax.annotate(
                "",
                xy=(x_inicio + 1.65, y),
                xytext=(x_inicio + 0.35, y),
                arrowprops=dict(arrowstyle="->", linewidth=2)
            )

            y -= 1

    dibujar_asignacion(asignacion_inicial, 0, "Fase 1: Inicial")
    dibujar_asignacion(asignacion_final, 4, "Fase 2: Mejorada")

    plt.tight_layout()
    plt.show()
def construccion_aleatoria(mflujo, mdist):
    n = len(mflujo)

    ubicaciones = list(range(n))
    random.shuffle(ubicaciones)

    asignacion = {}

    for maquina in range(n):
        asignacion[maquina] = ubicaciones[maquina]

    return asignacion
def exportar_resultados_excel(
    asignacion_inicial,
    costo_inicial,
    asignacion_final,
    costo_final,
    mejora,
    tiempo
):
    datos_inicial = []

    for maquina, ubicacion in asignacion_inicial.items():
        datos_inicial.append({
            "Máquina": maquina,
            "Ubicación inicial": ubicacion
        })

    datos_final = []

    for maquina, ubicacion in asignacion_final.items():
        datos_final.append({
            "Máquina": maquina,
            "Ubicación final": ubicacion
        })

    resumen = {
        "Costo inicial": [costo_inicial],
        "Costo final": [costo_final],
        "Porcentaje de mejora": [mejora],
        "Tiempo de ejecución": [tiempo]
    }

    with pd.ExcelWriter("resultados_qap.xlsx") as writer:
        pd.DataFrame(datos_inicial).to_excel(
            writer,
            sheet_name="Asignacion inicial",
            index=False
        )

        pd.DataFrame(datos_final).to_excel(
            writer,
            sheet_name="Asignacion final",
            index=False
        )

        pd.DataFrame(resumen).to_excel(
            writer,
            sheet_name="Resumen",
            index=False
        )

    print("\nResultados exportados en: resultados_qap.xlsx")
