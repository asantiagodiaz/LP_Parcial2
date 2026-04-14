import ply.yacc as yacc
from lexer import tokens

# ---- Reglas de la gramatica ----

def p_programa(p):
    '''programa : sentencias'''
    print(">>> Programa parseado correctamente")

def p_sentencias_mult(p):
    '''sentencias : sentencia PUNTO_COMA sentencias'''
    pass

def p_sentencias_una(p):
    '''sentencias : sentencia PUNTO_COMA'''
    pass

# Tipos de sentencia
def p_sentencia(p):
    '''sentencia : crear_db
                 | usar_db
                 | crear_col
                 | insertar
                 | buscar
                 | actualizar
                 | eliminar'''
    pass

# CREAR BASE nombre
def p_crear_db(p):
    '''crear_db : CREAR BASE ID'''
    print(f"  [CREAR BD] nombre: {p[3]}")

# USAR nombre
def p_usar_db(p):
    '''usar_db : USAR ID'''
    print(f"  [USAR BD] nombre: {p[2]}")

# CREAR COLECCION nombre
def p_crear_col(p):
    '''crear_col : CREAR COLECCION ID'''
    print(f"  [CREAR COLECCION] nombre: {p[3]}")

# INSERTAR EN coleccion DOCUMENTO {...}
def p_insertar(p):
    '''insertar : INSERTAR EN ID DOCUMENTO documento'''
    print(f"  [INSERTAR] en coleccion: {p[3]}, documento: {p[5]}")

# BUSCAR EN coleccion TODO
def p_buscar_todo(p):
    '''buscar : BUSCAR EN ID TODO'''
    print(f"  [BUSCAR] todos los documentos en: {p[3]}")

# BUSCAR EN coleccion DONDE condiciones
def p_buscar_filtro(p):
    '''buscar : BUSCAR EN ID DONDE condiciones'''
    print(f"  [BUSCAR] en {p[3]} donde {p[5]}")

# ACTUALIZAR EN coleccion DONDE condiciones CON documento
def p_actualizar(p):
    '''actualizar : ACTUALIZAR EN ID DONDE condiciones CON documento'''
    print(f"  [ACTUALIZAR] en {p[3]} donde {p[5]} con {p[7]}")

# ELIMINAR EN coleccion DONDE condiciones
def p_eliminar(p):
    '''eliminar : ELIMINAR EN ID DONDE condiciones'''
    print(f"  [ELIMINAR] de {p[3]} donde {p[5]}")

# Documentos tipo JSON
def p_documento(p):
    '''documento : LLAVE_IZQ pares LLAVE_DER'''
    p[0] = p[2]

def p_pares_mult(p):
    '''pares : par COMA pares'''
    p[0] = {**p[1], **p[3]}

def p_pares_uno(p):
    '''pares : par'''
    p[0] = p[1]

def p_par(p):
    '''par : CADENA DOS_PUNTOS valor'''
    p[0] = {p[1]: p[3]}

# Tipos de valor
def p_valor_cadena(p):
    '''valor : CADENA'''
    p[0] = p[1]

def p_valor_numero(p):
    '''valor : NUMERO'''
    p[0] = p[1]

def p_valor_true(p):
    '''valor : VERDADERO'''
    p[0] = True

def p_valor_false(p):
    '''valor : FALSO'''
    p[0] = False

def p_valor_doc(p):
    '''valor : documento'''
    p[0] = p[1]

def p_valor_lista(p):
    '''valor : CORCHETE_IZQ lista CORCHETE_DER'''
    p[0] = p[2]

def p_lista_mult(p):
    '''lista : valor COMA lista'''
    p[0] = [p[1]] + p[3]

def p_lista_uno(p):
    '''lista : valor'''
    p[0] = [p[1]]

def p_lista_vacia(p):
    '''lista : '''
    p[0] = []

# Condiciones de busqueda
def p_condiciones_y(p):
    '''condiciones : condicion Y condiciones'''
    p[0] = f"({p[1]} Y {p[3]})"

def p_condiciones_o(p):
    '''condiciones : condicion O condiciones'''
    p[0] = f"({p[1]} O {p[3]})"

def p_condiciones_simple(p):
    '''condiciones : condicion'''
    p[0] = p[1]

def p_condicion(p):
    '''condicion : CADENA operador valor'''
    p[0] = f"{p[1]} {p[2]} {p[3]}"

def p_operador(p):
    '''operador : IGUAL_IGUAL
               | DIFERENTE
               | MAYOR
               | MENOR
               | MAYOR_IGUAL
               | MENOR_IGUAL'''
    p[0] = p[1]

# Manejo de errores de sintaxis
def p_error(p):
    if p:
        print(f"Error de sintaxis en '{p.value}', linea {p.lineno}")
    else:
        print("Error de sintaxis: se esperaban mas tokens")

# Crear el parser
parser = yacc.yacc()
