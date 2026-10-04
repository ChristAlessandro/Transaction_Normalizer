# Transaction Normalizer

Sistema desarrollado en Python para normalizar y explorar transacciones provenientes de diferentes fuentes con estructuras heterogéneas.

El proyecto identifica el formato de origen de cada transacción, transforma los datos a un modelo común, valida la información y genera métricas para su exploración mediante una interfaz CLI.

## Objetivo

Procesar transacciones provenientes de diferentes fuentes y convertirlas a una estructura normalizada:

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

## Tecnologías

* Python 3
* pytest
* Flask
* JSON
* Git / GitHub

## Estructura del proyecto

```text
Transaction_Normalizer/
│
├── config/
│   └── rules.json
│
├── data/
│   ├── transactions_valid.json
│   └── transactions_invalid.json
│
├── docs/
│   └── nota_tecnica.md
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── normalizer.py
│   ├── validator.py
│   ├── metrics.py
│   ├── cli.py
│   └── web.py
│
├── tests/
│   ├── __init__.py
│   ├── test_normalizer.py
│   ├── test_validator.py
│   └── test_metrics.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

## Reglas de normalización

Las reglas principales se encuentran en:

```text
config/rules.json
```

### Fuentes soportadas

#### Source 1

```text
id
amount
currency
timestamp
status
```

#### Source 2

```text
transaction_id
total
currency_code
created_at
state
```

#### Source 3

```text
ref
amount
date
result
```

### Conversión de montos

* Source 1: el monto se convierte directamente a número decimal.
* Source 2: `total` se interpreta como centavos.
* Source 3: se elimina el símbolo `€` y la coma decimal se convierte en punto.

Ejemplos:

```text
10050 → 100.50 USD
€99,99 → 99.99 EUR
```

No se realiza conversión entre monedas.

### Monedas

Las monedas soportadas son:

```text
USD
EUR
```

Los códigos de moneda se normalizan a mayúsculas.

### Estados

Los estados provenientes de las diferentes fuentes se convierten a:

```text
SUCCESS
FAILED
PENDING
```

Mapeo:

```text
completed → SUCCESS
success   → SUCCESS
ok        → SUCCESS
failed    → FAILED
error     → FAILED
pending   → PENDING
```

### Fechas

Se aceptan los siguientes formatos:

```text
YYYY-MM-DD HH:MM:SS
DD/MM/YYYY HH:MM
YYYY-MM-DDTHH:MM:SSZ
```

Todas las fechas se convierten a formato ISO-8601 UTC.

## Tratamiento de datos inválidos

Las transacciones inválidas no se eliminan.

Se conservan junto con la razón por la que no pudieron ser procesadas.

Entre los posibles errores se encuentran:

* ID faltante.
* Monto inválido.
* Moneda no soportada.
* Fecha inválida.
* Estado no reconocido.
* Fuente no identificada.

Esto permite analizar posteriormente los datos problemáticos sin perder la información original.

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/ChristAlessandro/Transaction_Normalizer.git
```

Entrar al proyecto:

```bash
cd Transaction_Normalizer
```

Crear el entorno virtual:

```bash
python -m venv .venv
```

Activar el entorno virtual en Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Instalar las dependencias:

```powershell
pip install -r requirements.txt
```

## Ejecución

Ejecutar el programa desde la raíz del proyecto:

```powershell
python src/main.py
```

El sistema mostrará un menú interactivo:

```text
========================================
     TRANSACTION NORMALIZER
========================================

1. Listar transacciones
2. Filtrar por estado
3. Filtrar por moneda
4. Ver transacciones inválidas
5. Ver métricas
6. Salir
```

### Opciones disponibles

#### 1. Listar transacciones

Muestra todas las transacciones que fueron normalizadas correctamente.

#### 2. Filtrar por estado

Permite consultar transacciones según su estado:

```text
SUCCESS
FAILED
PENDING
```

#### 3. Filtrar por moneda

Permite consultar transacciones por moneda:

```text
USD
EUR
```

#### 4. Ver transacciones inválidas

Muestra las transacciones que no pudieron ser normalizadas o validadas correctamente.

#### 5. Ver métricas

Muestra información como:

* Total de transacciones procesadas.
* Total de transacciones válidas.
* Total de transacciones inválidas.
* Porcentaje de transacciones válidas.
* Porcentaje de transacciones inválidas.
* Cantidad de transacciones por estado.
* Totales monetarios por moneda.

#### 6. Salir

Finaliza la ejecución del programa.

## Pruebas

Para ejecutar las pruebas automatizadas:

```powershell
pytest -v
```

Las pruebas verifican principalmente:

* Detección de fuentes.
* Conversión de montos.
* Normalización de monedas.
* Normalización de estados.
* Conversión de fechas.
* Validación de transacciones.
* Detección de datos inválidos.
* Cálculo de métricas.

## Datos de prueba

El proyecto incluye dos conjuntos de datos:

```text
data/transactions_valid.json
data/transactions_invalid.json
```

Los archivos contienen ejemplos de diferentes fuentes y casos inconsistentes para comprobar el comportamiento del sistema.

Las transacciones del archivo `transactions_invalid.json` representan casos que pueden contener errores como monedas no soportadas, montos inválidos, fechas imposibles, estados desconocidos o estructuras no identificadas.

## Arquitectura

El proyecto separa las responsabilidades principales en diferentes módulos.

### normalizer.py

Se encarga de:

* Detectar la fuente de una transacción.
* Obtener los campos correspondientes.
* Normalizar montos.
* Normalizar monedas.
* Normalizar estados.
* Convertir fechas.
* Generar el modelo común.

### validator.py

Se encarga de validar:

* ID.
* Monto.
* Moneda.
* Fecha.
* Estado.
* Fuente.

### metrics.py

Se encarga de calcular:

* Total procesado.
* Transacciones válidas.
* Transacciones inválidas.
* Porcentajes.
* Cantidad por estado.
* Totales por moneda.

### cli.py

Contiene la interfaz interactiva de línea de comandos que permite explorar y filtrar la información procesada.

### main.py

Coordina la carga de datos, normalización, validación, generación de métricas e inicio de la interfaz CLI.

### rules.json

Contiene las reglas configurables utilizadas por el sistema para:

* Monedas soportadas.
* Mapeo de estados.
* Formatos de fecha.
* Estructuras de las fuentes.

## Uso de inteligencia artificial

La inteligencia artificial fue utilizada como herramienta de apoyo durante el desarrollo del proyecto y no como autora de las decisiones principales.

Se utilizó IA para:

* Proponer estructuras iniciales de funciones.
* Apoyar en la implementación de lógica de parsing y validación.
* Detectar y solucionar errores durante el desarrollo.
* Apoyar en la creación de pruebas automatizadas.
* Revisar posibles mejoras en la organización del código.

Las decisiones finales sobre el modelo normalizado, las reglas de transformación, las monedas soportadas, el mapeo de estados, los formatos de fecha y los criterios para considerar una transacción válida fueron definidas y revisadas manualmente.

Durante el desarrollo también se realizaron ajustes al código generado inicialmente para adaptarlo al funcionamiento real del proyecto, corregir errores de importación y asegurar que las pruebas automatizadas funcionaran correctamente.

## Decisiones de diseño

El proyecto utiliza un modelo común para evitar que cada fuente tenga que ser procesada de manera independiente durante la exploración de los datos.

Las transacciones válidas se convierten al mismo esquema:

```json
{
    "id": "string",
    "amount": 99.99,
    "currency": "USD",
    "timestamp": "2025-03-10T14:22:00Z",
    "status": "SUCCESS",
    "source": "source_1"
}
```

Las transacciones inválidas no se descartan, ya que conservarlas permite identificar problemas en los datos de origen y analizar posteriormente las causas de los errores.

No se realiza conversión de divisas, debido a que el objetivo del proyecto es la normalización estructural y no la conversión monetaria.

## Repositorio

El código fuente del proyecto se encuentra disponible en GitHub:

[https://github.com/ChristAlessandro/Transaction_Normalizer](https://github.com/ChristAlessandro/Transaction_Normalizer)

## Autor

Proyecto académico individual.

Desarrollado utilizando Python y Git/GitHub.