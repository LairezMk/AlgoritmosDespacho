import pandas as pd
import plotly.io as pio
from PIL import Image, ImageTk
#import tkinter as tk
import customtkinter as ctk 
from io import BytesIO
import plotly.figure_factory as ff
from Procesos import *
import webbrowser
from CTkMessagebox import CTkMessagebox
#import pygame

class Mostrar_Procesos(ctk.CTkToplevel):  # Clase para mostrar la ventana con gráficos
    def __init__(self, procesos):
        super().__init__()
        self.title("Graficar")
        self.geometry("800x800")
        self.resizable(False, False)
        self.procesos = procesos
        self.fuente1= ctk.CTkFont(family="Lato", size=16, weight="bold")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)  

        # Crear pestañas
        self.TabView = ctk.CTkTabview(self, width=750, height=550)
        self.TabView.pack(pady=20)

        self.TabView.add("FIFO")
        self.TabView.add("SJF")
        self.TabView.add("Prioridad")

        # Crear labels en las pestañas
        self.labelfifo = ctk.CTkLabel(self.TabView.tab("FIFO"), text="Cargando...")
        self.labelfifo.pack(pady=20)

        self.labelsjf = ctk.CTkLabel(self.TabView.tab("SJF"), text="SJF")
        self.labelsjf.pack(pady=20)

        self.labelprioridad = ctk.CTkLabel(self.TabView.tab("Prioridad"), text="Prioridad")
        self.labelprioridad.pack(pady=20)

        # Llamar al método para generar la gráfica
        self.generar_grafica(self.procesos, "FIFO")
        self.generar_grafica(self.procesos, "SJF")
        self.generar_grafica(self.procesos, "Prioridad")

    def generar_grafica(self, procesos, algoritmo):

        if algoritmo == "FIFO":
            # Calcular el tiempo de espera y de sistema para el algoritmo FIFO
            procesos.sort(key=lambda x: x.tiempo_llegada)
            procesos = Fifo(procesos)[0]

        elif algoritmo == "SJF":
            # Calcular el tiempo de espera y de sistema para el algoritmo SJF
            procesos = SJF(procesos)[0]

        elif algoritmo == "Prioridad":
            # Calcular el tiempo de espera y de sistema para el algoritmo de prioridad
            procesos = Prioridad(procesos)[0]

        procesos.sort(key=lambda x: x.tiempo_llegada)

        # Convertir los datos de los procesos a una lista de diccionarios
        procesos_data = [{"Task": p.nombre, "Tiempo llegada": p.tiempo_llegada, "Ráfaga": p.rafaga, "Finish": p.tiempo_final, "Start": p.tiempo_inicio} for p in procesos]

        # Datos para la gráfica de Gantt
        df = pd.DataFrame(procesos_data)

        # Crear la gráfica de Gantt
        fig = ff.create_gantt(df, index_col="Task", show_colorbar=False, group_tasks=True, title=f"Diagrama de Gantt - {algoritmo}")
        fig.update_layout(xaxis_type='linear', autosize=True, width=700, height=300)
        fig.update_xaxes(title="Tiempo (segundos)", dtick=1)  # Especificar eje X como numérico
        fig.update_yaxes(title="Procesos")

        #fig.show()

        #Obtener el link para abrir la gráfica en el navegador

        pio.write_html(fig, file='gantt.html', auto_open=False)
        
        # Convertir la gráfica a imagen
        img_bytes = pio.to_image(fig, format="png")
        img = Image.open(BytesIO(img_bytes))

        # Convertir la imagen a un formato compatible con tkinter
        img_tk = ImageTk.PhotoImage(img)

        if algoritmo == "FIFO":
            # Actualizar el label con la imagen en la pestaña FIFO
            self.labelfifo.configure(image=img_tk, text="")
            self.labelfifo.pack(pady=20)
            #Crear un label para mostrar el tiempo de espera y de sistema
            self.label_fifo = ctk.CTkLabel(self.TabView.tab("FIFO"), text=f"Tiempo de espera: {Fifo(procesos)[1]}", font=self.fuente1)
            self.label_fifo.pack(pady=20)
            self.label_fifo = ctk.CTkLabel(self.TabView.tab("FIFO"), text=f"Tiempo de sistema: {Fifo(procesos)[2]}", font=self.fuente1)
            self.label_fifo.pack(pady=20)

            #Crear un link para ver abrir el diagrama de gantt en el navegador, solo se ejecuta si se hace click en el link
            self.link= ctk.CTkLabel(self.TabView.tab("FIFO"), text="Abrir en navegador", text_color="lightblue", cursor="hand2", font=self.fuente1)
            self.link.pack(pady=20)

           # link=fig.show()

            self.link.bind("<Button-1>", lambda e: webbrowser.open('gantt.html')) 

        elif algoritmo == "SJF":
            # Actualizar el label con la imagen en la pestaña SJF
            self.labelsjf.configure(image=img_tk, text="")
            self.labelsjf.pack(pady=20)
            #Crear un label para mostrar el tiempo de espera y de sistema
            self.label_sjf = ctk.CTkLabel(self.TabView.tab("SJF"), text=f"Tiempo de espera: {SJF(procesos)[1]}", font=self.fuente1)
            self.label_sjf.pack(pady=20)
            self.label_sjf = ctk.CTkLabel(self.TabView.tab("SJF"), text=f"Tiempo de sistema: {SJF(procesos)[2]}", font=self.fuente1)
            self.label_sjf.pack(pady=20)

            #Crear un link para ver abrir el diagrama de gantt en el navegador, solo se ejecuta si se hace click en el link
            self.link= ctk.CTkLabel(self.TabView.tab("SJF"), text="Abrir en navegador", text_color="lightblue", cursor="hand2", font=self.fuente1)
            self.link.pack(pady=20)

           # link=fig.show()

            self.link.bind("<Button-1>", lambda e: webbrowser.open('gantt.html')) 

        elif algoritmo == "Prioridad":
            # Actualizar el label con la imagen en la pestaña Prioridad
            self.labelprioridad.configure(image=img_tk, text="")
            self.labelprioridad.pack(pady=20)
            #Crear un label para mostrar el tiempo de espera y de sistema
            self.label_prioridad = ctk.CTkLabel(self.TabView.tab("Prioridad"), text=f"Tiempo de espera: {Prioridad(procesos)[1]}", font=self.fuente1)
            self.label_prioridad.pack(pady=20)
            self.label_prioridad = ctk.CTkLabel(self.TabView.tab("Prioridad"), text=f"Tiempo de sistema: {Prioridad(procesos)[2]}", font=self.fuente1)
            self.label_prioridad.pack(pady=20)

            #Crear un link para ver abrir el diagrama de gantt en el navegador, solo se ejecuta si se hace click en el link
            self.link= ctk.CTkLabel(self.TabView.tab("Prioridad"), text="Abrir en navegador", text_color="lightblue", cursor="hand2", font=self.fuente1)
            self.link.pack(pady=20)

           # link=fig.show()

            self.link.bind("<Button-1>", lambda e: webbrowser.open('gantt.html')) 

    def on_closing(self):
        msg = CTkMessagebox(title="Salir?", message="Desea cerrar las gráficas?",
                        icon="question", option_1="No", option_2="Si")
        response = msg.get()
    
        if response=="Si":
            #pygame.mixer.init()
            #pygame.mixer.music.load("mario64.mp3")
            #pygame.mixer.music.play()
            #self.after(1000, self.quit)  # Cierra toda la aplicación
            self.destroy()

if __name__ == "__main__":
    procesos = [Proceso("P1", 0, 6, 2), Proceso("P2", 1, 4, 1), Proceso("P3", 2, 2, 0), Proceso("P4", 3, 3, 1)]
    #procesos = [Proceso("P1", 1, 1, 1)]
    Mostrar_Procesos = Mostrar_Procesos(procesos)
    Mostrar_Procesos.mainloop()


