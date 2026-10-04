import json
import re
from datetime import datetime, timezone


def cargar_reglas(ruta_reglas):
    """
    Carga las reglas de normalización desde el archivo JSON.
    """
    with open(ruta_reglas, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def detectar_fuente(transaccion, reglas):
    """
    Determina la fuente de una transacción comparando sus campos
    con las estructuras definidas en rules.json.
    """

    for fuente, campos in reglas["source_formats"].items():
        if all(campo in transaccion for campo in campos):
            return fuente

    return "unknown"


def normalizar_moneda(moneda):
    """
    Convierte el código de moneda a mayúsculas.
    """
    if not isinstance(moneda, str):
        return None

    return moneda.strip().upper()


def normalizar_estado(estado, reglas):
    """
    Convierte los diferentes estados de las fuentes al estado estándar.
    """

    if not isinstance(estado, str):
        return None

    estado_normalizado = estado.strip().lower()

    return reglas["status_mapping"].get(estado_normalizado)


def normalizar_fecha(fecha, formatos):
    """
    Convierte una fecha de cualquiera de los formatos permitidos
    al formato ISO-8601 con UTC.
    """

    if not isinstance(fecha, str):
        return None

    fecha = fecha.strip()

    for formato in formatos:
        try:
            fecha_convertida = datetime.strptime(fecha, formato)

            # Los formatos sin zona horaria se interpretan como UTC.
            fecha_convertida = fecha_convertida.replace(tzinfo=timezone.utc)

            return fecha_convertida.strftime("%Y-%m-%dT%H:%M:%SZ")

        except ValueError:
            continue

    return None


def normalizar_monto(monto, fuente):
    """
    Convierte el monto a float siguiendo las reglas de cada fuente.
    """

    if fuente == "source_2":
        try:
            return float(monto) / 100
        except (ValueError, TypeError):
            return None

    if fuente == "source_3":
        if not isinstance(monto, str):
            return None

        monto = monto.strip()

        # Elimina el símbolo de euro.
        monto = monto.replace("€", "").strip()

        # Convierte la coma decimal en punto.
        monto = monto.replace(",", ".")

        try:
            return float(monto)
        except ValueError:
            return None

    try:
        return float(monto)
    except (ValueError, TypeError):
        return None


def obtener_campos(transaccion, fuente):
    """
    Obtiene los campos correspondientes a cada fuente.
    """

    if fuente == "source_1":
        return {
            "id": transaccion.get("id"),
            "amount": transaccion.get("amount"),
            "currency": transaccion.get("currency"),
            "timestamp": transaccion.get("timestamp"),
            "status": transaccion.get("status")
        }

    if fuente == "source_2":
        return {
            "id": transaccion.get("transaction_id"),
            "amount": transaccion.get("total"),
            "currency": transaccion.get("currency_code"),
            "timestamp": transaccion.get("created_at"),
            "status": transaccion.get("state")
        }

    if fuente == "source_3":
        return {
            "id": transaccion.get("ref"),
            "amount": transaccion.get("amount"),
            "currency": "EUR" if isinstance(
                transaccion.get("amount"), str
            ) and "€" in transaccion.get("amount") else None,
            "timestamp": transaccion.get("date"),
            "status": transaccion.get("result")
        }

    return None


def normalizar_transaccion(transaccion, reglas):
    """
    Normaliza una transacción individual.

    Retorna:
    - La transacción normalizada si es posible.
    - None si la fuente no puede ser identificada o existen
      datos que no pueden transformarse.
    """

    fuente = detectar_fuente(transaccion, reglas)

    if fuente == "unknown":
        return None

    campos = obtener_campos(transaccion, fuente)

    if campos is None:
        return None

    identificador = campos["id"]

    if identificador is None:
        return None

    identificador = str(identificador)

    monto = normalizar_monto(
        campos["amount"],
        fuente
    )

    if monto is None:
        return None

    moneda = normalizar_moneda(
        campos["currency"]
    )

    if moneda not in reglas["supported_currencies"]:
        return None

    fecha = normalizar_fecha(
        campos["timestamp"],
        reglas["date_formats"]
    )

    if fecha is None:
        return None

    estado = normalizar_estado(
        campos["status"],
        reglas
    )

    if estado is None:
        return None

    return {
        "id": identificador,
        "amount": round(monto, 2),
        "currency": moneda,
        "timestamp": fecha,
        "status": estado,
        "source": fuente
    }


def normalizar_transacciones(transacciones, reglas):
    """
    Normaliza una lista de transacciones.

    Retorna dos listas:
    - transacciones normalizadas
    - transacciones que no pudieron normalizarse
    """

    validas = []
    invalidas = []

    for transaccion in transacciones:
        resultado = normalizar_transaccion(
            transaccion,
            reglas
        )

        if resultado is not None:
            validas.append(resultado)
        else:
            invalidas.append(transaccion)

    return validas, invalidas