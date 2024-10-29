from tkinter import *
from tkinter import END, messagebox, ttk
from tkinter.font import Font
from PIL import Image, ImageTk


# ##############################################
# VISTA VENTANA PRINCIPAL
# ##############################################
class Nosotros:
    def __init__(self, window):
        self.window = window
        self.ventanaCentrada(800, 500)  # Centrar ventana
        self.imagen = PhotoImage(file="images/nosotros.png")
        self.vista_nosotros()  # Crear la interfaz

    def ventanaCentrada(self, ancho, alto):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        posX = (screen_width // 2) - (ancho // 2)
        posY = (screen_height // 2) - (alto // 2)
        self.window.geometry(f"{ancho}x{alto}+{int(posX)}+{int(posY)}")

    def vista_nosotros(self):
        self.window.title("FERRETERIA")
        bgcolor = "lightgrey"
        titulo_font = Font(family="Helvetica", size=16, weight="bold")
        subtitulo_font = Font(family="Helvetica", size=14, weight="bold")

        titulo = Label(self.window, text="NOSOTROS", font=titulo_font, bd="10", bg=bgcolor)
        titulo.place(x=1, y=5, width=800, height=40)
        titulo.config(bg=bgcolor)

        imagen_nosotros = Label(self.window, image=self.imagen)
        imagen_nosotros.place(x=450, y=100)

        espacio_1 = Label(self.window)
        espacio_1.grid(row=1)
        espacio_2 = Label(self.window)
        espacio_2.grid(row=2)
        espacio_3 = Label(self.window)
        espacio_3.grid(row=3)

        integrante1 = Label(self.window, text="Javier Medina", font=subtitulo_font, bd="10")
        integrante1.place(x=20, y=100, width=400, height=40)
        
        integrante2 = Label(self.window, text="Nicolás Sampayo", font=subtitulo_font, bd="10")
        integrante2.place(x=20, y=150, width=400, height=40)

        integrante3 = Label(self.window, text="Lautaro Barrionuevo", font=subtitulo_font, bd="10")
        integrante3.place(x=20, y=200, width=400, height=40)

        integrante4 = Label(self.window, text="Eliana Guattarini", font=subtitulo_font, bd="10")
        integrante4.place(x=20, y=250, width=400, height=40)
        
        integrante5 = Label(self.window, text="Federico Escobedo", font=subtitulo_font, bd="10")
        integrante5.place(x=20, y=300, width=400, height=40)

if __name__ == "__main__":
    nos_tk = Tk()
    app = Nosotros(nos_tk)
    nos_tk.mainloop()
