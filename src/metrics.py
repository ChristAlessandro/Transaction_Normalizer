from collections import Counter, defaultdict


def calcular_metricas(transacciones, invalidas):
    """
    Calcula las métricas principales del procesamiento.
    """

    total_validas = len(transacciones)
    total_invalidas = len(invalidas)
    total_procesadas = total_validas + total_invalidas

    estados = Counter()
    totales_moneda = defaultdict(float)

    for transaccion in transacciones:
        estados[transaccion["status"]] += 1
        totales_moneda[transaccion["currency"]] += transaccion["amount"]

    return {
        "total_procesadas": total_procesadas,
        "total_validas": total_validas,
        "total_invalidas": total_invalidas,
        "porcentaje_validas": calcular_porcentaje(
            total_validas,
            total_procesadas
        ),
        "porcentaje_invalidas": calcular_porcentaje(
            total_invalidas,
            total_procesadas
        ),
        "por_estado": dict(estados),
        "totales_por_moneda": {
            moneda: round(total, 2)
            for moneda, total in totales_moneda.items()
        }
    }


def calcular_porcentaje(valor, total):
    """
    Calcula un porcentaje evitando división entre cero.
    """

    if total == 0:
        return 0.0

    return round((valor / total) * 100, 2)