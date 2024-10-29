import sqlite3
import re

# ##############################################
# MODELO
# ##############################################


def conexion():
    con=sqlite3.connect('ferreteria.db')
    return con

def crear_tabla():
    con = conexion()
    cursor = con.cursor()
    sql = """CREATE TABLE IF NOT EXISTS clientes
            (id_cuit INTEGER PRIMARY KEY,
            nombre_rs varchar(35),
            telefono varchar(20),
            mail varchar(35),
            direccion varchar(50))"""
    # id_cuit en vez de ser autoincremental, tomo el cuit como ID único
    # nombre_rs hace referencia al nombre completo o razón social
    cursor.execute(sql)
    con.commit()

##########  INSERTAR DATOS  #################

def agregar_cliente(id_cuit, nombre_rs, telefono, mail, direccion, tree, limpiar, actualizar_treeview):
    validacion_mail= re.compile((r"(\w+@\w+\.+\w)"),re.IGNORECASE)
    if validacion_mail.search(str(mail)) is None:
        return "Mail erroneo"
    
    con = conexion()
    cursor = con.cursor()
    
    cuit_buscado = (id_cuit,)
    sql_id_cuit = f"SELECT id_cuit FROM clientes WHERE id_cuit = ?"
    cursor.execute(sql_id_cuit, (id_cuit,))
    if cursor.fetchone() != None:
        return "El DNI-CUIT ya esta en la base de datos"
    
    data = (id_cuit, nombre_rs, telefono, mail, direccion)
    sql = "INSERT INTO clientes(id_cuit, nombre_rs, telefono, mail, direccion) VALUES(?, ?, ?, ?, ?)"
    cursor.execute(sql, data)
    con.commit()
    actualizar_treeview(tree)
    limpiar()
    return "Datos Cargados Correctamente"
            
        
def borrar_cliente(tree):
        valor = tree.selection()
        item = tree.item(valor)
        id_cuit = item['text']

        con = conexion()
        cursor = con.cursor()
        data = (id_cuit,)
        sql = "DELETE FROM clientes WHERE id_cuit = ?"
        cursor.execute(sql, data)
        con.commit()
        tree.delete(valor)
        return("Clientes", "Datos de cliente borrados")

def actualizar_treeview(tree):
    records = tree.get_children()
    for element in records:
        tree.delete(element)

    sql = "SELECT * FROM clientes ORDER BY id_cuit ASC"
    con = conexion()
    cursor = con.cursor()
    datos = cursor.execute(sql)

    resultado = datos.fetchall()
    for fila in resultado:
         tree.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[3], fila[4]))

def verificar_id_cuit(id_cuit):
    con = conexion()
    cursor = con.cursor()
    sql = "SELECT COUNT(*) FROM clientes WHERE id_cuit = ?;"
    cursor.execute(sql,id_cuit)
    id_cuit_ok = cursor.fetchone()[0] > 0
    con.close()
    return id_cuit_ok

def update(id_cuit, nombre_rs, telefono, mail, direccion, tree, limpiar, actualizar_treeview):
    con = conexion()
    cursor = con.cursor()
    data = (nombre_rs, telefono, mail, direccion, id_cuit)
    sql = "UPDATE clientes SET nombre_rs=?, telefono=?, mail=?, direccion=? WHERE id_cuit=?;"
    cursor.execute(sql, data)
    con.commit()
    con.close()
    actualizar_treeview(tree)
    limpiar()
    return("Información", "Cliente modificado")

def cargar_datos(tree):
    for item in tree.get_children():
        tree.delete(item)

    con = conexion()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM clientes ORDER BY id_cuit")
    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", len(tree.get_children()), text=row[0], values=row[1:])
    con.close()
     
# Inicialización del modelo Clientes
try:
    conexion()
    crear_tabla()
except:
    print("Error en la tabla")