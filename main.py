import pygame
import copy
from funciones import *

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