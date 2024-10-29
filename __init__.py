from tkinter import *
from tkinter import END, messagebox, ttk
from tkinter.font import Font
from venta_modelo import actualizar_treeview, agregar, borrar, cargar_datos, verificar_id, update
from vista_botones import *
from PIL import Image, ImageTk
import venta_vista
import clientes_vista
import nosotros

class MenuPrincipal:
    
    def __init__(self, window):
        self.window = window
        self.ventanaCentrada(1100, 650)  # Centrar ventana
        self.vista_principal()  # Crear la interfaz

    def ventanaCentrada(self, ancho, alto):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        posX = (screen_width // 2) - (ancho // 2)
        posY = (screen_height // 2) - (alto // 2)
        self.window.geometry(f"{ancho}x{alto}+{int(posX)}+{int(posY)}")

     # Nueva función para abrir la ventana de Registrar Venta
    def boton_registrar_venta(self):
        nueva_ventana = Toplevel(self.window)  # Crear nueva ventana Toplevel
        #nueva_ventana.geometry("900x800")      # Tamaño de la nueva ventana
        venta_vista.MenuPrincipal(nueva_ventana)    # Lla

    def boton_clientes(self):
        nueva_ventana = Toplevel(self.window)  # Crear nueva ventana Toplevel
        #nueva_ventana.geometry("900x800")      # Tamaño de la nueva ventana
        clientes_vista.MenuClientes(nueva_ventana)    # Lla

    def boton_nosotros(self):
        nueva_ventana = Toplevel(self.window)
        nosotros.Nosotros(nueva_ventana)


    def boton_prueba_vista(self):
        pass
        #nueva_ventana = Toplevel(self.window)  # Crear nueva ventana Toplevel
        #nueva_ventana.geometry("900x800")      # Tamaño de la nueva ventana
        #prueba_vista.MenuPrincipal(nueva_ventana)    # Lla

    def vista_principal(self):
        self.window.title("FERRETERIA - TERMINAL DE VENTA")

        # Título de la ventana
        titulo = Label(self.window, text="FERRETERIA - TERMINAL DE VENTAS", bg="lightgrey")
        titulo.grid(row=0, column=0, columnspan=7, sticky=W + E)

        # Ajustes para botones
        button_font = Font(family="Helvetica", size=16, weight="bold")
        image_xy = 64

        # Cargar imágenes
        icon_venta = ImageTk.PhotoImage(Image.open("images/icon_ventas.png").resize((image_xy, image_xy)))
        icon_v_realizada = ImageTk.PhotoImage(Image.open("images/icon_v_realizada.png").resize((image_xy, image_xy)))
        icon_nosotros = ImageTk.PhotoImage(Image.open("images/icon_nosotros.png").resize((image_xy, image_xy)))
        icon_clientes = ImageTk.PhotoImage(Image.open("images/icon_clientes.png").resize((image_xy, image_xy)))

        # Crear botones con imágenes y texto
        Button(self.window, text="Registrar\nVenta", image=icon_venta, compound="top", font=button_font, command=self.boton_registrar_venta).place(x=x1, y=y1, width=b_width, height=b_height)

        Button(self.window, text="Ventas\nRealizadas", image=icon_v_realizada, compound="top", font=button_font).place(x=(x1 + b_width + b_padX), y=y1, width=b_width, height=b_height)

        Button(self.window, text="Nosotros...", image=icon_nosotros, compound="top", font=button_font, command=self.boton_nosotros).place(x=(x1 + 2 * (b_width + b_padX)), y=y1, width=b_width, height=b_height)
        
        Button(self.window, text="Clientes", image=icon_clientes, compound="top", font=button_font, command=self.boton_clientes).place(x=x1, y=(y1 + b_height + b_padY), width=b_width, height=b_height)

        # Mantener las referencias a las imágenes
        self.icon_venta = icon_venta
        self.icon_v_realizada = icon_v_realizada
        self.icon_nosotros = icon_nosotros
        self.icon_clientes = icon_clientes

if __name__ == "__main__":
    root_tk = Tk()
    app = MenuPrincipal(root_tk)
    root_tk.mainloop()
