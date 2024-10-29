from tkinter import *
from tkinter import Label, Tk, StringVar, IntVar, Entry, Button, messagebox, ttk,PhotoImage, messagebox
from tkinter.font import Font
from clientes_modelo import actualizar_treeview, agregar_cliente, borrar_cliente, cargar_datos, verificar_id_cuit, update
from PIL import Image, ImageTk


## VISTA ##############################################
class MenuClientes:

    def __init__(self, window):
        self.window = window
        self.ventanaCentrada(900, 700)  # Centrar ventana
        self.imagen = PhotoImage(file="images/clientes.png")
        self.vista_clientes()  # Crear la interfaz

    def ventanaCentrada(self, ancho, alto):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        posX = (screen_width // 2) - (ancho // 2)
        posY = (screen_height // 2) - (alto // 2)
        self.window.geometry(f"{ancho}x{alto}+{int(posX)}+{int(posY)}")

    def vista_clientes(self):
        self.window.title("FERRETERIA - CARTERA DE CLIENTES")
        # Variables para controlar el diseño y color de la interfaz
        bgcolor = "lightgrey"
        #plum2
        #lightgrey
        titulo_font = Font(family="Helvetica", size=16, weight="bold")
        #button_font = Font(family="Sylfaen", size=106)
        boton_font = Font(family="Helvetica", size=10, weight="bold")
        entry_font = Font(family="Helvetica", size=10)

        titulo = Label(self.window, text="INGRESO DE DATOS", font=titulo_font, bd="10", bg=bgcolor)
        titulo.place(x=1,y=5,width=900,height=40)
        titulo.config(bg=bgcolor)

        etiqueta_imagen = Label(self.window, image=self.imagen)
        etiqueta_imagen.place(x=730, y=29)

        espacio_1 = Label(self.window)
        espacio_1.grid(row=1)
        espacio_2 = Label(self.window)
        espacio_2.grid(row=2)
        espacio_3 = Label(self.window)
        espacio_3.grid(row=3)
            
        Label(self.window, text="CUIT-DNI", font=boton_font).grid(row=6, column=1, sticky=E)
        Label(self.window, text="NOMBRE-RAZÓN SOCIAL", font=boton_font, anchor='e').grid(row=7, column=1, sticky=E)
        Label(self.window, text="TELÉFONO", font=boton_font, anchor='e').grid(row=8, column=1, sticky=E)
        Label(self.window, text="MAIL", font=boton_font, anchor='e').grid(row=6, column=5, sticky=E)
        Label(self.window, text="DIRECCIÓN", font=boton_font, anchor='e').grid(row=7, column=5, sticky=E)
    
        # Variables
        self.vid_cuit = IntVar()
        self.vnombre_rs = StringVar()
        self.vtelefono = IntVar()
        self.vmail = StringVar()
        self.vdireccion = StringVar()

        # Inputs
        Entry(self.window, textvariable=self.vid_cuit, font=entry_font, fg="black", bg="snow", relief="solid", justify="center").grid(row=6, column=2)
        Entry(self.window, textvariable=self.vnombre_rs, font=entry_font, fg="black", bg="snow", relief="solid", justify="center").grid(row=7, column=2)
        Entry(self.window, textvariable=self.vtelefono, font=entry_font, fg="black", bg="snow", relief="solid", justify="center").grid(row=8, column=2)
        Entry(self.window, textvariable=self.vmail, font=entry_font, fg="black", bg="snow", relief="solid", justify="center").grid(row=6, column=6)
        Entry(self.window, textvariable=self.vdireccion, font=entry_font, fg="black", bg="snow", relief="solid", justify="center").grid(row=7, column=6)

        self.vid_cuit.set(0), self.vnombre_rs.set("------"), self.vtelefono.set(0), self.vmail.set("---@---.com"), self.vdireccion.set("")

        espacio_4 = Label(self.window)
        espacio_4.grid(row=8)
        espacio_5 = Label(self.window)
        espacio_5.grid(row=9)

        zocalo_superior=Label(self.window, font=("Sylfaen",10), bd="10")
        zocalo_superior.place(x=5, y=145, width=900, height=20)
        zocalo_superior.config(fg="WHITE",bg=bgcolor)

        ## TREEVIEW #######################################
        etiqueta_espacio_5 = Label(self.window)
        etiqueta_espacio_5.grid(row=13)
        etiqueta_espacio_5.config(bg="plum2")

        ##grilla de datso
        self.tree = ttk.Treeview(self.window)
        self.tree["columns"] = ('1','2','3','4')
        self.tree.column("#0", width=25, minwidth=25)
        self.tree.column("1", width=80, minwidth=60, anchor="center")
        self.tree.column("2", width=50, minwidth=40, anchor="center")
        self.tree.column("3", width=80, minwidth=60, anchor="center")  
        self.tree.column("4", width=80, minwidth=60, anchor="center")
        self.tree.heading("#0", text="DNI/CUIT")
        self.tree.heading("1", text="NOMBRE / RAZÓN SOCIAL")
        self.tree.heading("2", text="TELEFONO")
        self.tree.heading("3", text="MAIL")
        self.tree.heading("4", text="DIRECCION")
        self.tree.place(x=5, y=260, width=890, height=250)

        ## BOTONES  #######################################

        Button(self.window, text="Guardar", font=titulo_font, bg=bgcolor, command= self.boton_guardar).place(x="50", y="180", width="150", height="50")
        
        Button(self.window, text="Modificar", font=titulo_font, bg=bgcolor, command= self.boton_modificar).place(x="250", y="180", width="150", height="50")
        
        Button(self.window, text="Eliminar", font=titulo_font, bg=bgcolor, command= self.boton_eliminar).place(x="450", y="180", width="150", height="50")

        cargar_datos(self.tree)

     
    def boton_guardar(self):
        titulo, mensaje = agregar_cliente(self.vid_cuit.get(), self.vnombre_rs.get(), self.vtelefono.get(), self.vmail.get(), self.vdireccion.get(), self.tree, self.limpiar, actualizar_treeview)
        messagebox.showinfo(titulo, mensaje)

    def boton_eliminar(self):
        confirma = messagebox.askquestion("ADVERTENCIA", "¿Está seguro qué desea borrar el registro?")
        if confirma == 'no':
            return
        titulo, mensaje = borrar_cliente(self.tree)

    def boton_modificar(self):
        idc = self.vid_cuit.get()
        if not idc:
            messagebox.showinfo("MODIFICAR CLIENTE", "Debe escribir un CUIT válido para modificar")
            return
        
        if not verificar_id_cuit(idc):
            messagebox.showinfo("MODIFICAR CLIENTE", "El CUIT ingresado no existe en la base de datos.")
            return

        titulo, mensaje = update(self.vid_cuit.get(), self.vnombre_rs.get(), self.vtelefono.get(), self.vmail.get(), self.vdireccion.get(), self.tree, self.limpiar, actualizar_treeview)
        messagebox.showinfo(titulo, mensaje)

    def limpiar(self):
        self.vid_cuit.set("")
        self.vnombre_rs.set("")
        self.vtelefono.set("-")
        self.vmail.set("@")
        self.vdireccion.set("")


if __name__ == "__main__":
    clientes_tk = Tk()
    app = MenuClientes(clientes_tk)
    clientes_tk.mainloop()



