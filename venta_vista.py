from tkinter import *
from tkinter import END, messagebox, ttk
from venta_modelo import actualizar_treeview, agregar, borrar, cargar_datos, verificar_id, update

# ##############################################
# VISTA VENTANA PRINCIPAL
# ##############################################
class MenuPrincipal:
    
    def __init__(self, window):
        self.window = window
        self.ventanaCentrada(700, 500)  # Centrar ventana
        self.vista_principal()  # Crear la interfaz

    def ventanaCentrada(self, ancho, alto):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        posX = (screen_width // 2) - (ancho // 2)
        posY = (screen_height // 2) - (alto // 2)
        self.window.geometry(f"{ancho}x{alto}+{int(posX)}+{int(posY)}")

    def vista_principal(self):
        self.window.title("FERRETERIA - REGISTRAR VENTA")

        titulo = Label(self.window, text="FERRETERIA - REGISTRAR VENTA", bg="lightgrey")
        titulo.grid(row=0, column=0, columnspan=7, sticky=W + E)

        # COMBOBOX
        cb_forma_pago = ["Débito", "Tarj. Crédito", "Cta. Cte.", "MercadoPago", "MODO", "Transferencia", "Efectivo"]
        cb_tipo_cliente = ["Consumidor Final", "Empresa"]

        # ETIQUETAS DE INPUTS
        Label(self.window, text="PRODUCTO").grid(row=1, column=0, sticky=E, pady=2)
        Label(self.window, text="CANTIDAD").grid(row=2, column=0, sticky=E, pady=2)
        Label(self.window, text="PRECIO UNIT.").grid(row=3, column=0, sticky=E, pady=2)
        Label(self.window, text="PRECIO TOTAL").grid(row=4, column=0, sticky=E, pady=2)
        Label(self.window, text="FORMA DE PAGO").grid(row=5, column=0, sticky=E, pady=2)
        Label(self.window, text="TIPO DE CLIENTE").grid(row=6, column=0, sticky=E, pady=(2, 20))

        # Variables
        self.vid = StringVar()
        self.vproducto = StringVar()
        self.vcantidad = StringVar()
        self.vprecio_unit = StringVar()
        self.vprecio_total = StringVar()
        self.vforma_pago = StringVar()
        self.vtipo_cliente = StringVar()

        # Calcular Precio Total
        self.vcantidad.trace("w", self.calcular_precio_total)
        self.vprecio_unit.trace("w", self.calcular_precio_total)

        # Inputs
        Entry(self.window, textvariable=self.vproducto).grid(row=1, column=1)
        Entry(self.window, textvariable=self.vcantidad, justify="right").grid(row=2, column=1)
        Entry(self.window, textvariable=self.vprecio_unit, justify="right").grid(row=3, column=1)
        Entry(self.window, textvariable=self.vprecio_total, justify="right", state="readonly").grid(row=4, column=1)

        combo_forma_pago = ttk.Combobox(self.window, textvariable=self.vforma_pago, values=cb_forma_pago, state="readonly")
        combo_forma_pago.grid(row=5, column=1)
        combo_forma_pago.set("Forma de Pago")

        combo_tipo_cliente = ttk.Combobox(self.window, textvariable=self.vtipo_cliente, values=cb_tipo_cliente, state="readonly")
        combo_tipo_cliente.grid(row=6, column=1, pady=(2, 20))
        combo_tipo_cliente.set("Tipo de Cliente")

        Entry(self.window, textvariable=self.vid, justify="center", width="10").grid(row=2, column=3, padx=(2, 0))

        # Treeview
        self.tree = ttk.Treeview(self.window)
        self.tree["columns"] = ("col1", "col2", "col3", "col4", "col5", "col6")
        self.tree.column("#0", width=25, minwidth=25, anchor=W)
        self.tree.heading("#0", text="ID")
        self.tree.column("col1", width=140, minwidth=80, anchor=W)
        self.tree.heading("col1", text="PRODUCTO")
        self.tree.column("col2", width=65, minwidth=65, anchor=CENTER)
        self.tree.heading("col2", text="CANTIDAD")
        self.tree.column("col3", width=80, minwidth=80, anchor=E)
        self.tree.heading("col3", text="PRECIO UNIT")
        self.tree.column("col4", width=100, minwidth=80, anchor=E)
        self.tree.heading("col4", text="PRECIO TOTAL")
        self.tree.column("col5", width=110, minwidth=100, anchor=CENTER)
        self.tree.heading("col5", text="FORMA DE PAGO")
        self.tree.column("col6", width=110, minwidth=80, anchor=CENTER)
        self.tree.heading("col6", text="TIPO DE CLIENTE")

        self.tree.grid(column=0, row=10, columnspan=6, padx=(25, 0))

        # Botones
        Button(self.window, text="Registrar Venta", width=20, command=self.vista_agregar).grid(row=1, column=2)
        Button(self.window, text="Modificar por ID", width=20, command=self.vista_update).grid(row=2, column=2)
        Button(self.window, text="Eliminar", width=20, command=self.vista_borrar).grid(row=3, column=2)
        Button(self.window, text="Limpiar datos", width=20, command=self.limpiar).grid(row=4, column=2)

        # Cargar los datos en el Treeview al iniciar
        cargar_datos(self.tree)

    def calcular_precio_total(self, *args):
        try:
            cantidad = float(self.vcantidad.get())
            precio_unit = float(self.vprecio_unit.get())
            precio_total = cantidad * precio_unit
            self.vprecio_total.set(f"{precio_total:.2f}")
        except ValueError:
            self.vprecio_total.set("0.00")

    def vista_agregar(self):
        titulo, mensaje = agregar(self.vproducto.get(), self.vcantidad.get(), self.vprecio_unit.get(), 
                                  self.vprecio_total.get(), self.vforma_pago.get(), self.vtipo_cliente.get(), 
                                  self.tree, self.limpiar, actualizar_treeview)
        messagebox.showinfo(titulo, mensaje)

    def vista_borrar(self):
        confirma = messagebox.askquestion("ADVERTENCIA", "¿Está seguro qué desea borrar el registro?")
        if confirma == 'no':
            return
        titulo, mensaje = borrar(self.tree)

    def vista_update(self):
        id = self.vid.get()
        if not id:
            messagebox.showinfo("MODIFICAR", "Debe escribir un ID válido para modificar.")
            return

        if not verificar_id(id):
            messagebox.showinfo("MODIFICAR", "El ID ingresado no existe en la base de datos.")
            return

        titulo, mensaje = update(self.vid.get(), self.vproducto.get(), self.vcantidad.get(), 
                                 self.vprecio_unit.get(), self.vprecio_total.get(), 
                                 self.vforma_pago.get(), self.vtipo_cliente.get(), 
                                 self.tree, self.limpiar, actualizar_treeview)
        messagebox.showinfo(titulo, mensaje)

    def limpiar(self):
        self.vid.set("")
        self.vproducto.set("")
        self.vcantidad.set("")
        self.vprecio_unit.set("")
        self.vprecio_total.set("0.00")
        self.vforma_pago.set("Forma de Pago")
        self.vtipo_cliente.set("Tipo de Cliente")

if __name__ == "__main__":
    root_tk = Tk()
    app = MenuPrincipal(root_tk)
    root_tk.mainloop()
