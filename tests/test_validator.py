from src.validator import validar_transaccion


def obtener_reglas():
    return {
        "supported_currencies": [
            "USD",
            "EUR"
        ]
    }


def obtener_transaccion_valida():
    return {
        "id": "tx_001",
        "amount": 100.50,
        "currency": "USD",
        "timestamp": "2025-03-10T14:22:00Z",
        "status": "SUCCESS",
        "source": "source_1"
    }


def test_transaccion_valida():
    resultado = validar_transaccion(
        obtener_transaccion_valida(),
        obtener_reglas()
    )

    assert resultado["valid"] is True
    assert resultado["reasons"] == []


def test_moneda_no_soportada():
    transaccion = obtener_transaccion_valida()
    transaccion["currency"] = "GBP"

    resultado = validar_transaccion(
        transaccion,
        obtener_reglas()
    )

    assert resultado["valid"] is False
    assert "Moneda no soportada: GBP" in resultado["reasons"]


def test_monto_invalido():
    transaccion = obtener_transaccion_valida()
    transaccion["amount"] = "abc"

    resultado = validar_transaccion(
        transaccion,
        obtener_reglas()
    )

    assert resultado["valid"] is False
    assert "Monto inválido" in resultado["reasons"]


def test_estado_invalido():
    transaccion = obtener_transaccion_valida()
    transaccion["status"] = "UNKNOWN"

    resultado = validar_transaccion(
        transaccion,
        obtener_reglas()
    )

    assert resultado["valid"] is False
    assert "Estado no reconocido: UNKNOWN" in resultado["reasons"]