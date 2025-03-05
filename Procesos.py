class Proceso:
    def __init__(self, nombre, tiempo_llegada, rafaga, prioridad):
        self.nombre = nombre 
        self.tiempo_llegada = tiempo_llegada
        self.rafaga = rafaga
        self.prioridad = prioridad
        self.tiempo_final = 0
        self.tiempo_inicio = 0
        

    def crear_proceso(self):
        self.nombre = input("Ingrese el nombre del proceso: ")
        self.tiempo_llegada = int(input("Ingrese el tiempo de llegada del proceso: "))
        self.rafaga = int(input("Ingrese la rafaga del proceso: "))

def crear_procesos():
    procesos = [] #Lista que me permitira almacenar los procesos
    cantidad_procesos = int(input("Cuantos procesos desea crear: ")) #Defino la cantidad de procesos que se crearan
    for i in range(cantidad_procesos): #Recorro la cantidad de procesos que se crearan
        proceso = Proceso("", 0, 0) #Creo un objeto de la clase Procesos
        proceso.crear_proceso() #Llamo al metodo crear_proceso
        procesos.append(proceso) #Agrego el proceso a la lista
    return procesos

def Fifo(procesos): #Funcion que implementa el algoritmo FIFO

    fifo_list = [] #Lista que me permitira almacenar los procesos

    for proceso in procesos: #Recorro la lista de procesos
        fifo_list.append(proceso) #Agrego el proceso a la lista

    tiempo_ejecucion = 0 #Me permite conocer el tiempo de ejecucion en le que me encuentro
    tiempo_espera = 0 #Me permite conocer el tiempo de espera de todos los procesos
    tiempo_sistema = 0 #Me permite conocer el tiempo de sistema de todos los procesos
    total = 0 #Me permite conocer el tiempo total de ejecucion de todos los procesos

    for proceso in fifo_list: #Recorro la lista de procesos
        total += proceso.rafaga #Sumo el tiempo de ejecucion de cada proceso 

    while (total > 0): #Mientras el tiempo total sea mayor a 0

        pasar_segundo = True #Variable que me permite saber si puedo avanzar un segundo en el tiempo de ejecucion

        for proceso in fifo_list:

            if(tiempo_ejecucion >= proceso.tiempo_llegada): #Verifico si el proceso ya existe )

                pasar_segundo = False

                proceso.tiempo_final = proceso.rafaga + tiempo_ejecucion #Calculo el tiempo final del proceso
                    
                tiempo_espera += tiempo_ejecucion - proceso.tiempo_llegada #Calculo el tiempo de espera
                tiempo_ejecucion += proceso.rafaga #Calculo el tiempo de ejecucion
                
                proceso.tiempo_inicio = tiempo_ejecucion - proceso.rafaga #Calculo el tiempo de inicio del proceso

                tiempo_sistema = tiempo_ejecucion - proceso.tiempo_llegada #Calculo el tiempo de sistema
                    
                total -= proceso.rafaga #Resto el tiempo de ejecucion del proceso al tiempo total
                    
                fifo_list.remove(proceso) #Elimino el proceso de la lista

                break

        if pasar_segundo:
            tiempo_ejecucion += 1

    return procesos, tiempo_espera/len(procesos), tiempo_sistema/len(procesos)

def SJF(procesos): #Funcion que implementa el algoritmo SJF

    sjf_list = [] #Lista que me permitira almacenar los procesos

    for proceso in procesos: #Recorro la lista de procesos
        sjf_list.append(proceso) #Agrego el proceso a la lista

    sjf_list.sort(key=lambda x: x.rafaga) #Ordeno la lista de procesos por rafaga

    return Fifo(sjf_list) #Llamo a la funcion FIFO  

def Prioridad(procesos): #Funcion que implementa el algoritmo de prioridad

    prioridad_list = [] #Lista que me permitira almacenar los procesos

    for proceso in procesos: #Recorro la lista de procesos
        prioridad_list.append(proceso) #Agrego el proceso a la lista

    prioridad_list.sort(key=lambda x: x.prioridad) #Ordeno la lista de procesos por rafaga

    return Fifo(prioridad_list) #Llamo a la funcion

    #Nuevo Comentario

#Ejemplo
#procesos = [Proceso("P1", 0, 6, 2), Proceso("P2", 1, 4, 1), Proceso("P3", 2, 2, 0), Proceso("P4", 3, 3, 1)]
#procesos = Fifo(procesos)[0]
#for proceso in procesos:
#    print(f"Proceso: {proceso.nombre} - Tiempo de llegada: {proceso.tiempo_llegada} - Rafaga: {proceso.rafaga} - Tiempo de inicio: {proceso.tiempo_inicio} - Tiempo final: {proceso.tiempo_final}")




