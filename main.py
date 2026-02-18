import pygame
import copy
from matriz import *
from inicio import *

pygame.init()
pygame.mixer.init()

try:
    pygame.mixer.music.load("musica_relajante.mp3")    
    pygame.mixer.music.set_volume(0.2) 
    pygame.mixer.music.play(-1)
except:
    print("No se pudo cargar la música.")

# --- Pantalla principal ---
dimension_pantalla = pygame.display.set_mode((800,600))
pygame.display.set_caption("Mi Sudoku")

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


# --- INICIO DEL JUEGO ---

accion, nivel = mostrar_inicio()
if accion == "Salir":
    pygame.quit()
    quit()

# Configurar dificultad
if nivel == "Fácil":
    numeros_por_region = 5
elif nivel == "Medio":
    numeros_por_region = 4
else:
    numeros_por_region = 3

# --- GENERACIÓN INICIAL DEL TABLERO ---
tablero_lleno = generar_sudoku()          # 1. Generar solución
solucion = copy.deepcopy(tablero_lleno)   # 2. Guardar solución (memoria)
crear_puzzle(tablero_lleno, numeros_por_region) # 3. Borrar números
tablero_inicial = copy.deepcopy(tablero_lleno)  # 4. Guardar puzzle con huecos
matriz = copy.deepcopy(tablero_lleno)           # 5. Matriz de juego

errores_celdas = [[False]*9 for _ in range(9)]
regiones_completadas = [[False]*3 for _ in range(3)]

botones = {
    "Validar": pygame.Rect(500, 540, 230, 50),
    "Reiniciar": pygame.Rect(70, 540, 230, 50),
    "Terminar": pygame.Rect(500, 10, 230, 50),
    "Volver": pygame.Rect(250, 10, 230, 50),
    "Sonido": pygame.Rect(650, 75 ,120, 40)
}

celda_seleccionada = None
puntaje = 0
juego_terminado = False
musica_pausada = False

# --- LOOP PRINCIPAL ---
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            quit()

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = evento.pos
            
            # Selección de celda
            if 175 <= mouseX <= 625 and 75 <= mouseY <= 525:
                fila = (mouseY - 75) // 50
                columna = (mouseX - 175) // 50
                celda_seleccionada = (fila, columna)

            # --- BOTÓN VALIDAR ---
            if botones["Validar"].collidepoint(mouseX, mouseY):
                
                if es_victoria(matriz, solucion) and not juego_terminado:
                    print("¡GANASTE!")
                    puntaje += 81
                    juego_terminado = True                

                # 1. Restar puntos por errores (-1 c/u)
                cant_errores = calcular_errores(matriz, solucion)
                puntaje -= cant_errores
                
                # 2. Marcar errores en rojo (Actualizamos la matriz de errores)
                for i in range(9):
                    for j in range(9):
                        # Si la celda no está vacía y es incorrecta -> Error (True)
                        if matriz[i][j] != 0 and matriz[i][j] != solucion[i][j]:
                            errores_celdas[i][j] = True
                        else:
                            # Si es correcta o está vacía -> No es error (False)
                            errores_celdas[i][j] = False

                # 3. Sumar puntos por regiones (+9 c/u)
                for rf in range(3):
                    for rc in range(3):
                        if not regiones_completadas[rf][rc]:
                            fila_inicio = rf * 3
                            col_inicio = rc * 3
                            if region_esta_correcta(matriz, solucion, fila_inicio, col_inicio):
                                puntaje += 9
                                regiones_completadas[rf][rc] = True

                # 4. Victoria (+81)
                if es_victoria(matriz, solucion):
                    puntaje += 81

            # --- BOTÓN REINICIAR ---
            if botones["Reiniciar"].collidepoint(mouseX, mouseY):
                tablero_lleno = generar_sudoku()
                solucion = copy.deepcopy(tablero_lleno)
                crear_puzzle(tablero_lleno, numeros_por_region)
                tablero_inicial = copy.deepcopy(tablero_lleno)
                matriz = copy.deepcopy(tablero_lleno)
                
                puntaje = 0
                celda_seleccionada = None
                juego_terminado = False
                errores_celdas = [[False]*9 for _ in range(9)]
                regiones_completadas = [[False]*3 for _ in range(3)]

            # --- BOTÓN TERMINAR ---
            if botones["Terminar"].collidepoint(mouseX, mouseY):
                nick = pedir_nick(dimension_pantalla)
                guardar_puntaje(nick, puntaje)
                
                # Volver a Inicio
                accion, nivel = mostrar_inicio()
                if accion == "Salir":
                    pygame.quit()
                    quit()
                
                # Regenerar tablero al volver a jugar
                if nivel == "Fácil": numeros_por_region = 5
                elif nivel == "Medio": numeros_por_region = 4
                else: numeros_por_region = 3

                tablero_lleno = generar_sudoku()
                solucion = copy.deepcopy(tablero_lleno)
                crear_puzzle(tablero_lleno, numeros_por_region)
                tablero_inicial = copy.deepcopy(tablero_lleno)
                matriz = copy.deepcopy(tablero_lleno)
                puntaje = 0
                celda_seleccionada = None
                juego_terminado = False
                errores_celdas = [[False]*9 for _ in range(9)]
                regiones_completadas = [[False]*3 for _ in range(3)]

            # --- BOTÓN VOLVER ---
            if botones["Volver"].collidepoint(mouseX, mouseY):
                accion, nivel = mostrar_inicio()
                if accion == "Salir":
                    pygame.quit()
                    quit()

                if nivel == "Fácil": numeros_por_region = 5
                elif nivel == "Medio": numeros_por_region = 4
                else: numeros_por_region = 3

                tablero_lleno = generar_sudoku()
                solucion = copy.deepcopy(tablero_lleno)
                crear_puzzle(tablero_lleno, numeros_por_region)
                tablero_inicial = copy.deepcopy(tablero_lleno)
                matriz = copy.deepcopy(tablero_lleno)
                puntaje = 0
                celda_seleccionada = None
                juego_terminado = False
                errores_celdas = [[False]*9 for _ in range(9)]
                regiones_completadas = [[False]*3 for _ in range(3)]
        
        # --- BOTÓN SONIDO (ON/OFF) ---
            if botones["Sonido"].collidepoint(mouseX, mouseY):
                if musica_pausada:
                    pygame.mixer.music.unpause() # Reanudar
                    musica_pausada = False
                else:
                    pygame.mixer.music.pause()   # Pausar
                    musica_pausada = True

        # --- TECLADO (Escribir números) ---
        elif evento.type == pygame.KEYDOWN and celda_seleccionada:
            fila, col = celda_seleccionada
            # Solo si es una celda editable (vacía en el tablero inicial)
            if tablero_inicial[fila][col] == 0:
                if evento.key in (pygame.K_BACKSPACE, pygame.K_DELETE):
                    matriz[fila][col] = 0
                    errores_celdas[fila][col] = False # Borrar error si borro el número
                
                elif evento.unicode in "123456789":
                    numero = int(evento.unicode)
                    matriz[fila][col] = numero
                    # Reiniciamos el error visual hasta que vuelva a validar
                    errores_celdas[fila][col] = False 

    # --- DIBUJADO ---
    dimension_pantalla.blit(fondo_img, (0,0))
    dibujar_tablero(dimension_pantalla)
    
    # Pasamos las variables necesarias a dibujar_numeros
    dibujar_numeros(dimension_pantalla, matriz, tablero_inicial, errores_celdas)
    dibujar_seleccion(dimension_pantalla, celda_seleccionada, errores_celdas)
    
    # Verificar si el sudoku está lleno (para habilitar botón Terminar)
    sudoku_listo = True
    for fila in range(9):
        if 0 in matriz[fila]:
            sudoku_listo = False
            break

    dibujar_botones(dimension_pantalla, botones, sudoku_listo)
    dibujar_puntaje(dimension_pantalla, puntaje)

    pygame.display.update()