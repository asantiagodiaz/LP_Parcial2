"""
Parser CYK (Cocke-Younger-Kasami) para operaciones de calculadora.

El algoritmo CYK requiere que la gramatica este en Forma Normal
de Chomsky (FNC), donde cada produccion es:
  A -> BC  (dos no terminales)
  A -> a   (un terminal)

Gramatica original de la calculadora:
  E -> E + T | E - T | T
  T -> T * F | T / F | F
  F -> ( E ) | num

Primero eliminamos producciones unitarias (E->T, T->F):
  E -> E + T | E - T | T * F | T / F | ( E ) | num
  T -> T * F | T / F | ( E ) | num
  F -> ( E ) | num

Luego convertimos a FNC:
  E  -> E A1 | E A2 | T A3 | T A4 | L A5 | num
  T  -> T A3 | T A4 | L A5 | num
  F  -> L A5 | num
  A1 -> P T          (representa: + T)
  A2 -> M T          (representa: - T)
  A3 -> S F          (representa: * F)
  A4 -> D F          (representa: / F)
  A5 -> E R          (representa: E ))
  P  -> +
  M  -> -
  S  -> *
  D  -> /
  L  -> (
  R  -> )
"""


# Gramatica en FNC
# Cada produccion se almacena como: no_terminal -> lista de alternativas
# Cada alternativa es una tupla de 1 elemento (terminal) o 2 elementos (no terminales)
GRAMATICA = {
    'E':  [('E', 'A1'), ('E', 'A2'), ('T', 'A3'), ('T', 'A4'), ('L', 'A5'), ('num',)],
    'T':  [('T', 'A3'), ('T', 'A4'), ('L', 'A5'), ('num',)],
    'F':  [('L', 'A5'), ('num',)],
    'A1': [('P', 'T')],
    'A2': [('M', 'T')],
    'A3': [('S', 'F')],
    'A4': [('D', 'F')],
    'A5': [('E', 'R')],
    'P':  [('+',)],
    'M':  [('-',)],
    'S':  [('*',)],
    'D':  [('/',)],
    'L':  [('(',)],
    'R':  [(')',)],
}


def tokenizar(expresion):
    """Convierte una cadena como '3 + 5 * 2' en una lista de tokens"""
    tokens = []
    i = 0
    while i < len(expresion):
        if expresion[i].isspace():
            i += 1
        elif expresion[i].isdigit():
            j = i
            while j < len(expresion) and (expresion[j].isdigit() or expresion[j] == '.'):
                j += 1
            valor = float(expresion[i:j]) if '.' in expresion[i:j] else int(expresion[i:j])
            tokens.append(('num', valor))
            i = j
        elif expresion[i] in '+-*/()':
            tokens.append((expresion[i], None))
            i += 1
        else:
            raise ValueError(f"Caracter inesperado: '{expresion[i]}'")
    return tokens


def cyk_parse(tokens):
    """
    Algoritmo CYK para reconocer y evaluar expresiones.
    Retorna (exito, tabla) donde exito es True si la cadena es valida.
    """
    n = len(tokens)
    if n == 0:
        return False, None

    # tabla[i][j] = diccionario {no_terminal: (produccion, punto_division)}
    # punto_division = -1 si es terminal, o k si es A -> BC con division en k
    tabla = [[{} for _ in range(n)] for _ in range(n)]

    # Paso 1: llenar la diagonal (producciones A -> a)
    for i in range(n):
        tipo_token = tokens[i][0]  # 'num', '+', '-', etc.
        for nt, producciones in GRAMATICA.items():
            for prod in producciones:
                if len(prod) == 1 and prod[0] == tipo_token:
                    tabla[i][i][nt] = (prod, -1)

    # Paso 2: llenar el resto de la tabla
    for longitud in range(2, n + 1):          # longitud del substring
        for i in range(n - longitud + 1):     # posicion inicial
            j = i + longitud - 1              # posicion final
            for k in range(i, j):             # punto de division
                for nt, producciones in GRAMATICA.items():
                    if nt in tabla[i][j]:
                        continue  # ya encontramos una derivacion para este NT
                    for prod in producciones:
                        if len(prod) == 2:
                            B, C = prod
                            if B in tabla[i][k] and C in tabla[k+1][j]:
                                tabla[i][j][nt] = (prod, k)

    exito = 'E' in tabla[0][n - 1]
    return exito, tabla


def evaluar(tabla, tokens, i, j, simbolo):
    """Evalua el resultado a partir de la tabla CYK"""
    info = tabla[i][j][simbolo]
    prod, k = info

    # Caso terminal
    if k == -1:
        if prod[0] == 'num':
            return tokens[i][1]
        return None

    B, C = prod

    # Caso parentesis: X -> L A5, donde A5 -> E R
    if B == 'L' and C == 'A5':
        # Dentro de A5 esta E y R, necesitamos evaluar E
        info_a5 = tabla[k + 1][j]['A5']
        prod_a5, k_a5 = info_a5
        return evaluar(tabla, tokens, k + 1, k_a5, 'E')

    # Caso operacion binaria: X -> Y Ak (donde Ak = A1, A2, A3 o A4)
    if C in ('A1', 'A2', 'A3', 'A4'):
        valor_izq = evaluar(tabla, tokens, i, k, B)
        # Ak -> OP Z, extraer Z
        info_ak = tabla[k + 1][j][C]
        prod_ak, k_ak = info_ak
        _, z_sym = prod_ak
        valor_der = evaluar(tabla, tokens, k_ak + 1, j, z_sym)

        if C == 'A1':
            return valor_izq + valor_der
        elif C == 'A2':
            return valor_izq - valor_der
        elif C == 'A3':
            return valor_izq * valor_der
        elif C == 'A4':
            if valor_der == 0:
                print("  Advertencia: division por cero")
                return float('inf')
            return valor_izq / valor_der

    return None


def cyk_reconocer(tokens):
    """Version simplificada que solo verifica si la expresion es valida (sin evaluar)"""
    n = len(tokens)
    if n == 0:
        return False

    # Usar conjuntos en vez de diccionarios (mas rapido para solo reconocimiento)
    tabla = [[set() for _ in range(n)] for _ in range(n)]

    # Paso base
    for i in range(n):
        tipo = tokens[i][0]
        for nt, prods in GRAMATICA.items():
            for prod in prods:
                if len(prod) == 1 and prod[0] == tipo:
                    tabla[i][i].add(nt)

    # Llenar tabla
    for lon in range(2, n + 1):
        for i in range(n - lon + 1):
            j = i + lon - 1
            for k in range(i, j):
                for nt, prods in GRAMATICA.items():
                    for prod in prods:
                        if len(prod) == 2:
                            B, C = prod
                            if B in tabla[i][k] and C in tabla[k + 1][j]:
                                tabla[i][j].add(nt)

    return 'E' in tabla[0][n - 1]


# ---------- Pruebas ----------
if __name__ == "__main__":
    expresiones = [
        "3 + 5",
        "10 - 2 * 3",
        "( 4 + 6 ) * 2",
        "100 / 4 + 3 * 2",
        "( 1 + 2 ) * ( 3 + 4 )",
        "8",
        "3 + 4 * 2 - 1",
        "( 10 + 5 ) / 3",
    ]

    expresiones_invalidas = [
        "+ 3 5",
        "3 + + 5",
        "( 3 + 5",
        "3 5 +",
    ]

    print("=" * 55)
    print("  PARSER CYK - CALCULADORA")
    print("=" * 55)

    for expr in expresiones:
        tokens = tokenizar(expr)
        exito, tabla = cyk_parse(tokens)
        if exito:
            resultado = evaluar(tabla, tokens, 0, len(tokens) - 1, 'E')
            print(f"  {expr:30s} = {resultado}")
        else:
            print(f"  {expr:30s} -> INVALIDA")

    print()
    print("Expresiones invalidas:")
    for expr in expresiones_invalidas:
        try:
            tokens = tokenizar(expr)
            exito, tabla = cyk_parse(tokens)
            print(f"  {expr:30s} -> {'VALIDA' if exito else 'INVALIDA'}")
        except ValueError as e:
            print(f"  {expr:30s} -> Error: {e}")
