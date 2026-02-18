import pygame

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