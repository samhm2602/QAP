import streamlit as st
import pandas as pd
import time
import io
import matplotlib.pyplot as plt

from funciones import (
    preparar_matriz,
    construccion,
    construccion_aleatoria,
    funcionobjetivo,
    mejora_swap
)
def crear_tabla_asignacion(asignacion):
    datos = []

    for maquina, ubicacion in asignacion.items():
        datos.append({
            "Máquina": f"M{maquina + 1}",
            "Ubicación asignada": f"Lugar {ubicacion + 1}"
        })

    return pd.DataFrame(datos)


def crear_tabla_comparativa(asignacion_inicial, asignacion_final):
    datos = []

    for maquina in asignacion_inicial.keys():
        datos.append({
            "Máquina": f"M{maquina + 1}",
            "Asignación inicial": f"Lugar {asignacion_inicial[maquina] + 1}",
            "Asignación final": f"Lugar {asignacion_final[maquina] + 1}"
        })

    return pd.DataFrame(datos)


def crear_grafica(asignacion_inicial, asignacion_final):
    df = crear_tabla_comparativa(asignacion_inicial, asignacion_final)

    fig, ax = plt.subplots(figsize=(9, 3 + len(df) * 0.4))
    ax.axis("off")

    tabla = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        loc="center",
        cellLoc="center"
    )

    tabla.auto_set_font_size(False)
    tabla.set_fontsize(11)
    tabla.scale(1.2, 1.6)

    ax.set_title(
        "Comparación de Asignaciones QAP",
        fontsize=16,
        fontweight="bold",
        pad=20
    )

    return fig


def generar_excel(asignacion_inicial, costo_inicial, asignacion_final, costo_final, mejora, tiempo):
    salida = io.BytesIO()

    df_inicial = crear_tabla_asignacion(asignacion_inicial)
    df_final = crear_tabla_asignacion(asignacion_final)

    resumen = pd.DataFrame({
        "Costo inicial": [costo_inicial],
        "Costo final": [costo_final],
        "Porcentaje de mejora": [mejora],
        "Tiempo de ejecución": [tiempo]
    })

    with pd.ExcelWriter(salida, engine="openpyxl") as writer:
        df_inicial.to_excel(writer, sheet_name="Asignacion inicial", index=False)
        df_final.to_excel(writer, sheet_name="Asignacion final", index=False)
        resumen.to_excel(writer, sheet_name="Resumen", index=False)

    salida.seek(0)
    return salida


def poner_diagonal_cero(matriz):
    n = min(len(matriz), len(matriz[0]))

    for i in range(n):
        matriz[i][i] = 0

    return matriz


def ejecutar_qap(mflujo, mdist, metodo):
    if len(mflujo) != len(mdist):
        st.error("ERROR: Las matrices deben tener el mismo tamaño.")
        st.stop()

    for fila in mflujo:
        if len(fila) != len(mflujo):
            st.error("ERROR: La matriz de flujo está mal formada.")
            st.stop()

    for fila in mdist:
        if len(fila) != len(mdist):
            st.error("ERROR: La matriz de distancia está mal formada.")
            st.stop()

    inicio = time.time()

    if metodo == "Mayor flujo - menor costo":
        asignacion = construccion(mflujo, mdist)
    else:
        asignacion = construccion_aleatoria(mflujo, mdist)

    costo_inicial = funcionobjetivo(mflujo, mdist, asignacion)

    asignacion_final, costo_final = mejora_swap(
        mflujo,
        mdist,
        asignacion
    )

    fin = time.time()
    tiempo = fin - inicio

    if costo_inicial != 0:
        porcentaje_mejora = ((costo_inicial - costo_final) / costo_inicial) * 100
    else:
        porcentaje_mejora = 0

    st.success("QAP ejecutado correctamente")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Asignación inicial")
        st.dataframe(crear_tabla_asignacion(asignacion))
        st.metric("Costo inicial", costo_inicial)

    with col2:
        st.subheader("Asignación final")
        st.dataframe(crear_tabla_asignacion(asignacion_final))
        st.metric("Costo final", costo_final)

    st.metric("Porcentaje de mejora", f"{porcentaje_mejora:.2f}%")
    st.metric("Tiempo de ejecución", f"{tiempo:.4f} segundos")

    fig = crear_grafica(asignacion, asignacion_final)

    st.subheader("Comparación gráfica de asignaciones")
    st.pyplot(fig)

    imagen = io.BytesIO()
    fig.savefig(imagen, format="png", bbox_inches="tight")
    imagen.seek(0)

    excel = generar_excel(
        asignacion,
        costo_inicial,
        asignacion_final,
        costo_final,
        porcentaje_mejora,
        tiempo
    )

    st.download_button(
        label="Descargar resultados en Excel",
        data=excel,
        file_name="resultados_qap.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.download_button(
        label="Descargar gráfica",
        data=imagen,
        file_name="grafica_qap.png",
        mime="image/png"
    )


st.set_page_config(
    page_title="QAP",
    page_icon="📊",
    layout="wide"
)

st.title("QAP")
st.subheader("Problema de Asignación Cuadrática")

st.divider()

modo = st.radio(
    "Seleccione cómo desea ingresar los datos:",
    [
        "Ingresar manualmente",
        "Subir archivo Excel",
        "Subir archivos CSV"
    ]
)

st.divider()

mflujo = None
mdist = None

if modo == "Ingresar manualmente":
    st.header("Entrada manual")

    tipo_matriz = st.radio(
        "Seleccione el tipo de matriz:",
        [
            "Cuadrada",
            "No cuadrada"
        ]
    )

    st.info(
        "La diagonal principal se asigna automáticamente con valor 0."
    )

    if tipo_matriz == "Cuadrada":
        tamaño = st.number_input(
            "Ingrese el tamaño de la matriz",
            min_value=2,
            value=3,
            step=1
        )

        filas = tamaño
        columnas = tamaño

    else:
        col_a, col_b = st.columns(2)

        with col_a:
            filas = st.number_input(
                "Número de filas",
                min_value=2,
                value=3,
                step=1
            )

        with col_b:
            columnas = st.number_input(
                "Número de columnas",
                min_value=2,
                value=3,
                step=1
            )

    st.subheader("Matriz de flujo")

    df_flujo_base = pd.DataFrame(
        [[0 for _ in range(columnas)] for _ in range(filas)]
    )

    df_flujo = st.data_editor(
        df_flujo_base,
        key="flujo_manual",
        use_container_width=True
    )

    st.subheader("Matriz de distancia")

    df_dist_base = pd.DataFrame(
        [[0 for _ in range(columnas)] for _ in range(filas)]
    )

    df_dist = st.data_editor(
        df_dist_base,
        key="distancia_manual",
        use_container_width=True
    )

    mflujo = df_flujo.values.tolist()
    mdist = df_dist.values.tolist()

    mflujo = poner_diagonal_cero(mflujo)
    mdist = poner_diagonal_cero(mdist)

    mflujo = preparar_matriz(mflujo)
    mdist = preparar_matriz(mdist)

elif modo == "Subir archivo Excel":
    st.header("Carga desde Excel")

    st.info(
        """
        Formato requerido:

        - Un solo archivo Excel.
        - Hoja 1: matriz de flujo.
        - Hoja 2: matriz de distancia.
        - La diagonal principal será ajustada automáticamente a 0.
        """
    )

    archivo = st.file_uploader(
        "Suba archivo Excel",
        type=["xlsx"]
    )

    if archivo is not None:
        flujo_df = pd.read_excel(
            archivo,
            sheet_name=0,
            header=None
        )

        dist_df = pd.read_excel(
            archivo,
            sheet_name=1,
            header=None
        )

        mflujo = preparar_matriz(flujo_df.values.tolist())
        mdist = preparar_matriz(dist_df.values.tolist())

elif modo == "Subir archivos CSV":
    st.header("Carga desde CSV")

    st.info(
        """
        Formato requerido:

        - Archivo CSV 1: matriz de flujo.
        - Archivo CSV 2: matriz de distancia.
        - La diagonal principal será ajustada automáticamente a 0.
        """
    )

    flujo_csv = st.file_uploader(
        "Suba CSV de flujo",
        type=["csv"]
    )

    dist_csv = st.file_uploader(
        "Suba CSV de distancia",
        type=["csv"]
    )

    if flujo_csv is not None and dist_csv is not None:
        flujo_df = pd.read_csv(
            flujo_csv,
            header=None
        )

        dist_df = pd.read_csv(
            dist_csv,
            header=None
        )

        mflujo = preparar_matriz(flujo_df.values.tolist())
        mdist = preparar_matriz(dist_df.values.tolist())

st.divider()

metodo = st.selectbox(
    "Método de construcción:",
    [
        "Mayor flujo - menor costo",
        "Aleatorio"
    ]
)

if mflujo is not None and mdist is not None:
    st.subheader("Matrices cargadas")

    col1, col2 = st.columns(2)

    with col1:
        st.write("Matriz de flujo")
        st.dataframe(pd.DataFrame(mflujo))

    with col2:
        st.write("Matriz de distancia")
        st.dataframe(pd.DataFrame(mdist))

    if st.button("Ejecutar QAP"):
        ejecutar_qap(mflujo, mdist, metodo)