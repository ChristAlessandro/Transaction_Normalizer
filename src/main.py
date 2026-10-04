import json

from normalizer import (
    cargar_reglas,
    normalizar_transaccion
)

from validator import validar_transaccion

from metrics import calcular_metricas

from cli import iniciar_cli


RUTA_REGLAS = "config/rules.json"
RUTA_DATOS_VALIDOS = "data/transactions_valid.json"
RUTA_DATOS_INVALIDOS = "data/transactions_invalid.json"


def cargar_datos(ruta):
    """
    Carga una lista de transacciones desde un archivo JSON.
    """

    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def procesar_transacciones(transacciones, reglas):
    """
    Procesa las transacciones siguiendo el flujo:

    1. Detectar y normalizar.
    2. Validar la transacción normalizada.
    3. Separar válidas e inválidas.
    4. Conservar el motivo de cada error.
    """

    validas = []
    invalidas = []

    for transaccion in transacciones:

        try:
            normalizada = normalizar_transaccion(
                transaccion,
                reglas
            )

            if normalizada is None:
                invalidas.append({
                    "data": transaccion,
                    "reasons": [
                        "No fue posible normalizar la transacción"
                    ]
                })

                continue

            resultado_validacion = validar_transaccion(
                normalizada,
                reglas
            )

            if resultado_validacion["valid"]:
                validas.append(normalizada)
            else:
                invalidas.append({
                    "data": transaccion,
                    "normalized_data": normalizada,
                    "reasons": resultado_validacion["reasons"]
                })

        except Exception as error:
            invalidas.append({
                "data": transaccion,
                "reasons": [
                    f"Error durante el procesamiento: {error}"
                ]
            })

    return validas, invalidas


def mostrar_resultado(validas, invalidas):
    """
    Muestra un resumen básico del procesamiento.
    """

    metricas = calcular_metricas(
        validas,
        invalidas
    )

    print("\n========================================")
    print("       RESULTADO DEL PROCESAMIENTO")
    print("========================================")

    print(
        f"Total procesadas: {metricas['total_procesadas']}"
    )

    print(
        f"Total válidas: {metricas['total_validas']}"
    )

    print(
        f"Total inválidas: {metricas['total_invalidas']}"
    )

    print(
        f"Porcentaje válidas: "
        f"{metricas['porcentaje_validas']}%"
    )

    print(
        f"Porcentaje inválidas: "
        f"{metricas['porcentaje_invalidas']}%"
    )

    print("\nPor estado:")

    for estado, cantidad in metricas["por_estado"].items():
        print(f"  {estado}: {cantidad}")

    print("\nTotales por moneda:")

    for moneda, total in metricas["totales_por_moneda"].items():
        print(f"  {moneda}: {total:.2f}")


def main():
    """
    Punto de entrada principal del programa.
    """

    reglas = cargar_reglas(RUTA_REGLAS)

    datos_validos = cargar_datos(
        RUTA_DATOS_VALIDOS
    )

    datos_invalidos = cargar_datos(
        RUTA_DATOS_INVALIDOS
    )

    todas_las_transacciones = (
        datos_validos + datos_invalidos
    )

    validas, invalidas = procesar_transacciones(
        todas_las_transacciones,
        reglas
    )

    mostrar_resultado(
        validas,
        invalidas
    )   

    iniciar_cli(
        validas,
        invalidas
    )


if __name__ == "__main__":
    main()