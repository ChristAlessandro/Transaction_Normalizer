from src.metrics import calcular_metricas


def test_calcular_metricas():

    transacciones = [
        {
            "id": "1",
            "amount": 100.50,
            "currency": "USD",
            "timestamp": "2025-03-10T14:22:00Z",
            "status": "SUCCESS",
            "source": "source_1"
        },
        {
            "id": "2",
            "amount": 25.00,
            "currency": "USD",
            "timestamp": "2025-03-10T15:00:00Z",
            "status": "FAILED",
            "source": "source_2"
        },
        {
            "id": "3",
            "amount": 99.99,
            "currency": "EUR",
            "timestamp": "2025-03-10T16:00:00Z",
            "status": "SUCCESS",
            "source": "source_3"
        }
    ]

    invalidas = [
        {
            "data": {
                "id": "4"
            },
            "reasons": [
                "Moneda no soportada: GBP"
            ]
        }
    ]

    resultado = calcular_metricas(
        transacciones,
        invalidas
    )

    assert resultado["total_procesadas"] == 4
    assert resultado["total_validas"] == 3
    assert resultado["total_invalidas"] == 1

    assert resultado["porcentaje_validas"] == 75.0
    assert resultado["porcentaje_invalidas"] == 25.0

    assert resultado["por_estado"]["SUCCESS"] == 2
    assert resultado["por_estado"]["FAILED"] == 1

    assert resultado["totales_por_moneda"]["USD"] == 125.50
    assert resultado["totales_por_moneda"]["EUR"] == 99.99