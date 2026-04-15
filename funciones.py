import pygame
import random


# ----- Funciones de pantalla de juego ----- #

# Cargar imágenes una sola vez
fondo_img = pygame.image.load("fondo_pantalla_juego.png")
fondo_img = pygame.transform.scale(fondo_img, (800, 600))
fondo_nick = pygame.image.load("fondo.sudoku.png")
fondo_nick = pygame.transform.scale(fondo_nick, (800, 600))

def pedir_nick(pantalla):
    '''
    DESCRIPCION:
        Loop de entrada de texto.
        Captura los eventos de teclado para que el usuario escriba su nombre.
        Maneha el borrado (Backspace) y la confirmacion (Enter).

    PARAMETROS:
        pantalla (pygame.Surface): La superficie principal donde se dibuja la interfaz.  

    RETORNA:
        str: El nombre ingresado por el usuario.
    '''

    fuente = pygame.font.Font(None, 50)
    nick = ""
    escribiendo = True

    while escribiendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nick != "":
                    escribiendo = False
                elif evento.key == pygame.K_BACKSPACE:
                    nick = nick[:-1]
                else:
                    if len(evento.unicode) == 1:
                        nick += evento.unicode

        pantalla.blit(fondo_nick, (0, 0))
        texto = fuente.render("Ingresá tu Nick:", True, (0, 0, 0))
        pantalla.blit(texto, (200, 200))
        
        x_nick = 200 + texto.get_width() + 20
        nick_texto = fuente.render(nick, True, (0, 0, 0))
        pantalla.blit(nick_texto, (x_nick, 200))

        pygame.display.update()

    return nick

def guardar_puntaje(nick, puntaje):
    '''
    DESCRIPCION:
        Abre el archivo 'puntajes.txt' en modo 'append' (agregar al final) y escribe el nuevo registro con formato 'Nombre : Puntaje'.
    
        PARAMETRO:
            nick (str): El nombre del jugador.
            puntaje (int): La cantidad de puntos obtenidos.
    '''
    with open("puntajes.txt", "a", encoding="utf-8") as archivo:
        archivo.write(f"{nick} : {puntaje}\n")

def dibujar_tablero(pantalla):
    '''
    DESCRIPCION:
        Dibuja la grilla del Sudoku.
        Usa lineas finas para las celdas individuales y lineas gruesas para separar las regiones 3x3, mejorando la visualizacion.

    PARAMETROS:
        pantalla (pygame.Surface): La superficie donde se dibujaran las lineas.
    '''
    color_linea_fina = (100, 100, 100)
    color_linea_gruesa = (0, 0, 0)
    tamaño_celdas = 50
    inicio_x = 175
    inicio_y = 75

    for i in range(10):
        # Líneas horizontales
        pygame.draw.line(pantalla, color_linea_fina, (inicio_x, inicio_y + i * tamaño_celdas), (inicio_x + tamaño_celdas*9, inicio_y + i * tamaño_celdas), 1)
        # Líneas verticales
        pygame.draw.line(pantalla, color_linea_fina, (inicio_x + i * tamaño_celdas, inicio_y), (inicio_x + i * tamaño_celdas, inicio_y + tamaño_celdas*9), 1)

    for i in range(0, 10, 3):
        pygame.draw.line(pantalla, color_linea_gruesa, (inicio_x, inicio_y + i * tamaño_celdas), (inicio_x + tamaño_celdas*9, inicio_y + i * tamaño_celdas), 4)
        pygame.draw.line(pantalla, color_linea_gruesa, (inicio_x + i * tamaño_celdas, inicio_y), (inicio_x + i * tamaño_celdas, inicio_y + tamaño_celdas*9), 4)

def dibujar_puntaje(pantalla, puntaje):
    '''
    DESCRIPCION:
        Renderiza el texto con el puntaje actual en la esquina superior izquierda.
        Utiliza una fuente de tamaño 50 y color negro para que sea bien visible.

    PARAMETROS:
        pantalla (Surface): La superficie de Pygame donde se dibujara el texto.
        puntaje (int): El numero entero que representa los puntos actuales del jugador.
     '''
    fuente = pygame.font.Font(None, 50)
    texto = fuente.render(f"Puntos: {puntaje}", True, (0, 0, 0))
    pantalla.blit(texto, (15, 15))

def dibujar_numeros(pantalla, matriz, tablero_inicial, errores_celdas):
    '''
    DESCRIPCION:
        Renderiza los numeros en cada celda con logica de colores:
        - NEGRO: Numeros fijos (del puzzle original).
        -AZUL: Numeros ingresados por el usuario.
        -ROJO: Numeros marcados como error tras validar.

    PARAMETROS:
        pantalla (pygame.Surface): Superficie de dibujo.
        matriz (list): La matriz de 9x9 con los numeros actuales del juego.
        tablero_inicial (list): La copia de la matriz original para sabeer que numeros son fijos.
        errores_celdas (list): Matriz de booleanos (True/False) indicando donde hay errores
    '''
    fuente = pygame.font.Font(None, 40)
    tamaño_celdas = 50
    inicio_x = 175
    inicio_y = 75

    for fila in range(9):
        for col in range(9):
            numero = matriz[fila][col]
            if numero != 0:
                # Prioridad de colores:
                if errores_celdas[fila][col]:
                    color = (255, 0, 0)       # Rojo: Error validado
                elif tablero_inicial[fila][col] != 0:
                    color = (0, 0, 0)         # Negro: Número fijo original
                else:
                    color = (0, 0, 255)       # Azul: Ingresado por usuario

                texto = fuente.render(str(numero), True, color)
                x = inicio_x + col * tamaño_celdas + tamaño_celdas//2 - texto.get_width()//2
                y = inicio_y + fila * tamaño_celdas + tamaño_celdas//2 - texto.get_height()//2
                pantalla.blit(texto, (x, y))

def dibujar_seleccion(pantalla, celda, errores_celdas):
    '''
    DESCRIPCION:
        Dibuja un recuadro de color sobre la celda que el usuario tiene seleccionada.
        - VERDE: Seleccion normal.
        - ROJO: Si selecciona una celda que contiene un error validado.

    PARAMETROS:
        pantalla (pygame.Surface): Superficie de dibujo.
        celda (tuple): Coordenadas (fila, columna) de la celda seleccionada. Puede ser None.
        errores_celdas (list): Matriz de booleanos para verificar si la celda es un error.
    '''
    if celda:
        fila, col = celda
        color = (0, 255, 0) # Verde por defecto
        if errores_celdas[fila][col]:
            color = (255, 0, 0) # Rojo si selecciono un error
        
        pygame.draw.rect(pantalla, color, (175 + col*50, 75 + fila*50, 50, 50), 3)

def dibujar_botones(pantalla, botones, sudoku_listo):
    '''
    DESCRIPCION:
        Itera sobre el diccionario de botones y los dibuja en pantalla.
        Controla la visibilidad del boton 'Terminar', que solo aparece cuando el tablero esta lleno.
    
    PARAMETROS:
        pantalla (pygame.Surface): Superficie de dibujo.
        botones (dict): Diccionario que contiene los objetos pygame.Rect de cada botón.
        sudoku_listo (bool): True si el tablero no tiene ceros (está lleno), False si falta completar.
    '''
    fuente = pygame.font.Font(None, 40)
    BLANCO = (255,255,255)
    NEGRO = (0,0,0)

    for texto, rect in botones.items():
        if texto == "Terminar" and not sudoku_listo:
            continue

        pygame.draw.rect(pantalla, BLANCO, rect)
        texto_render = fuente.render(texto, True, NEGRO)
        pantalla.blit(texto_render, (rect.x + 20, rect.y + 10))


# ----- Funciones de matriz -----#

def crear_tablero_vacio():
    '''
    DESCRIPCION:
        Genera una matriz de 9x9 inicializada con ceros.
        El '0' representa una celda vacia en el sudoku.

    RETORNA:
        list[list[int]]: Una lista de 9 listas con 9 ceros cada una.
    '''
    return [[0 for _ in range(9)] for _ in range(9)]

def es_valido(tablero, fila, col, num):
    """
    DESCRIPCION:
        Verifica si colocar un numero en una posicion especifica cumple con las 3 reglas del sudoku:
        1. No repetirse en la misma fila.
        2. No repetirse en la misma columna.
        3. No repetirse en la sub-region de 3x3.
    
    PARAMETROS:
        tablero (list): La matriz de juego actual.
        fila (int): Indica de la fila (0-8).
        col (int): Indice de la columna (0-8).
        num (int): El numero a validar (1-9).

    RETORNA:
        bool: True si el movimiento es valido, False si rompe alguna regla.
    """
    # Fila
    if num in tablero[fila]:
        return False
    # Columna
    for i in range(9):
        if tablero[i][col] == num:
            return False
    # Región
    inicio_fila = (fila // 3) * 3
    inicio_col = (col // 3) * 3
    for i in range(inicio_fila, inicio_fila + 3):
        for j in range(inicio_col, inicio_col + 3):
            if tablero[i][j] == num:
                return False
    return True

def resolver(tablero):
    """
    DESCRIPICION:
        Algoritmo de 'Backtracking' recursivo.
        Busca celdas vacias y prueba numeros aleatorios.  Si llega a un callejon sin salida, retrocede (backtracks) para probar otro camino.

    PARAMETROS:
        tablero (list): La matriz que se intentara resolver in-place.

    RETORNA:
        bool: True si encontro una solucion completa, False si no tiene solucion.
    """
    for i in range(9):
        for j in range(9):
            if tablero[i][j] == 0:
                numeros = list(range(1, 10))
                random.shuffle(numeros)
                for num in numeros:
                    if es_valido(tablero, i, j, num):
                        tablero[i][j] = num
                        if resolver(tablero):
                            return True
                        tablero[i][j] = 0
                return False
    return True

def generar_sudoku():
    """
    DESCRIPCION:
        Funcion principal para crear un sudoku nuevo.
        Crea un tablero vacio y lo resuelve completamente usando backtracking para obtener una solucion valida y aleatoria.

    Retorna:
        list: Una matriz 9x9 completa y valida.
    """
    tablero = crear_tablero_vacio()
    resolver(tablero)
    return tablero

def crear_puzzle(tablero, pistas_por_region):
    """
    DESCRIPCION:
        Toma un tablero resuelto y elimina numeros para convertirlo en un juego.
        Recorre cada region de 3x3 y deja visibles solo la cantidad de pistas indicada, poniendo el resto en 0.

    PARAMETROS:
        tablero (list): El tablero completo (se modifica in-place).
        pistas_por_region (int): Cantidad de numeros a mantener por cada subcuadro.

    RETORNA: 
        list: El tablero modificado con huecos (ceros).
    """
    for region_fila in [0, 3, 6]:
        for region_col in [0, 3, 6]:
            posiciones = []
            for i in range(region_fila, region_fila + 3):
                for j in range(region_col, region_col + 3):
                    posiciones.append((i, j))
            
            random.shuffle(posiciones)
            
            # Borramos los números que sobran
            for k in range(pistas_por_region, 9):
                fila, col = posiciones[k]
                tablero[fila][col] = 0
    return tablero

def validar_numero(tablero, fila, col, num):
    """
    DESCRIPCION:
        Funcion puente para la interfaz grafica.
        Permite validar si un numero es correcto ignorando que ese mismo numero ya pueda estar escrito temporalmente en la celda (lo borra, valida y lo restaura).

    RETORNA:
        bool: True si el numero es logicamente valido en esa posicion.
    """
    valor_actual = tablero[fila][col]
    tablero[fila][col] = 0
    es_correcto = es_valido(tablero, fila, col, num)
    tablero[fila][col] = valor_actual
    return es_correcto

# ----- FUNCIONES DE PUNTAJE (Comparando con Solución) ----- #

def calcular_errores(tablero, solucion):
    """
    DESCRIPCION:
        Compara el tablero actual con la solucion exacta.
        Cuenta cuantas celdas tienen un numero diferente al de la solucion (ignora las celdas vacias/ceros).
    
    PARAMETROS:
        tablero (list): Estado actual del juego.
        solucion (list): La matriz resuelta perfecta.

    RETORNA:
        int: Cantidad total de errores encontrados.
    """
    cantidad = 0
    for i in range(9):
        for j in range(9):
            if tablero[i][j] != 0 and tablero[i][j] != solucion[i][j]:
                cantidad += 1
    return cantidad

def region_esta_correcta(tablero, solucion, fila_inicio, col_inicio):
    """
    DESCRIPCION:
        Verifica si una sub-region de 3x3 especifica esta completamente llena y coincide exactamente con la solucion.

    PARAMETROS:
        fila_inicio, col_inicio (int): Coordenadas superiores izquierdas de la region.
    
    RETORNA:
        bool: True si la region esta completa y perfecta.
    """

    for i in range(fila_inicio, fila_inicio + 3):
        for j in range(col_inicio, col_inicio + 3):
            if tablero[i][j] != solucion[i][j]:
                return False
    return True

def es_victoria(tablero, solucion):
    """
    DESCRIPCION:
        Verifica si el jugador ha ganado el juego.
        Compara celda por celda todo el tablero con la solucion.

    RETORNA:
        bool: True si el tablero es identico a la solucion.
    """
    for i in range(9):
        for j in range(9):
            if tablero[i][j] != solucion[i][j]:
                return False
    return True

# ----- Funciones de pantalla de inicio ----- #

fondo = pygame.image.load("fondo.sudoku.png")
fondo = pygame.transform.scale(fondo, (800, 600))
fondo_pantalla_juego = pygame.image.load("fondo_pantalla_juego.png")

def cargar_puntajes():

    """
    DESCRIPCION:
        Lee el archivo 'puntajes.txt'.
        Procesa cada linea separando el nombre y el puntaje.

    RETORNA:
        list: Lista de tuplas (nombre, puntaje) con los datos convertidos.
    """

    puntajes = []

    with open("puntajes.txt", "r", encoding="utf-8") as archivo:
        for linea in archivo:
            if ":" in linea:
                nombre, puntaje = linea.strip().split(" : ")
                puntaje = int(puntaje)  
                puntajes.append((nombre, puntaje))

    return puntajes

def mejores_cinco(puntajes):
    
    """
    DESCRIPCION:
        Ordena las listas de puntajes de matoy a menor y recorta la lista para quedarse solo con los Top 5.
        Utiliza una funcion lambda como clave de ordenamiento.

    PARAMETROS:
        puntajes (list): Lista de tuplas con formato (nombre, puntaje).


    RETORNA:
        list: Una nueva lita con los 5 puntajes mas altos ordenados.
    """

    puntajes_ordenados = sorted(puntajes, key=lambda x: x[1], reverse=True)
    return puntajes_ordenados[:5]

def mostrar_puntajes(pantalla):
    
    """
    DESCRIPCION:
        Despliega una pantalla que muestra los mejores 5 puntajes guardados.
        Muestra:
            - Fondo del juego y recuadro blanco.
            - Título "Mejores 5 puntajes".
            - Lista de nombres y puntajes.
            - Botón "Volver".

        Esta función mantiene su propio loop hasta que se hace clic en VOLVER.

    PARAMETROS:
        pantalla (Surface): La superficie de Pygame donde se dibujara todo.

    RETORNA:
        None: No devuelve ningun valor, solo modifica la pantalla.
    """

    fondo = pygame.image.load("fondo.sudoku.png")
    fondo = pygame.transform.scale(fondo, (800, 600))

    fuente = pygame.font.Font(None, 60)
    fuente_chica = pygame.font.Font(None, 40)

    puntajes = mejores_cinco(cargar_puntajes())

    volver_boton = pygame.Rect(300, 520, 200, 50)

    en_puntajes = True
    while en_puntajes:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if volver_boton.collidepoint(evento.pos):
                    en_puntajes = False  # vuelve a la pantalla de inicio

        # DIBUJAR FONDO
        pantalla.blit(fondo, (0, 0))
        pygame.draw.rect(pantalla, (255, 255, 255), (100, 30, 600, 470))

        # Título
        titulo = fuente.render("Mejores 5 puntajes", True, (255, 255, 255))
        pygame.draw.rect(pantalla, (0, 0, 0), (130, 50, 540, 90))
        pantalla.blit(titulo, (210, 75))
        

        # Listado
        y = 160
        if puntajes:
            for nombre, pts in puntajes:
                texto = fuente_chica.render(f"{nombre}: {pts}", True, (0, 0, 0))
                pantalla.blit(texto, (250, y))
                y += 50
        else:
            texto = fuente_chica.render("No hay puntajes guardados", True, (0, 0, 0))
            pantalla.blit(texto, (200, 250))

        # Botón volver
        pygame.draw.rect(pantalla, (255, 255, 255), volver_boton)
        texto_volver = fuente_chica.render("Volver", True, (0, 0, 0))
        pantalla.blit(texto_volver, (volver_boton.x + 50, volver_boton.y + 10))

        pygame.display.update()

def mostrar_inicio():

    """
    DESCRIPCION:
        Pantalla del Menu Principal.
        Maneja la navegacion inicial del juego.
        Permite seleccionar dificultad (Facil/Medio/Dificil) ciclicamente.

    RETORNA:
        tuple (accion_elegida, nivel_seleccionado)
        Ejemplo: ("Jugar", "Medio") o ("Salir", "Facil")
    """

    pantalla = pygame.display.set_mode((800,600))
    pygame.display.set_caption("Sudoku")

    # Cargar fondo
    fondo = pygame.image.load("fondo.sudoku.png")
    fondo = pygame.transform.scale(fondo, (800, 600))

    blanco = (255, 255, 255)
    negro = (0,0,0)
    fuente = pygame.font.Font(None, 40)

    # Botones principales
    botones = {
        "Nivel": (50, 200, 200, 50),
        "Jugar": (50, 270, 200, 50),
        "Ver Puntajes": (50, 340, 200, 50),
        "Salir": (50, 410, 200, 50)
    }

    nivel = "Fácil"  # nivel por defecto

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "Salir", nivel

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                mouse_pos = evento.pos
                for texto, coord in botones.items():
                    rect = pygame.Rect(coord)
                    if rect.collidepoint(mouse_pos):
                        if texto == "Jugar":
                            return "Jugar", nivel
                        elif texto == "Nivel":
                            # Cambiar nivel con cada clic
                            if nivel == "Fácil":
                                nivel = "Medio"
                            elif nivel == "Medio":
                                nivel = "Difícil"
                            else:
                                nivel = "Fácil"
                        elif texto == "Ver Puntajes":
                            mostrar_puntajes(pantalla)
                        elif texto == "Salir":
                            return "Salir", nivel

        # Dibujar fondo y botones
        pantalla.blit(fondo, (0,0))
        pygame.draw.rect(pantalla, blanco, (30, 130, 240, 350))
        for texto, coord in botones.items():
            pygame.draw.rect(pantalla, negro, coord)
            texto_render = fuente.render(texto, True, blanco)
            pantalla.blit(texto_render, (coord[0] + 20, coord[1] + 10))

        # Mostrar nivel actual
        nivel_render = fuente.render(f"Nivel: {nivel}", True, negro)
        pantalla.blit(nivel_render, (75, 150))

        pygame.display.flip()
