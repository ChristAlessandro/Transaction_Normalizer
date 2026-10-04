from src.normalizer import (
    detectar_fuente,
    normalizar_monto,
    normalizar_moneda,
    normalizar_estado,
    normalizar_fecha
)


def test_detectar_source_1():
    transaccion = {
        "id": "tx_001",
        "amount": "100.50",
        "currency": "USD",
        "timestamp": "2025-03-10 14:22:00",
        "status": "completed"
    }

    reglas = {
        "source_formats": {
            "source_1": [
                "id",
                "amount",
                "currency",
                "timestamp",
                "status"
            ]
        }
    }

    assert detectar_fuente(transaccion, reglas) == "source_1"


def test_normalizar_monto_source_1():
    assert normalizar_monto("100.50", "source_1") == 100.50


def test_normalizar_monto_source_2():
    assert normalizar_monto(10050, "source_2") == 100.50


def test_normalizar_monto_source_3():
    assert normalizar_monto("€99,99", "source_3") == 99.99


def test_normalizar_moneda():
    assert normalizar_moneda("usd") == "USD"
    assert normalizar_moneda("eur") == "EUR"


def test_normalizar_estado():
    reglas = {
        "status_mapping": {
            "completed": "SUCCESS",
            "success": "SUCCESS",
            "ok": "SUCCESS",
            "failed": "FAILED",
            "error": "FAILED",
            "pending": "PENDING"
        }
    }

    assert normalizar_estado("completed", reglas) == "SUCCESS"
    assert normalizar_estado("failed", reglas) == "FAILED"
    assert normalizar_estado("pending", reglas) == "PENDING"


def test_normalizar_fecha():
    formatos = [
        "%Y-%m-%d %H:%M:%S",
        "%d/%m/%Y %H:%M",
        "%Y-%m-%dT%H:%M:%SZ"
    ]

    resultado = normalizar_fecha(
        "2025-03-10 14:22:00",
        formatos
    )

    assert resultado == "2025-03-10T14:22:00Z"