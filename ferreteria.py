from tkinter import *
from tkinter import messagebox
import sqlite3
from tkinter import ttk
import re

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


try:
    conexion()
    crear_tabla()
except:
    print("Error en la tabla")




def agregar(producto, cantidad, precio_unit, precio_total, forma_pago, tipo_cliente, tree):
    con = conexion()
    cursor = con.cursor()
    data = (producto, cantidad, precio_unit, precio_total, forma_pago, tipo_cliente)
    sql = "INSERT INTO ventas(producto, cantidad, precio_unit, precio_total, forma_pago, tipo_cliente) VALUES (?, ?, ?, ?, ?, ?)"
    cursor.execute(sql, data)
    con.commit()
    messagebox.showinfo("Venta", "Venta registrada")
    actualizar_treeview(tree)
    limpiar()


def borrar(tree):
    confirma = messagebox.askquestion("ADVERTENCIA", "¿Está seguro qué desea borrar el registro?")
    if confirma == 'no':
        return

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
    messagebox.showinfo("Venta", "Registro borrado")


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
        print(fila)
        tree.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[3], fila[4], fila[5], fila[6]))


def update(id, producto, cantidad, precio_unit, precio_total, forma_pago, tipo_cliente, tree):
    if not id:
        messagebox.showinfo("MODIFICAR", "Debe escribir un ID válido para modificar.")
        return

    con = conexion()
    cursor = con.cursor()
    data = (producto, cantidad, precio_unit, precio_total, forma_pago, tipo_cliente, id)
    sql = "UPDATE ventas SET producto=?, cantidad=?, precio_unit=?, precio_total=?, forma_pago=?, tipo_cliente=? WHERE id=?;"
    cursor.execute(sql, data)
    con.commit()
    con.close()
    messagebox.showinfo("Información", "Venta modificada")
    actualizar_treeview(tree)
    limpiar()

def limpiar():
    entry_producto.delete(0, END)
    entry_cantidad.delete(0, END)
    entry_precio_unit.delete(0, END)
    entry_precio_total.delete(0, END) 
    entry_modificar.delete(0, END)
    #entry_forma_pago.delete(0, END)
    #entry_tipo_cliente.delete(0, END)

#LA FUNCION CARGAR_DATOS FUNCIONA COMO CONSULTA
# YA QUE SE UTILIZA PARA CARGAR LOS DATOS EXISTENTES
# EN LA BASE DE DATOS
def cargar_datos(tree):
    for item in tree.get_children():
        tree.delete(item)
        
    con = conexion()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM ventas ORDER BY id DESC")
    rows = cursor.fetchall()
    
    for row in rows:
        tree.insert("", END, text=row[0], values=row[1:])
    con.close()

# ##############################################
# VISTA VENTANA PRINCIPAL
# ##############################################
principal = Tk()
principal.title("FERRETERIA - TERMINAL DE VENTA")
principal.geometry("700x500")

titulo = Label(principal, text="FERRETERIA - TERMINAL DE VENTAS", bg="lightgrey")
titulo.grid(row=0, column=0, columnspan=7, sticky=W+E)

# COMBOBOX
cb_forma_pago = ["Débito", "Tarj. Crédito", "Cta. Cte.", "MercadoPago", "MODO", "Transferencia", "Efectivo"]
cb_tipo_cliente = ["Consumidor Final", "Empresa"]

# ETIQUETAS DE INPUTS
producto = Label(principal, text="PRODUCTO")
producto.grid(row=1, column=0, sticky=E, pady=2)

cantidad = Label(principal, text="CANTIDAD")
cantidad.grid(row=2, column=0, sticky=E, pady=2)

precio_unit = Label(principal, text="PRECIO UNIT.")
precio_unit.grid(row=3, column=0, sticky=E, pady=2)

precio_total = Label(principal, text="PRECIO TOTAL")
precio_total.grid(row=4, column=0, sticky=E, pady=2)

forma_pago = Label(principal, text="FORMA DE PAGO")
forma_pago.grid(row=5, column=0, sticky=E, pady=2)

tipo_cliente = Label(principal, text="TIPO DE CLIENTE")
tipo_cliente.grid(row=6, column=0, sticky=E, pady=(2, 20))

####################################

vid = StringVar()
vproducto = StringVar()
vcantidad = StringVar()
vprecio_unit = StringVar()
vprecio_total = StringVar()
vforma_pago = StringVar()
vtipo_cliente = StringVar()

################################################
# FUNCIONES VARIAS - CALCULAR PRECIO TOTAL EN TIEMPO REAL
# La funcion TRACE de TKINTER está explicado
# en el capitulo 10, del libro Building Modern GUIs with Tkinter and Python - Saurabh Chandrakar
# en el capítulo 9, del libro Python A Fondo - Oscar Ramires Jimenéz
################################################

def calcular_precio_total(*args):
    try:
        cantidad = float(vcantidad.get())
        precio_unit = float(vprecio_unit.get())
        precio_total = cantidad * precio_unit
        vprecio_total.set(f"{precio_total:.2f}")
    except ValueError:
        vprecio_total.set("0.00")


vcantidad.trace("w", calcular_precio_total)
vprecio_unit.trace("w", calcular_precio_total)

####################################
# INPUTS
entry_producto = Entry(principal, textvariable=vproducto)
entry_producto.grid(row=1, column=1)

entry_cantidad = Entry(principal, textvariable=vcantidad, justify="right")
entry_cantidad.grid(row=2, column=1)

entry_precio_unit = Entry(principal, textvariable=vprecio_unit, justify="right")
entry_precio_unit.grid(row=3, column=1)

entry_precio_total = Entry(principal, textvariable=vprecio_total, justify="right", state="readonly")
entry_precio_total.grid(row=4, column=1)

combo_forma_pago = ttk.Combobox(principal, textvariable=vforma_pago, values=cb_forma_pago, state="readonly")
combo_forma_pago.grid(row=5, column=1)
combo_forma_pago.set("Forma de Pago")

combo_tipo_cliente = ttk.Combobox(principal, textvariable=vtipo_cliente, values=cb_tipo_cliente, state="readonly")
combo_tipo_cliente.grid(row=6, column=1, pady=(2, 20))
combo_tipo_cliente.set("Tipo de Cliente")

entry_modificar = Entry(principal, textvariable=vid, justify="center", width="10")
entry_modificar.grid(row=2, column=3, padx=(2, 0))

#####################################
# TREEVIEW
#####################################

tree = ttk.Treeview(principal)
tree["columns"] = ("col1", "col2", "col3", "col4", "col5", "col6")
tree.column("#0", width=25, minwidth=25, anchor=W)
tree.heading("#0", text="ID")
tree.column("col1", width=140, minwidth=80, anchor=W)
tree.heading("col1", text="PRODUCTO")
tree.column("col2", width=65, minwidth=65, anchor=CENTER)
tree.heading("col2", text="CANTIDAD")
tree.column("col3", width=80, minwidth=80, anchor=E)
tree.heading("col3", text="PRECIO UNIT")
tree.column("col4", width=100, minwidth=80, anchor=E)
tree.heading("col4", text="PRECIO TOTAL")
tree.column("col5", width=110, minwidth=100, anchor=CENTER)
tree.heading("col5", text="FORMA DE PAGO")
tree.column("col6", width=110, minwidth=80, anchor=CENTER)
tree.heading("col6", text="TIPO DE CLIENTE")

tree.grid(column=0, row=10, columnspan=6, padx=(25, 0))


##################################
# BOTONES DE CONTROL
##################################

boton_agregar = Button(principal, text="Registrar Venta",width=20, command=lambda:agregar(vproducto.get(), vcantidad.get(), vprecio_unit.get(), vprecio_total.get(), vforma_pago.get(), vtipo_cliente.get(), tree))
boton_agregar.grid(row=1, column=2)

boton_modificar = Button(principal, text="Modificar por ID", width=20, command=lambda:update(vid.get(), vproducto.get(), vcantidad.get(), vprecio_unit.get(), vprecio_total.get(), vforma_pago.get(), vtipo_cliente.get(), tree))
boton_modificar.grid(row=2, column=2)

boton_eliminar = Button(principal, text="Eliminar",width=20, command=lambda:borrar(tree))
boton_eliminar.grid(row=3, column=2)

boton_limpiar = Button(principal, text="Limpiar datos", width=20, command= lambda:limpiar())
boton_limpiar.grid(row=4, column=2)

cargar_datos(tree)
principal.mainloop()
