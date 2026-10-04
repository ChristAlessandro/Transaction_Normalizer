import json

from flask import Flask, render_template, request

from normalizer import cargar_reglas
from metrics import calcular_metricas
from main import cargar_datos, procesar_transacciones


app = Flask(
    __name__,
    template_folder="../templates"
)


RUTA_REGLAS = "config/rules.json"
RUTA_DATOS_VALIDOS = "data/transactions_valid.json"
RUTA_DATOS_INVALIDOS = "data/transactions_invalid.json"


def cargar_todas_las_transacciones():
    datos_validos = cargar_datos(RUTA_DATOS_VALIDOS)
    datos_invalidos = cargar_datos(RUTA_DATOS_INVALIDOS)

    return datos_validos + datos_invalidos


@app.route("/")
def inicio():
    reglas = cargar_reglas(RUTA_REGLAS)

    transacciones = cargar_todas_las_transacciones()

    validas, invalidas = procesar_transacciones(
        transacciones,
        reglas
    )

    filtro_status = request.args.get("status", "").upper()
    filtro_currency = request.args.get("currency", "").upper()

    transacciones_filtradas = validas

    if filtro_status:
        transacciones_filtradas = [
            transaccion
            for transaccion in transacciones_filtradas
            if transaccion["status"] == filtro_status
        ]

    if filtro_currency:
        transacciones_filtradas = [
            transaccion
            for transaccion in transacciones_filtradas
            if transaccion["currency"] == filtro_currency
        ]

    metricas = calcular_metricas(
        validas,
        invalidas
    )

    return render_template(
        "index.html",
        transacciones=transacciones_filtradas,
        invalidas=invalidas,
        metricas=metricas,
        filtro_status=filtro_status,
        filtro_currency=filtro_currency
    )


if __name__ == "__main__":
    app.run(
        debug=True
    )