Tecnologías
Python 3
pytest
Flask
JSON
Git / GitHub
Estructura del proyecto
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
Reglas de normalización

Las reglas principales se encuentran en:

config/rules.json
Fuentes soportadas

Source 1

id
amount
currency
timestamp
status

Source 2

transaction_id
total
currency_code
created_at
state

Source 3

ref
amount
date
result
Conversión de montos
Source 1: el monto se convierte directamente a número decimal.
Source 2: total se interpreta como centavos.
Source 3: se elimina el símbolo € y la coma decimal se convierte en punto.

Ejemplo:

10050 → 100.50 USD
€99,99 → 99.99 EUR

No se realiza conversión entre monedas.

Monedas

Las monedas soportadas son:

USD
EUR

Los códigos se normalizan a mayúsculas.

Estados

Los estados de las diferentes fuentes se convierten a:

SUCCESS
FAILED
PENDING

Mapeo:

completed → SUCCESS
success   → SUCCESS
ok        → SUCCESS
failed    → FAILED
error     → FAILED
pending   → PENDING
Fechas

Se aceptan los siguientes formatos:

YYYY-MM-DD HH:MM:SS
DD/MM/YYYY HH:MM
YYYY-MM-DDTHH:MM:SSZ

Todas las fechas se convierten a ISO-8601 UTC.

Tratamiento de datos inválidos

Las transacciones inválidas no se eliminan.

Se conservan junto con la razón por la que no pudieron ser procesadas.

Entre los posibles errores se encuentran:

ID faltante.
Monto inválido.
Moneda no soportada.
Fecha inválida.
Estado no reconocido.
Fuente no identificada.

Esto permite analizar posteriormente los datos problemáticos.

Instalación

Clonar el repositorio:

git clone https://github.com/ChristAlessandro/Transaction_Normalizer.git

Entrar al proyecto:

cd Transaction_Normalizer

Crear el entorno virtual:

python -m venv .venv

Activar el entorno virtual en Windows PowerShell:

.venv\Scripts\Activate.ps1

Instalar dependencias:

pip install -r requirements.txt
Ejecución

Ejecutar el programa:

python src/main.py

El sistema mostrará un menú interactivo:

1. Listar transacciones
2. Filtrar por estado
3. Filtrar por moneda
4. Ver transacciones inválidas
5. Ver métricas
6. Salir
Pruebas

Para ejecutar las pruebas automatizadas:

pytest -v

Las pruebas verifican principalmente:

Detección de fuentes.
Conversión de montos.
Normalización de monedas.
Normalización de estados.
Conversión de fechas.
Validación de transacciones.
Detección de errores.
Cálculo de métricas.
Datos de prueba

El proyecto incluye dos conjuntos de datos:

data/transactions_valid.json
data/transactions_invalid.json

Los archivos contienen ejemplos de diferentes fuentes y casos inconsistentes para comprobar el comportamiento del sistema.

Uso de inteligencia artificial

La inteligencia artificial fue utilizada como herramienta de apoyo durante el desarrollo para:

Proponer estructuras iniciales de funciones.
Apoyar en la implementación de lógica de parsing y validación.
Detectar errores durante el desarrollo.
Apoyar en la creación de pruebas.

Las decisiones finales sobre el modelo normalizado, reglas de transformación, monedas soportadas, estados, formatos de fecha y criterios de validez fueron definidas antes de implementar la lógica y fueron posteriormente revisadas y validadas.

Autor

Proyecto académico individual.

Desarrollado utilizando Python y Git/GitHub.