import sqlite3

# ##############################################
# MODELO
# ##############################################

def conexion():
    con = sqlite3.connect("ferreteria.db")
    return con


def crear_tabla():
    con = conexion()
    cursor = con.cursor()
    sql = """CREATE TABLE IF NOT EXISTS ventas
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto varchar(20),
            cantidad int,
            precio_unit float,
            precio_total float,
            forma_pago varchar(20),
            tipo_cliente varchar(20))
            """
    cursor.execute(sql)
    con.commit()


def agregar(producto, cantidad, precio_unit, precio_total, forma_pago, tipo_cliente, tree, limpiar, actualizar_treeview):
    con = conexion()
    cursor = con.cursor()
    data = (producto, cantidad, precio_unit, precio_total, forma_pago, tipo_cliente)
    sql = "INSERT INTO ventas(producto, cantidad, precio_unit, precio_total, forma_pago, tipo_cliente) VALUES (?, ?, ?, ?, ?, ?)"
    cursor.execute(sql, data)
    con.commit()
    actualizar_treeview(tree)
    limpiar()
    return ("Venta", "Venta registrada")


def borrar(tree):
    valor = tree.selection()
    item = tree.item(valor)
    id = item['text']

    con = conexion()
    cursor = con.cursor()
    data = (id,)
    sql = "DELETE FROM ventas WHERE id = ?"
    cursor.execute(sql, data)
    con.commit()
    tree.delete(valor)
    return("Venta", "Registro borrado")


def actualizar_treeview(tree):
    records = tree.get_children()
    for element in records:
        tree.delete(element)

    sql = "SELECT * FROM ventas ORDER BY id ASC"
    con = conexion()
    cursor = con.cursor()
    datos = cursor.execute(sql)

    resultado = datos.fetchall()
    for fila in resultado:
        tree.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[3], fila[4], fila[5], fila[6]))

def verificar_id(id):
    con = conexion()
    cursor = con.cursor()
    sql = "SELECT COUNT(*) FROM ventas WHERE id = ?;"
    cursor.execute(sql, id)
    id_ok = cursor.fetchone()[0] > 0
    con.close()
    return id_ok

def update(id, producto, cantidad, precio_unit, precio_total, forma_pago, tipo_cliente, tree, limpiar, actualizar_treeview):
    con = conexion()
    cursor = con.cursor()
    data = (producto, cantidad, precio_unit, precio_total, forma_pago, tipo_cliente, id)
    sql = "UPDATE ventas SET producto=?, cantidad=?, precio_unit=?, precio_total=?, forma_pago=?, tipo_cliente=? WHERE id=?;"
    cursor.execute(sql, data)
    con.commit()
    con.close()
    actualizar_treeview(tree)
    limpiar()
    return("Información", "Venta modificada")

def cargar_datos(tree):
    for item in tree.get_children():
        tree.delete(item)
        
    con = conexion()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM ventas ORDER BY id DESC")
    rows = cursor.fetchall()
    
    for row in rows:
        tree.insert("", len(tree.get_children()), text=row[0], values=row[1:])
    con.close()

# Inicialización del modelo Ventas
try:
    conexion()
    crear_tabla()
except:
    print("Error en la tabla")
