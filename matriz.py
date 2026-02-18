import random

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

# --- FUNCIONES DE PUNTAJE (Comparando con Solución) ---

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