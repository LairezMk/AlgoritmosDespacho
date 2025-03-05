from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
from customtkinter import *
import matplotlib.pyplot as plt
import numpy as np
from tkinter import font as tkFont
import pygame
from PIL import Image, ImageTk
from Procesos import Proceso
from Graficas import Mostrar_Procesos
import cv2

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
        ctk.set_default_color_theme("ThemeCoffee.json")
        self.title("Algoritmos de Procesos")
        self.geometry("600x550")
        self.resizable(False, False)
        #tkFont.Font(family="Kanit", size=12)
        self.fuente= CTkFont(family="Kanit\Kanit-Black.ttf", size=25, weight="bold")
        self.fuente2= CTkFont(family="Lato", size=15, weight="bold")
        fuente_aviso= CTkFont(family="Poppins", size=16, weight="bold")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        side_img_data = Image.open("Img-Cafe.png")
        side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(600, 100))  # Ajustamos el tamaño de la imagen

        # Agregar la imagen en la parte superior
        CTkLabel(self, text="", image=side_img).pack(fill="x", side="top")

        frame = ctk.CTkFrame(self, width=600, height=380, corner_radius=0)
        frame.pack_propagate(0)  # Evita que el frame se redimensione
        frame.pack(fill="both", expand=True)  

        # Título
        self.label = ctk.CTkLabel(master=frame, text="Algoritmos de Procesos", font=self.fuente)
        self.label.pack(pady=20)
        
        self.button_iniciar = ctk.CTkButton(master=frame, text="Iniciar", font=self.fuente2,
                                             command=self.abrir_grafica)
        self.button_iniciar.pack(pady=20)
        
        self.button_salir = ctk.CTkButton(master=frame, text="Salir", font=self.fuente2,
                                          command=self.on_closing)
        self.button_salir.pack(pady=20)

        icon_fifo = CTkImage(Image.open("fifo.png"), size=(50, 50))
        icon_sjf = CTkImage(Image.open("sjf.png"), size=(50, 50))
        icon_prio = CTkImage(Image.open("prioridad.png"), size=(50, 50))

        frame_icons = ctk.CTkFrame(master=frame, corner_radius=8)
        frame_icons.pack(pady=10)

        CTkLabel(frame_icons, text=" FIFO ", image=icon_fifo).pack(side="left", padx=10)
        CTkLabel(frame_icons, text=" SJF ", image=icon_sjf).pack(side="left", padx=10)
        CTkLabel(frame_icons, text=" Prioridad ", image=icon_prio).pack(side="left", padx=10)

        frame_info = ctk.CTkFrame(master=frame, corner_radius=8)
        frame_info.pack(side="bottom", anchor="se", padx=5, pady=5)

        label_autor = ctk.CTkLabel(frame_info, text="Desarrollado por:\nSamuel Herrera \nJonathan Gaviria", font=fuente_aviso, justify="left",
                                   text_color="white")
        label_autor.pack(padx=10, pady=5)

        switch = ctk.CTkSwitch(master=frame, text="Modo Oscuro", command=self.cambiar_modo, font=self.fuente2, text_color="white", 
                               corner_radius=10)
        switch.pack(pady=10)
        
        self.set_icon("Windows.jpg")

    def cambiar_modo(self):
            if ctk.get_appearance_mode() == "Dark":
                ctk.set_appearance_mode("Light")
            else:
                ctk.set_appearance_mode("Dark")
    
    def abrir_grafica(self):
        self.withdraw()  # Oculta la ventana principal
        Grafica(self)
    
    def on_closing(self):
        msg = CTkMessagebox(title="Salir?", message="Desea cerrar el programa?",
                        icon="question", option_1="No", option_2="Si")
        response = msg.get()
    
        if response=="Si":
            pygame.mixer.init()
            pygame.mixer.music.load("mario64.mp3")
            pygame.mixer.music.play()
            self.after(1000, self.quit)  # Cierra toda la aplicación

        else:
            print("Click 'Yes' to exit!")
            
    def set_icon(self, icon_path):
        try:
            img = Image.open(icon_path)
            img = img.resize((32, 32), Image.Resampling.LANCZOS)  # Redimensiona la imagen
            photo = ImageTk.PhotoImage(img)
            self.iconphoto(False, photo)
        except Exception as e:
            print(f"Error cargando el icono: {e}")

class Grafica(ctk.CTkToplevel):
    def __init__(self, root):
        super().__init__(root)
        ctk.set_default_color_theme("ThemeCoffee.json")
        self.root = root
        self.title("Graficar")
        self.geometry("600x350")
        self.resizable(False, False)
        fuente = CTkFont(family="Kanit\Kanit-Black.ttf", size=20, weight="bold")
        fuente_2= CTkFont(family="Lato", size=15, weight="bold")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        frame = ctk.CTkFrame(self, width=580, height=330, border_width=2, border_color="white")
        frame.pack_propagate(0)  # Evita que el frame se redimensione
        frame.grid(row=0, column=0, padx=10, pady=10)
        
        self.label = ctk.CTkLabel(master=frame, text="Ingrese la Cantidad de Procesos (máx 10)", font=fuente)
        self.label.pack(pady=20)
        
        self.num_procesos = ctk.CTkEntry(master=frame, font=("Bevan", 20))
        self.num_procesos.pack(pady=10)
        
        self.button_ejecutar = ctk.CTkButton(master=frame, text="Ejecutar Algoritmo", font=fuente_2, command=self.ejecutar_algoritmo)
        self.button_ejecutar.pack(pady=20)
        
        self.button_volver = ctk.CTkButton(master=frame, text="Volver al inicio", font=fuente_2, command=self.volver_inicio)
        self.button_volver.pack(pady=20)
    
    def ejecutar_algoritmo(self):
        try:
            num_procesos = int(self.num_procesos.get())
            if 1 <= num_procesos <= 10:
                self.pedir_datos(num_procesos)
                #self.mostrar_animacion(num_procesos)
            else:
                CTkMessagebox(title="Error", message="Ingrese un número entre 1 y 10.")
        except ValueError:
            CTkMessagebox(title="Error", message="Ingrese un número válido.")
    
    def mostrar_animacion(self, num_procesos):
        plt.figure()
        plt.plot(np.random.rand(10))
        plt.title(f"Animación con {num_procesos} procesos")
        plt.show()

    def pedir_datos(self, num_procesos):
        #Lista procesos
        self.destroy()
        Procesos(self.root, num_procesos)

    def volver_inicio(self):
        self.destroy()
        self.root.deiconify()

    def on_closing(self):
        msg = CTkMessagebox(title="Salir?", message="Desea cerrar el programa?",
                        icon="question", option_1="No", option_2="Si")
        response = msg.get()
    
        if response=="Si":
            pygame.mixer.init()
            pygame.mixer.music.load("mario64.mp3")
            pygame.mixer.music.play()
            self.after(1000, self.quit)  # Cierra toda la aplicación

class Procesos(ctk.CTkToplevel):
    def __init__(self, root, num_procesos):
        super().__init__(root)
        self.title("Procesos")
        self.geometry("800x600")
        self.resizable(False, False)
        self.root= root

        self.fuente1= CTkFont(family="Kanit\Kanit-Black.ttf", size=20, weight="bold")
        self.fuente2= CTkFont(family="Lato", size=15, weight="bold")

        # On closing
        self.protocol("WM_DELETE_WINDOW", self.volver_inicio)

        self.num_procesos = num_procesos
        self.proceso_actual = 0
        self.Lprocesos = []  # Lista de procesos

        frameizq = ctk.CTkFrame(self, width=380, height=580, border_width=2, border_color="white")
        frameizq.pack_propagate(0)  # Evita que el frame se redimensione
        frameizq.grid(row=0, column=0, padx=10, pady=10)

        self.frameder = ctk.CTkFrame(self, width=380, height=580, border_width=2, border_color="white")
        self.frameder.pack_propagate(0)  # Evita que el frame se redimensione
        self.frameder.grid(row=0, column=1, padx=10, pady=10)

        # Crear la interfaz
        self.label_titulo = ctk.CTkLabel(frameizq, text="", font=self.fuente1)
        self.label_titulo.pack(pady=10)

        self.label_nombre = ctk.CTkLabel(frameizq, text="Ingrese el nombre del proceso:", font=self.fuente2)
        self.label_nombre.pack(pady=5)
        #Hacer que el nombre solo pueda ser de maximo 2 caracteres
        self.entry_nombre = ctk.CTkEntry(frameizq, font=self.fuente2)
        self.entry_nombre.pack(pady=5)
        vcmd = (self.register(self.validar_longitud), "%P")
        self.entry_nombre.configure(validate="key", validatecommand=vcmd)

        self.label_llegada = ctk.CTkLabel(frameizq, text="Ingrese el tiempo de llegada del proceso:", font=self.fuente2)
        self.label_llegada.pack(pady=5)
        self.entry_llegada = ctk.CTkEntry(frameizq, font=("Bevan", 15))
        self.entry_llegada.pack(pady=5)

        self.label_rafaga = ctk.CTkLabel(frameizq, text="Ingrese la ráfaga del proceso:", font=self.fuente2)
        self.label_rafaga.pack(pady=5)
        self.entry_rafaga = ctk.CTkEntry(frameizq, font=("Bevan", 15))
        self.entry_rafaga.pack(pady=5)

        self.label_prioridad = ctk.CTkLabel(frameizq, text="Ingrese la prioridad del proceso:", font=self.fuente2)
        self.label_prioridad.pack(pady=5)
        self.entry_prioridad = ctk.CTkEntry(frameizq, font=("Bevan", 15))
        self.entry_prioridad.pack(pady=5)

        self.boton_guardar = ctk.CTkButton(frameizq, text="Guardar", font=self.fuente2, command=self.guardar_proceso)
        self.boton_guardar.pack(pady=20)

        self.boton_volver= ctk.CTkButton(frameizq, text="Volver al inicio", font=self.fuente2, command=self.volver_inicio)
        self.boton_volver.pack(pady=20)

        #Sección para la ejecución del video
        self.canvas=ctk.CTkCanvas(self.frameder, width=300, height=300)
        self.canvas.pack(pady=150)
        video=cv2.VideoCapture("shimmy.mp4")
        self.video=video
        self.actualizar_video()
        self.actualizar_interfaz()

        self.entries = [self.entry_nombre, self.entry_llegada, self.entry_rafaga, self.entry_prioridad]

        # Asociar eventos a cada Entry
        for i, entry in enumerate(self.entries):
            entry.bind("<Return>", lambda event, idx=i: self.focus_next(idx))  # Enter para avanzar
            entry.bind("<Up>", lambda event, idx=i: self.focus_previous(idx))  # Flecha arriba
            entry.bind("<Down>", lambda event, idx=i: self.focus_next(idx))    # Flecha abajo

    def focus_next(self, index):
        """ Mueve el cursos al siguiente campo """
        if index + 1 < len(self.entries):
            self.entries[index + 1].focus_set()

    def focus_previous(self, index):
        """ Mueve el cursos al campo anterior """
        if index - 1 >= 0:
            self.entries[index - 1].focus_set()

    def validar_longitud(self, P):
        #Valida la longitud del texto ingresado 
        return len(P) <= 2

    def actualizar_interfaz(self):
        """Actualiza la interfaz para el proceso actual"""
        self.proceso_actual += 1
        if self.proceso_actual > self.num_procesos:
            self.mostrar_resumen()
            return

        self.label_titulo.configure(text=f"Ingresando el proceso {self.proceso_actual}/{self.num_procesos}", font=self.fuente1)

        # Limpiar los campos de entrada
        self.entry_nombre.delete(0, "end")
        self.entry_llegada.delete(0, "end")
        self.entry_rafaga.delete(0, "end")
        self.entry_prioridad.delete(0, "end")

    def actualizar_video(self):   
        #Actualizar los fotogramas del video

        ret, frame = self.video.read()

        if ret:
            frame=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame=Image.fromarray(frame)
            frame=ImageTk.PhotoImage(frame)
            self.canvas.create_image(0, 0, image=frame, anchor="nw")
            self.canvas.image=frame
            self.after(10, self.actualizar_video)
        #Si no hay más fotogramas, se vuelve a reproducir el video
        else:
            self.video=cv2.VideoCapture("shimmy.mp4")
            self.actualizar_video()

    def guardar_proceso(self):
        """Guarda el proceso actual y actualiza la interfaz para el siguiente"""
        nombre = self.entry_nombre.get().strip() #El .strip elimina los espacios en blanco
        llegada = self.entry_llegada.get().strip()
        rafaga = self.entry_rafaga.get().strip()
        prioridad = self.entry_prioridad.get().strip()

        # Validaciones básicas
        if not nombre or not llegada.isdigit() or not rafaga.isdigit() or not prioridad.isdigit():
            CTkMessagebox(title="Error", message="Por favor, ingrese valores válidos.")
            return

        self.Lprocesos.append(Proceso(nombre, int(llegada), int(rafaga), int(prioridad)))

        if self.proceso_actual <= self.num_procesos:
            #Hacer que el mensaje de guardado desaparezca después de 2 segundos automaticamente
            self.label_mensaje = ctk.CTkLabel(self.frameder, text="Proceso guardado correctamente.", font=("Bevan", 14))
            self.label_mensaje.pack(pady=5)
            self.after(2000, self.label_mensaje.destroy)  # Desaparece en 2 segundos
            #self.actualizar_interfaz()

            #self.after(2000, self.actualizar_interfaz)

        self.actualizar_interfaz()

    def mostrar_resumen(self):
        mensaje = "Procesos ingresados:\n"
        for i in range(len(self.Lprocesos)):
            proceso = self.Lprocesos[i]
            mensaje += (f"\nProceso {i+1}: {proceso.nombre}\n"
                        f"  - Llegada: {proceso.tiempo_llegada}\n"
                        f"  - Ráfaga: {proceso.rafaga}\n"
                        f"  - Prioridad: {proceso.prioridad}\n")

        self.mensaje=CTkMessagebox(title="Resumen de Procesos", message=mensaje, icon="info", option_1="Ok")
        #self.destroy()  
        #self.volver_inicio()
        #Se muestran las graficas solo si se ha presionado el boton ok en el resumen de procesos
        if self.mensaje.get()=="Ok":
            #self.withdraw()
            Mostrar_Procesos(self.Lprocesos)
            self.destroy()
            self.volver_inicio()

    def volver_inicio(self):
        self.destroy()
        Grafica(self.root)
        
if __name__ == "__main__":
    app = App()
    app.mainloop()
