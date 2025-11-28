class tools:
  def generar_df_info(fechaVenta, ifExists):
    import pandas as pd
    import sqlite3 as sql
    import random as r
    listaInsumosProductos = [
        "Cuaderno profesional", "Cuaderno doble raya", "Lápiz del número 2", "Pluma azul",
        "Pluma negra", "Pluma roja", "Marcador permanente", "Marcador para pizarrón",
        "Resaltador amarillo", "Resaltador verde", "Resaltador rosa", "Goma de borrar",
        "Sacapuntas", "Tijeras escolares", "Tijeras de oficina", "Regla de 30 cm",
        "Compás metálico", "Juego de geometría", "Pegamento en barra", "Pegamento líquido",
        "Cinta adhesiva", "Corrector líquido", "Corrector en cinta", "Carpeta tamaño carta",
        "Carpeta tamaño oficio", "Separadores de plástico", "Hojas blancas tamaño carta",
        "Hojas recicladas", "Hojas cuadriculadas", "Post-it", "Bloc de notas",
        "Engrapadora", "Caja de grapas", "Clips metálicos", "Broches tipo baco",
        "Folder manila", "Folder plástico con broche", "Archivador", "Tóner para impresora",
        "Cartuchos de tinta", "Calculadora científica", "Calculadora básica", "Memoria USB",
        "Mouse inalámbrico", "Teclado", "Agenda anual", "Calendario de escritorio",
        "Papel fotográfico", "Papel bond", "Cinta doble cara", "Pega diamantina"
    ]
    listaInsumosCajeros = [
        "Juan Carlos Ramírez López", "Miguel Ángel Torres Hernández", "José Luis González Cruz",
        "Carlos Alberto Mendoza Pérez", "Luis Fernando Ortega Díaz",
        "María Fernanda Castillo Reyes", "Ana Sofía Morales García", "Valeria Jiménez Flores",
        "Diana Carolina Salazar Ruiz", "Paola Alejandra Vargas León"
    ]
    listaInsumosSucursales = [
        "Centro Histórico", "Polanco", "Santa Fe", "Coyoacán", "Cuemanco",
        "Tlalpan", "Xochimilco", "La Condesa", "Reforma", "San Ángel"
    ]
    listaInsumosAbecedario = [
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
        "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
        "U", "V", "W", "X", "Y", "Z"
    ]


    ####################################################
    # Zona de definicion de listas vacías
    ####################################################
    listaInsumoV_fecha = []
    listaInsumoV_cajero = []
    listaInsumoV_producto = []
    listaInsumoV_precio = []
    listaInsumoV_cantidad = []
    listaInsumoV_total = []
    listaInsumoV_clave = []
    listaInsumoV_sucursal = []

    for i in range(1, r.randint(1000, 35001)):
      ####################################################
      # Zona de definicion de variables
      ####################################################

      cajero = r.choice(listaInsumosCajeros)
      producto = r.choice(listaInsumosProductos)
      precio = round(r.randint(10, 20000) * r.random(), 2)
      cantidad = r.randint(1, 100)
      total = round(precio * cantidad, 2)
      clave = f"{r.choice(listaInsumosAbecedario)}{r.choice(listaInsumosAbecedario)}{r.choice(listaInsumosAbecedario)}-{r.randint(100, 999)}"
      sucursal = r.choice(listaInsumosSucursales)

      ####################################################
      # Zona de alimentacion de las listas
      ####################################################
      listaInsumoV_fecha.append(fechaVenta)
      listaInsumoV_cajero.append(cajero)
      listaInsumoV_producto.append(producto)
      listaInsumoV_precio.append(precio)
      listaInsumoV_cantidad.append(cantidad)
      listaInsumoV_total.append(total)
      listaInsumoV_clave.append(clave)
      listaInsumoV_sucursal.append(sucursal)

    dictPrevio = {
      "ColFecha": listaInsumoV_fecha,
      "ColCajero": listaInsumoV_cajero,
      "ColProducto": listaInsumoV_producto,
      "ColPrecio": listaInsumoV_precio,
      "ColCantidad": listaInsumoV_cantidad,
      "ColTotal": listaInsumoV_total,
      "ColClave": listaInsumoV_clave,
      "ColSucursal": listaInsumoV_sucursal
    }

    df_ventas = pd.DataFrame(dictPrevio)
    print(f"Dataframe generado con éxito al {fechaVenta}")

    ####################################################
    # Zona de alimentacion de la base de datos
    ####################################################

    conexion = sql.connect("Ventas.db")
    df_ventas.to_sql("Ventas_2025", conexion, if_exists=ifExists)
    conexion.close()
    print(f"Base de datos alimentada al {fechaVenta}")

  #_______________________________________________________________________________
  def consulta(query):
    import pandas as pd
    import sqlite3 as sql
    import random as r

    conexion = sql.connect("Ventas.db")
    df_consulta = pd.read_sql_query(query, conexion)
    conexion.close()
    return df_consulta

  #_______________________________________________________________________________

  def generar_df_info_rango(fechaInicial, fechaFinal):
    import pandas as pd
    import sqlite3 as sql
    import random as r
    ##################################################################################
    def rangoFecha(fechaInicial, fechaFinal):
      import pandas as pd
      import sqlite3 as sql
      import random as r

      rangoObjetosFecha = pd.date_range(start=fechaInicial, end=fechaFinal, freq="1d")
      rangoStrFecha = []
      for objFecha in rangoObjetosFecha:
        strFecha = dt.datetime.strftime(objFecha, "%Y-%m-%d")
        rangoStrFecha.append(strFecha)
      return rangoStrFecha
    ##################################################################################

    rango_fechas = rangoFecha(fechaInicial, fechaFinal)
    for fechaVenta in rango_fechas:
      tools.generar_df_info(fechaVenta, "append")
    print(f"Se generó con éxito las ventas del {fechaInicial} al {fechaFinal}")
