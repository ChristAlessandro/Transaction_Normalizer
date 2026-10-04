def validar_id(transaccion):
    """
    Verifica que la transacción tenga un identificador.
    """
    if not transaccion.get("id"):
        return False, "ID faltante"

    return True, None


def validar_monto(transaccion):
    """
    Verifica que el monto sea numérico y no negativo.
    """
    monto = transaccion.get("amount")

    if not isinstance(monto, (int, float)):
        return False, "Monto inválido"

    if monto < 0:
        return False, "El monto no puede ser negativo"

    return True, None


def validar_moneda(transaccion, reglas):
    """
    Verifica que la moneda esté dentro de las monedas soportadas.
    """
    moneda = transaccion.get("currency")

    if moneda not in reglas["supported_currencies"]:
        return False, f"Moneda no soportada: {moneda}"

    return True, None


def validar_fecha(transaccion):
    """
    Verifica que exista una fecha normalizada en formato ISO-8601.
    """
    fecha = transaccion.get("timestamp")

    if not fecha:
        return False, "Fecha faltante o inválida"

    if not isinstance(fecha, str):
        return False, "Fecha inválida"

    if not fecha.endswith("Z"):
        return False, "Fecha no está en formato ISO-8601 UTC"

    return True, None


def validar_estado(transaccion):
    """
    Verifica que el estado pertenezca al conjunto normalizado.
    """
    estados_validos = {
        "SUCCESS",
        "FAILED",
        "PENDING"
    }

    estado = transaccion.get("status")

    if estado not in estados_validos:
        return False, f"Estado no reconocido: {estado}"

    return True, None


def validar_fuente(transaccion):
    """
    Verifica que exista una fuente identificable.
    """
    fuente = transaccion.get("source")

    if not fuente or fuente == "unknown":
        return False, "Fuente no identificada"

    return True, None


def validar_transaccion(transaccion, reglas):
    """
    Ejecuta todas las validaciones de una transacción.

    Retorna:
    {
        "valid": True/False,
        "reasons": []
    }
    """

    validaciones = [
        validar_id(transaccion),
        validar_monto(transaccion),
        validar_moneda(transaccion, reglas),
        validar_fecha(transaccion),
        validar_estado(transaccion),
        validar_fuente(transaccion)
    ]

    errores = []

    for es_valida, motivo in validaciones:
        if not es_valida:
            errores.append(motivo)

    return {
        "valid": len(errores) == 0,
        "reasons": errores
    }


def validar_transacciones(transacciones, reglas):
    """
    Valida una lista de transacciones y separa las válidas
    de las inválidas.

    Las transacciones inválidas conservan sus datos y
    agregan las razones del rechazo.
    """

    validas = []
    invalidas = []

    for transaccion in transacciones:
        resultado = validar_transaccion(
            transaccion,
            reglas
        )

        if resultado["valid"]:
            validas.append(transaccion)
        else:
            transaccion_invalida = {
                "data": transaccion,
                "reasons": resultado["reasons"]
            }

            invalidas.append(transaccion_invalida)

    return validas, invalidas