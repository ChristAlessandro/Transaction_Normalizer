from metrics import calcular_metricas


def mostrar_encabezado(titulo):
    """
    Muestra un encabezado para las diferentes vistas del CLI.
    """

    print("\n" + "=" * 50)
    print(titulo.center(50))
    print("=" * 50)


def mostrar_transaccion(transaccion):
    """
    Muestra una transacción normalizada.
    """

    print(f"ID:         {transaccion['id']}")
    print(f"Monto:      {transaccion['amount']:.2f}")
    print(f"Moneda:     {transaccion['currency']}")
    print(f"Fecha:      {transaccion['timestamp']}")
    print(f"Estado:     {transaccion['status']}")
    print(f"Fuente:     {transaccion['source']}")
    print("-" * 50)


def listar_transacciones(transacciones):
    """
    Muestra todas las transacciones normalizadas.
    """

    mostrar_encabezado("TRANSACCIONES NORMALIZADAS")

    if not transacciones:
        print("No hay transacciones para mostrar.")
        return

    for transaccion in transacciones:
        mostrar_transaccion(transaccion)

    print(f"Total mostradas: {len(transacciones)}")


def filtrar_por_estado(transacciones):
    """
    Permite al usuario filtrar las transacciones por estado.
    """

    mostrar_encabezado("FILTRAR POR ESTADO")

    print("Estados disponibles:")
    print("1. SUCCESS")
    print("2. FAILED")
    print("3. PENDING")

    opcion = input("\nSeleccione un estado: ").strip()

    estados = {
        "1": "SUCCESS",
        "2": "FAILED",
        "3": "PENDING"
    }

    estado = estados.get(opcion)

    if estado is None:
        print("Opción inválida.")
        return

    resultados = [
        transaccion
        for transaccion in transacciones
        if transaccion["status"] == estado
    ]

    print(f"\nTransacciones con estado {estado}:")
    listar_transacciones(resultados)


def filtrar_por_moneda(transacciones):
    """
    Permite al usuario filtrar las transacciones por moneda.
    """

    mostrar_encabezado("FILTRAR POR MONEDA")

    print("Monedas disponibles:")
    print("1. USD")
    print("2. EUR")

    opcion = input("\nSeleccione una moneda: ").strip()

    monedas = {
        "1": "USD",
        "2": "EUR"
    }

    moneda = monedas.get(opcion)

    if moneda is None:
        print("Opción inválida.")
        return

    resultados = [
        transaccion
        for transaccion in transacciones
        if transaccion["currency"] == moneda
    ]

    print(f"\nTransacciones en {moneda}:")
    listar_transacciones(resultados)


def mostrar_invalidas(invalidas):
    """
    Muestra las transacciones inválidas junto con sus razones.
    """

    mostrar_encabezado("TRANSACCIONES INVÁLIDAS")

    if not invalidas:
        print("No existen transacciones inválidas.")
        return

    for indice, transaccion in enumerate(invalidas, start=1):

        print(f"Transacción inválida #{indice}")

        print("\nDatos originales:")
        print(transaccion["data"])

        print("\nMotivos:")

        for motivo in transaccion["reasons"]:
            print(f"  - {motivo}")

        print("-" * 50)

    print(f"Total inválidas: {len(invalidas)}")


def mostrar_metricas(transacciones, invalidas):
    """
    Muestra las métricas generales del procesamiento.
    """

    mostrar_encabezado("MÉTRICAS")

    metricas = calcular_metricas(
        transacciones,
        invalidas
    )

    print(
        f"Total procesadas: "
        f"{metricas['total_procesadas']}"
    )

    print(
        f"Total válidas: "
        f"{metricas['total_validas']}"
    )

    print(
        f"Total inválidas: "
        f"{metricas['total_invalidas']}"
    )

    print(
        f"Porcentaje válidas: "
        f"{metricas['porcentaje_validas']}%"
    )

    print(
        f"Porcentaje inválidas: "
        f"{metricas['porcentaje_invalidas']}%"
    )

    print("\nCantidad por estado:")

    for estado, cantidad in metricas["por_estado"].items():
        print(f"  {estado}: {cantidad}")

    print("\nTotales por moneda:")

    for moneda, total in metricas["totales_por_moneda"].items():
        print(f"  {moneda}: {total:.2f}")


def mostrar_menu():
    """
    Muestra el menú principal.
    """

    print("\n")
    print("=" * 50)
    print("          TRANSACTION NORMALIZER")
    print("=" * 50)

    print("1. Listar transacciones")
    print("2. Filtrar por estado")
    print("3. Filtrar por moneda")
    print("4. Ver transacciones inválidas")
    print("5. Ver métricas")
    print("6. Salir")

    print("=" * 50)


def iniciar_cli(transacciones, invalidas):
    """
    Inicia el menú interactivo de la aplicación.
    """

    while True:

        mostrar_menu()

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            listar_transacciones(transacciones)

        elif opcion == "2":
            filtrar_por_estado(transacciones)

        elif opcion == "3":
            filtrar_por_moneda(transacciones)

        elif opcion == "4":
            mostrar_invalidas(invalidas)

        elif opcion == "5":
            mostrar_metricas(
                transacciones,
                invalidas
            )

        elif opcion == "6":
            print("\nGracias por utilizar Transaction Normalizer.")
            break

        else:
            print("\nOpción inválida. Intente nuevamente.")