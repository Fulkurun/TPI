import sqlite3

class Libreria:
    def __init__(self):
        self.conexion = Conexiones()
        self.conexion.abrirConexion()
        self.conexion.miCursor.execute("DROP TABLE IF EXISTS LIBROS")
        self.conexion.miCursor.execute("CREATE TABLE LIBROS (id_libro INTEGER PRIMARY KEY AUTOINCREMENT, isbn VARCHAR(30) UNIQUE, titulo VARCHAR(30), autor VARCHAR(30), genero VARCHAR(30), precio FLOAT NOT NULL, fecha_ultimo_precio DATE, cant_disponible INTEGER NOT NULL)")
        self.conexion.miCursor.execute("DROP TABLE IF EXISTS VENTAS")
        self.conexion.miCursor.execute("CREATE TABLE VENTAS (id_venta INTEGER PRIMARY KEY, id_libro INTEGER NOT NULL, cantidad INTEGER NOT NULL, fecha DATE NOT NULL)")
        self.conexion.miCursor.execute("DROP TABLE IF EXISTS HISTORICO_LIBROS")
        self.conexion.miCursor.execute("CREATE TABLE HISTORICO_LIBROS (id_libro INTEGER, titulo VARCHAR(30), autor VARCHAR(30), precio_historico FLOAT NOT NULL, fecha_historico DATE NOT NULL, FOREIGN KEY(id_libro) REFERENCES LIBROS(id_libro))")
        self.conexion.miConexion.commit()
    
    def agregar_libro(self):
        try:
            isbn = input("Por favor ingrese el ISBN del libro: ")
            titulo = input("Por favor ingrese el título del libro: ")
            autor = input("Por favor ingrese el autor del libro: ")
            genero = input("Por favor ingrese el género del libro: ")
            precio = float(input("Por favor ingrese el precio del libro: "))
            fecha_ultimo_precio = input("Por favor ingrese la fecha del último precio (YYYY-MM-DD): ")
            cant_disponible = int(input("Por favor ingrese la cantidad disponible del libro: "))

            self.conexion.miCursor.execute("INSERT INTO LIBROS (isbn, titulo, autor, genero, precio, fecha_ultimo_precio, cant_disponible) VALUES (?, ?, ?, ?, ?, ?, ?)", (isbn, titulo, autor, genero, precio, fecha_ultimo_precio, cant_disponible))
            self.conexion.miConexion.commit()
            print("Libro agregado exitosamente")
        except:
            print("Error al agregar un libro")
    
    def modificar_precio(self, id_libro, nuevo_precio):
        try:
            confirmacion = input("¿Está seguro de que desea modificar el precio del libro? (s/n): ")
            if confirmacion.lower() == "s":
                self.conexion.miCursor.execute("SELECT * FROM LIBROS WHERE id_libro = ?", (id_libro,))
                libro = self.conexion.miCursor.fetchone()
                if libro:
                    self.conexion.miCursor.execute("INSERT INTO HISTORICO_LIBROS (id_libro, titulo, autor, precio_historico, fecha_historico) VALUES (?, ?, ?, ?, date('now'))",
                                                (libro[0], libro[2], libro[3], libro[5]))
                    self.conexion.miCursor.execute("UPDATE LIBROS SET precio = ? WHERE id_libro = ?", (nuevo_precio, id_libro))
                    self.conexion.miConexion.commit()
                    print("Libro modificado correctamente")
                else:
                    print("No se encontró un libro con el ID especificado")
            else:
                print("Operación cancelada")
        except:
            print("Error al modificar un libro")
    
    def incrementar_cantidad_disponible(self, id_libro, cantidad):
        try:
            self.conexion.miCursor.execute("UPDATE LIBROS SET cant_disponible = cant_disponible + ? WHERE id_libro = ?", (cantidad, id_libro))
            self.conexion.miConexion.commit()
            print("Cantidad disponible incrementada exitosamente")
        except:
            print("Error al incrementar la cantidad disponible")
    
    def eliminar_libro(self, titulo, autor):
        try:
            self.conexion.miCursor.execute("DELETE FROM LIBROS WHERE titulo = ? AND autor = ?", (titulo, autor))
            self.conexion.miConexion.commit()
            print("Libro eliminado correctamente")
        except:
            print("Error al eliminar un libro")
    
    def registrar_venta(self, id_libro, cantidad, fecha):
        try:
            self.conexion.miCursor.execute("INSERT INTO VENTAS (id_libro, cantidad, fecha) VALUES (?, ?, ?)", (id_libro, cantidad, fecha))
            self.conexion.miConexion.commit()

            self.conexion.miCursor.execute("UPDATE LIBROS SET cant_disponible = cant_disponible - ? WHERE id_libro = ?", (cantidad, id_libro))
            self.conexion.miConexion.commit()

            print("Venta registrada exitosamente")
        except:
            print("Error al registrar la venta")
    
    def actualizar_precios(self, porcentaje):
        try:
            self.conexion.miCursor.execute("SELECT id_libro, titulo, autor, precio FROM LIBROS")
            libros = self.conexion.miCursor.fetchall()

            for libro in libros:
                id_libro, titulo, autor, precio = libro
                precio_historico = precio 

                nuevo_precio = precio * (1 + porcentaje / 100)

                self.conexion.miCursor.execute("INSERT INTO HISTORICO_LIBROS (id_libro, titulo, autor, precio_historico, fecha_historico) VALUES (?, ?, ?, ?, date('now'))",
                                               (id_libro, titulo, autor, precio_historico))
                self.conexion.miCursor.execute("UPDATE LIBROS SET precio = ? WHERE id_libro = ?", (nuevo_precio, id_libro))
                self.conexion.miConexion.commit()

            print("Precios actualizados exitosamente")
        except:
            print("Error al actualizar los precios")
    def mostrar_libros_ordenados(self):
        try:
            self.conexion.miCursor.execute("SELECT * FROM LIBROS ORDER BY id_libro, autor, titulo")
            libros = self.conexion.miCursor.fetchall()

            print("Listado de libros:")
            for libro in libros:
                print(libro)
        except:
            print("Error al mostrar los libros")
    def mostrar_registros_antiguos(self, fecha):
        try:
            self.conexion.miCursor.execute("SELECT * FROM LIBROS WHERE id_libro IN (SELECT id_libro FROM HISTORICO_LIBROS WHERE fecha_historico < ?)", (fecha,))
            registros = self.conexion.miCursor.fetchall()

            print("Registros antiguos anteriores a la fecha:", fecha)
            for registro in registros:
                print(registro)
        except:
            print("Error al mostrar los registros antiguos")
    
    def cerrar_libreria(self):
        self.conexion.cerrarConexion()

class Conexiones:
    def abrirConexion(self):
        self.miConexion = sqlite3.connect("Libreria.db")
        self.miCursor = self.miConexion.cursor()
        
    def cerrarConexion(self):
        self.miConexion.close()  


libreria = Libreria()

while True:
    print("Menu de opciones Libreria")
    print("1- Agregar libro")
    print("2- Modificar precio de un libro")
    print("3- Incrementar cantidad disponible de un libro")
    print("4- Eliminar libro")
    print("5- Mostrar todos los libros ordenados por ID, Autor y Título")
    print("6- Registrar venta")
    print("7- Actualizar precios")
    print("8- Mostrar registros antiguos")
    print("0- Cerrar librería")
    
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        libreria.agregar_libro()
    elif opcion == "2":
        id_libro = int(input("Ingrese el ID del libro: "))
        nuevo_precio = float(input("Ingrese el nuevo precio: "))
        libreria.modificar_precio(id_libro, nuevo_precio)
    elif opcion == "3":
        id_libro = int(input("Ingrese el ID del libro: "))
        cantidad = int(input("Ingrese la cantidad a incrementar: "))
        libreria.incrementar_cantidad_disponible(id_libro, cantidad)
    elif opcion == "4":
        titulo = input("Ingrese el título del libro: ")
        autor = input("Ingrese el autor del libro: ")
        libreria.eliminar_libro(titulo, autor)
    elif opcion == "5":
        libreria.mostrar_libros_ordenados()
    elif opcion == "6":
        id_libro = int(input("Ingrese el ID del libro: "))
        cantidad = int(input("Ingrese la cantidad vendida: "))
        fecha = input("Ingrese la fecha de la venta (YYYY-MM-DD): ")
        libreria.registrar_venta(id_libro, cantidad, fecha)
    elif opcion == "7":
        porcentaje = float(input("Ingrese el porcentaje de aumento de precios: "))
        libreria.actualizar_precios(porcentaje)
    elif opcion == "8":
        fecha = input("Ingrese la fecha límite para los registros antiguos (YYYY-MM-DD): ")
        libreria.mostrar_registros_antiguos(fecha)
    elif opcion == "0":
        libreria.cerrar_libreria()
        break
    else:
        print("Opción inválida. Por favor seleccione una opción válida.")
