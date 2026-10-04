# Nota técnica

## 1. Objetivo del proyecto

El proyecto **Transaction Normalizer** tiene como objetivo procesar transacciones provenientes de diferentes fuentes con estructuras heterogéneas, transformarlas a un modelo común, validar su información y generar métricas que permitan explorar los resultados.

La solución fue desarrollada en Python y utiliza una interfaz CLI para que el usuario pueda consultar las transacciones normalizadas, aplicar filtros y visualizar métricas.

## 2. Diseño y modelo normalizado

Se definió un modelo común para todas las transacciones:

```json
{
    "id": "string",
    "amount": 99.99,
    "currency": "USD",
    "timestamp": "2025-03-10T14:22:00Z",
    "status": "SUCCESS",
    "source": "source_1"
}
````

El campo `source` permite conservar la procedencia de cada transacción después de la normalización.

El proyecto separa responsabilidades en los módulos `normalizer.py`, `validator.py`, `metrics.py`, `cli.py` y `main.py`.

## 3. Reglas de normalización

Se definieron tres formatos de entrada:

* `source_1`: utiliza `id`, `amount`, `currency`, `timestamp` y `status`.
* `source_2`: utiliza `transaction_id`, `total`, `currency_code`, `created_at` y `state`.
* `source_3`: utiliza `ref`, `amount`, `date` y `result`.

Los montos se transforman según su fuente. En `source_2`, el campo `total` representa centavos, mientras que en `source_3` se elimina el símbolo `€` y se convierte la coma decimal a punto.

Las monedas soportadas son `USD` y `EUR`.

Los diferentes estados de las fuentes se transforman a los estados estándar `SUCCESS`, `FAILED` y `PENDING`.

Las fechas admiten tres formatos de entrada y son convertidas a ISO-8601 UTC.

No se realiza conversión de divisas, debido a que el objetivo es normalizar la estructura de los datos y no realizar conversiones monetarias.

## 4. Validación y datos inválidos

Una transacción es considerada válida cuando posee un identificador, monto válido, moneda soportada, fecha válida, estado reconocido y una fuente identificable.

Las transacciones inválidas no son eliminadas. Se conservan para poder identificar y analizar los problemas presentes en los datos originales.

## 5. Métricas e interfaz

El sistema calcula el total de transacciones procesadas, cantidad y porcentaje de válidas e inválidas, cantidad por estado y totales por moneda.

La interfaz CLI permite listar transacciones, filtrarlas por estado o moneda, consultar transacciones inválidas y visualizar las métricas obtenidas.

## 6. Uso de inteligencia artificial

La inteligencia artificial fue utilizada como herramienta de apoyo durante el desarrollo para proponer estructuras iniciales, apoyar en la implementación de lógica de parsing y validación, generar pruebas y ayudar a identificar errores.

Las decisiones principales no fueron delegadas a la IA. El modelo normalizado, las fuentes soportadas, reglas de conversión, monedas, estados, formatos de fecha y criterios de validez fueron definidos y revisados manualmente.

Durante el desarrollo se realizaron ajustes sobre las propuestas iniciales para adaptarlas al proyecto, solucionar errores de importación y verificar el funcionamiento mediante pruebas automatizadas.

## 7. Resultado

La solución permite integrar transacciones de diferentes estructuras en un modelo uniforme, conservar los datos inválidos para su análisis y proporcionar una interfaz sencilla para explorar los resultados.
