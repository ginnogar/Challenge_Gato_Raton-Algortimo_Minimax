import tkinter as tk # Importa la librería tkinter para crear interfaces gráficas.
import random # Importa la librería random para generar posiciones aleatorias.

# Variables globales
tamano_tablero = 5 # Tamaño del tablero (5x5).
tamano_celda = 100 # Tamaño de cada celda del tablero en píxeles.
contador_turnos = 0 # Contador de turnos.
max_turnos = 4 # Número máximo de turnos antes de que el juego termine en empate.
pos_gato = None # Posición del gato en el tablero (se inicializa más tarde).
pos_raton = None # Posición del ratón en el tablero (se inicializa más tarde).
canvas = None # Canvas de tkinter para dibujar el tablero y las piezas (se inicializa más tarde).
root = None # Ventana principal de tkinter (se inicializa más tarde).
turno_raton = True # Variable que indica si es el turno del ratón.

def dibujar_tablero(): # Función para dibujar el tablero del juego.
    for fila in range(tamano_tablero): # Itera sobre las filas del tablero.
        for columna in range(tamano_tablero): # Itera sobre las columnas del tablero.
            color = "white" if (fila + columna) % 2 == 0 else "black" # Alterna colores blanco y negro para las celdas.
            canvas.create_rectangle( # Dibuja un rectángulo que representa una celda del tablero.
                columna * tamano_celda,
                fila * tamano_celda,
                (columna + 1) * tamano_celda,
                (fila + 1) * tamano_celda,
                fill=color # Color de la celda.
            )

def posicion_aleatoria(): # Función para generar una posición aleatoria dentro del tablero.
    return random.randint(0, tamano_tablero - 1), random.randint(0, tamano_tablero - 1) # Devuelve una tupla con una posición aleatoria.

def dibujar_piezas(): # Función para borrar las piezas anteriores y dibujar las nuevas posiciones del gato y el ratón.
    canvas.delete("pieza") # Elimina todas las piezas dibujadas anteriormente.

    # Dibuja el gato
    canvas.create_rectangle(
        pos_gato[1] * tamano_celda, # Coordenada x del rectángulo del gato.
        pos_gato[0] * tamano_celda, # Coordenada y del rectángulo del gato.
        (pos_gato[1] + 1) * tamano_celda, # Coordenada x del borde derecho del rectángulo del gato.
        (pos_gato[0] + 1) * tamano_celda, # Coordenada y del borde inferior del rectángulo del gato.
        fill="orange", # Color del gato.
        tags="pieza" # Etiqueta para identificar la pieza.
    )

    # Dibuja el ratón
    canvas.create_rectangle(
        pos_raton[1] * tamano_celda, # Coordenada x del rectángulo del ratón.
        pos_raton[0] * tamano_celda, # Coordenada y del rectángulo del ratón.
        (pos_raton[1] + 1) * tamano_celda, # Coordenada x del borde derecho del rectángulo del ratón.
        (pos_raton[0] + 1) * tamano_celda, # Coordenada y del borde inferior del rectángulo del ratón.
        fill="grey", # Color del ratón.
        tags="pieza" # Etiqueta para identificar la pieza.
    )

def mover_raton(event): # Función para mover el ratón en respuesta a la entrada del usuario.
    global contador_turnos, pos_raton, turno_raton # Declaración de variables globales que se usarán y modificarán.

    if not turno_raton: # Si no es el turno del ratón, no hacer nada.
        return

    if contador_turnos >= max_turnos: # Si se alcanzó el número máximo de turnos, finaliza el juego en empate.
        finalizar_juego("El Juego termina en un empate")
        return

    tecla = event.keysym # Captura la tecla presionada.
    nueva_pos = list(pos_raton) # Crea una lista con la posición actual del ratón.
    
    # Actualiza la posición del ratón según la tecla presionada.
    if tecla == "w": 
        nueva_pos[0] -= 1
    elif tecla == "s":
        nueva_pos[0] += 1
    elif tecla == "a":
        nueva_pos[1] -= 1
    elif tecla == "d":
        nueva_pos[1] += 1

    # Validar el movimiento del ratón
    if 0 <= nueva_pos[0] < tamano_tablero and 0 <= nueva_pos[1] < tamano_tablero: # Comprueba que la nueva posición esté dentro del tablero.
        pos_raton = tuple(nueva_pos) # Actualiza la posición del ratón.
        contador_turnos += 1 # Incrementa el contador de turnos.
        dibujar_piezas() # Redibuja las piezas en sus nuevas posiciones.
        turno_raton = False # Cambia el turno al gato.

        # Verificar si el ratón ha escapado
        if contador_turnos >= max_turnos: # Si se alcanzó el número máximo de turnos, finaliza el juego en empate.
            finalizar_juego("El Juego termina en un empate")
            return

        # Mover el gato
        root.after(500, mover_gato) # Llama a la función para mover el gato después de un retraso de 500 milisegundos.

def mover_gato(): # Función para mover el gato usando el algoritmo minimax.
    global pos_gato, turno_raton # Declaración de variables globales que se usarán y modificarán.

    def distancia_manhattan(pos1, pos2): # Función que calcula la distancia de Manhattan entre dos posiciones.
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) # Devuelve la distancia de Manhattan.

    def evaluar_posicion(pos_gato, pos_raton): # Función que evalúa la posición del gato y el ratón.
        if pos_gato == pos_raton: # Si el gato y el ratón están en la misma posición, el valor es infinito (gato atrapa al ratón).
            return float('inf')
        else:
            return -distancia_manhattan(pos_gato, pos_raton) # Devuelve la distancia negativa (cuanto más cerca, mejor para el gato).

    def minimax(pos_gato, pos_raton, profundidad, es_maximizador): # Función del algoritmo minimax para encontrar el mejor movimiento.
        if profundidad == 3 or pos_gato == pos_raton: # Si se alcanza la profundidad máxima o el gato atrapa al ratón, evalúa la posición.
            return evaluar_posicion(pos_gato, pos_raton)
        
        movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)] # Lista de movimientos posibles.
        if es_maximizador: # Si es el turno del gato (maximizador).
            max_eval = -float('inf') # Inicializa el valor máximo.
            for mov in movimientos: # Itera sobre los movimientos posibles.
                nueva_pos = (pos_gato[0] + mov[0], pos_gato[1] + mov[1]) # Calcula la nueva posición del gato.
                if 0 <= nueva_pos[0] <tamano_tablero and 0 <= nueva_pos[1] <tamano_tablero: # Comprueba que la nueva posición esté dentro del tablero.
                    eval = minimax(nueva_pos, pos_raton, profundidad - 1, False) # Llama recursivamente a minimax para evaluar la nueva posición.
                    max_eval = max(max_eval, eval) # Actualiza el valor máximo.
            return max_eval # Devuelve el valor máximo.
        else: # Si es el turno del ratón (minimizador).
            min_eval = float('inf') # Inicializa el valor mínimo.
            for mov in movimientos: # Itera sobre los movimientos posibles.
                nueva_pos = (pos_raton[0] + mov[0], pos_raton[1] + mov[1]) # Calcula la nueva posición del ratón.
                if 0 <= nueva_pos[0] < tamano_tablero and 0 <= nueva_pos[1] <tamano_tablero: # Comprueba que la nueva posición esté dentro del tablero.
                    eval = minimax(pos_gato, nueva_pos, profundidad - 1, True) # Llama recursivamente a minimax para evaluar la nueva posición.
                    min_eval = min(min_eval, eval) # Actualiza el valor mínimo.
            return min_eval # Devuelve el valor mínimo.

    def mejor_movimiento_gato(pos_gato, pos_raton): # Función para encontrar el mejor movimiento para el gato.
        movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)] # Lista de movimientos posibles.
        mejor_movimiento = None # Inicializa la mejor posición como None.
        mejor_valor = -float('inf') # Inicializa el mejor valor como negativo infinito.

        for mov in movimientos: # Itera sobre los movimientos posibles.
            nueva_pos = (pos_gato[0] + mov[0], pos_gato[1] + mov[1]) # Calcula la nueva posición del gato.
            if 0 <= nueva_pos[0] < tamano_tablero and 0 <= nueva_pos[1] < tamano_tablero: # Comprueba que la nueva posición esté dentro del tablero.
                valor = minimax(nueva_pos, pos_raton, 3, False)  # Evalúa la nueva posición usando minimax con profundidad 3.
                if valor > mejor_valor: # Si el valor es mejor que el mejor valor encontrado.
                    mejor_valor = valor # Actualiza el mejor valor.
                    mejor_movimiento = nueva_pos # Actualiza la mejor posición.

        return mejor_movimiento # Devuelve la mejor posición encontrada.

    mejor_movimiento = mejor_movimiento_gato(pos_gato, pos_raton) # Encuentra el mejor movimiento para el gato.
    if mejor_movimiento: # Si se encuentra un mejor movimiento.
        pos_gato = mejor_movimiento # Actualiza la posición del gato.

    dibujar_piezas() # Redibuja las piezas en sus nuevas posiciones.
    turno_raton = True # Cambia el turno al ratón.

    # Verificar si el gato atrapa al ratón
    if pos_gato == pos_raton: # Si el gato y el ratón están en la misma posición.
        finalizar_juego("El Gato atrapo al Ratón") # Finaliza el juego con el mensaje de que el gato atrapó al ratón.
    elif contador_turnos >= max_turnos: # Si se alcanzó el número máximo de turnos.
        finalizar_juego("El Juego termina en un empate") # Finaliza el juego con el mensaje de empate.


def finalizar_juego(mensaje): # Función para mostrar un mensaje de finalización del juego y desactivar las teclas.
    canvas.create_text( # Crea un texto en el canvas.
        tamano_tablero * tamano_celda / 2, # Coordenada x del texto.
        tamano_tablero * tamano_celda / 2, # Coordenada y del texto.
        text=mensaje, # Mensaje de finalización del juego.
        font=("Arial", 24), # Fuente del texto.
        fill="red" # Color del texto.
    )
    root.unbind("<Up>") # Desactiva la tecla de flecha arriba.
    root.unbind("<Down>") # Desactiva la tecla de flecha abajo.
    root.unbind("<Left>") # Desactiva la tecla de flecha izquierda.
    root.unbind("<Right>") # Desactiva la tecla de flecha derecha.

def main(): # Función principal para configurar la ventana principal y el tablero.
    global root, canvas, pos_gato, pos_raton # Declaración de variables globales que se usarán y modificarán.

    root = tk.Tk() # Crea la ventana principal.
    root.title("Gato y Ratón") # Establece el título de la ventana.

    canvas = tk.Canvas(root, width=tamano_tablero * tamano_celda, height=tamano_tablero * tamano_celda) # Crea un canvas de tkinter con el tamaño del tablero.
    canvas.pack() # Empaqueta el canvas en la ventana principal.

    dibujar_tablero() # Llama a la función para dibujar el tablero.

    pos_gato = posicion_aleatoria() # Genera una posición aleatoria para el gato.
    pos_raton = posicion_aleatoria() # Genera una posición aleatoria para el ratón.

    while pos_gato == pos_raton: # Asegura que el gato y el ratón no estén en la misma posición inicial.
        pos_raton = posicion_aleatoria() # Genera una nueva posición aleatoria para el ratón.

    dibujar_piezas() # Llama a la función para dibujar las piezas en sus posiciones iniciales.

    root.bind("<w>", mover_raton) # Asigna la tecla "w" para mover el ratón hacia arriba.
    root.bind("<s>", mover_raton) # Asigna la tecla "s" para mover el ratón hacia abajo.
    root.bind("<a>", mover_raton) # Asigna la tecla "a" para mover el ratón hacia la izquierda.
    root.bind("<d>", mover_raton) # Asigna la tecla "d" para mover el ratón hacia la derecha.

    root.mainloop() # Inicia el bucle principal de la interfaz gráfica.

if __name__ == "__main__": # Comprueba si el script se está ejecutando directamente.
    main() # Llama a la función principal.
