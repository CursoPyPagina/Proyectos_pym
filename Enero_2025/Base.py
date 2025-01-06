class tools:
    # Atributos de clase
    abcdario = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 
        'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 
        'U', 'V', 'W', 'X', 'Y', 'Z']

    papelerias = ['Xochimilco', 'Cuemanco', 'Coapa', 'Milpa Alta', 'CU', 'Zócalo', 
                  'Narvarte', 'Santa Fé', 'Polanco', 'Centro']

    lineas = ['Cuadernos', 'Libretas', 'Lápices', 'Plumones', 'Borradores', 'Sacapuntas',
             'Laptops', 'Tablets', 'Mochilas', 'Bolsas', 'Cajas', 'Pegamento', 'Tijeras',
             'Monitores', 'Teclados', 'Mouse', 'Audífonos', 'Cables', 'Cargadores', 'Baterías',
             'Pc', 'Uniformes', 'Pinturas', 'Pinceles', 'Papel', 'Cartulinas']

    def definiciones():
        """Funcion para crera la base de datos y la tabla que ocuparemos para
        almacenar la infomacion simulada de las ventas"""
        import sqlite3 as sql
        
        # Creamos la base de datos en caso de que no exista
        sql.connect("Ventas.db")

        # Creamos la tabla
        query_create = f"""
        CREATE TABLE Ventas_2024(
            PRODUCTO TEXT, 
            CLAVE_PRODUCTO TEXT, 
            PRECIO_VENTA REAL, 
            CANTIDAD_VENDIDO INT, 
            SUCURSAL TEXT, 
            FECHA TEXT
            )
        """

        # Creamos la base de datos, la cual se llamara Ejemplo
        conn = sql.connect("Ventas.db")

        # El siguiente cursor nos permitira ejecutar sentencias SQL
        cursor = conn.cursor()

        # Ejecutamos la consulta
        try:
            cursor.execute(query_create)

            # Gurdamos cambios
            conn.commit()
            print("Tabla creada con éxito")
        except sql.Error as e:
            print(f"Error: {e.args[0]}")

        # Siempre que abrimos una conexion a la base de datos, debemos cerrarla al finalizar
        conn.close()

    # Metodos
    def _generar_info(date):
        """Método para simular las ventas de las diferentes papelerías"""
        
        # Importacion de librerias que utilizaremos
        import random as r
        import pandas as pd

        # Establecemos una fecha de venta
        fecha_reporte = date

        # importamos los catalogos que tienen la asociacion
        # clave_producto--->nombre del producto
        df_claves = pd.read_excel('Catalogo_Claves.xlsx')
        # clave_producto--->precio del producto
        df_p = pd.read_excel('Catalogo_Precios.xlsx')
        
        productos = []
        claves_producto = []
        precios_venta = []
        cantidades_vendidas = []
        sucursal_producto = []

        # dados los dataframes, podemos regresar de nuevo a los diccionarios
        claves_p = df_p.set_index('DESCRIPCION').to_dict()['PRECIO']
        claves = df_claves.set_index('DESCRIPCION').to_dict()['CLAVE']

        # Simulacion de las 1000 ventas
        for i in range(r.randint(1000, 10000)):
            # Generamos informacion aleatoria para simular las ventas

            # Seleccionamos un producto aleatorio
            producto = r.choice(tools.lineas)

            # Por medio de nuestros catalogos, diccionario, podemos obtener
            precio_venta = claves_p[producto]
            clave_producto = claves[producto]

            # Simulamos la cantidad vendida
            cantidad = r.randint(0, 9)

            # Seleccionamos la sucursal
            sucursal = r.choice(tools.papelerias)

            # Agregamos la informacion a las listas
            productos.append(producto)
            claves_producto.append(clave_producto)
            precios_venta.append(precio_venta)
            cantidades_vendidas.append(cantidad)
            sucursal_producto.append(sucursal)

        # Definimos el diccionario para crear el dataframe
        diccionario_df = {'Producto': productos,
                          'Clave del producto': claves_producto,
                          'Precio de venta': precios_venta,
                          'Cantidad vendida': cantidades_vendidas,
                          'Sucursal': sucursal_producto}

        # Creamos el dataframe
        df = pd.DataFrame(diccionario_df)
        df['Fecha'] = fecha_reporte 
        columnas = ['PRODUCTO', 'CLAVE_PRODUCTO', 'PRECIO_VENTA', 'CANTIDAD_VENDIDO', 'SUCURSAL', 'FECHA']
        df.columns = columnas

        print(f"Generación exitosa al {date}")
        return df
    
    def _inserciones_mult(df):
        """Método para alimentar la tabla de la base de datos"""
        
        import random as r
        import pandas as pd
        import sqlite3 as sql
        
        # Generamos la informacion
        conn = sql.connect("Ventas.db")
        cursor = conn.cursor()

        for i in range(len(df)):
            query_insert = f"""
            INSERT INTO 
            Ventas_2024(PRODUCTO, CLAVE_PRODUCTO, PRECIO_VENTA, CANTIDAD_VENDIDO, SUCURSAL, FECHA)
            VALUES('{df.loc[i, "PRODUCTO"]}', '{df.loc[i, "CLAVE_PRODUCTO"]}', 
                    {df.loc[i, "PRECIO_VENTA"]}, {df.loc[i, "CANTIDAD_VENDIDO"]}, 
                   '{df.loc[i, "SUCURSAL"]}', '{df.loc[i, "FECHA"]}')
            """

            cursor.execute(query_insert)
            conn.commit()
        conn.close()
        
        print(f"Inserción existosa")
        
    def proceso(fecha_ini, fecha_fin=None):
        """Metodo en el cual simulamos la informacion de las ventas y adicionalmente realizamos
        las inserciones. Se podra generar informacion de un solo dia o informacion de 
        todo un rango de fechas."""

        import pandas as pd
        import time as t
        
        inicio_total = t.time()
        
        # Caso en el cual solo es una fecha en la cual se desea generar
        if fecha_fin is None:
            inicio = t.time()
            # generamos
            df = tools._generar_info(fecha_ini)
            # Insertamos
            tools._inserciones_mult(df)
            fin = t.time()
            
            print(f'Fecha: {fecha_ini} || Tiempo de ejecución: {round((fin - inicio) / 60, 2)} minutos')
        # Caso en el que se desea generar la infomracion de todo un rango de fechas
        else:
            # generamos el rango con pandas
            rango = pd.DataFrame(pd.date_range(fecha_ini, fecha_fin))
            # Convertimos el rango anterior a strings
            rango[0] = rango[0].apply(str).apply(lambda x: x[:10])

            for i in range(len(rango)):
                inicio = t.time()
                df = tools._generar_info((rango.iloc[i][0]))
                tools._inserciones_mult(df)
                fin = t.time()
                
                del df
                
                print(f'Fecha: {rango.iloc[i][0]} || Tiempo de ejecución: {round((fin - inicio) / 60, 2)} minutos')
                print("-" * 35)
            
        fin_total = t.time()
        
        if fecha_fin != None:
            print(f'Tiempo de ejecución total: {round((fin_total - inicio_total) / 60, 2)}')
            
    def comprobar_fechas():
        """Método para ver cuales fechas tenemos cargadas en la tabla"""
        import sqlite3 as sql
        import pandas as pd
    
        # Creamos la tabla
        query = """
        SELECT DISTINCT FECHA FROM Ventas_2024
        """
        
        # Creamos la base de datos, la cual se llamara Ejemplo
        conn = sql.connect("Ventas.db")

        # Ejecutamos la consulta
        try:
            df = pd.read_sql_query(query, conn)
            print(df)
        except sql.Error as e:
            print(f"Error: {e.args[0]}")

        # Siempre que abrimos una conexion a la base de datos, debemos cerrarla al finalizar
        conn.close()