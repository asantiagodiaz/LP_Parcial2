import ply.lex as lex

# Palabras reservadas del lenguaje
reservadas = {
    'crear': 'CREAR',
    'usar': 'USAR',
    'insertar': 'INSERTAR',
    'buscar': 'BUSCAR',
    'actualizar': 'ACTUALIZAR',
    'eliminar': 'ELIMINAR',
    'base': 'BASE',
    'coleccion': 'COLECCION',
    'en': 'EN',
    'documento': 'DOCUMENTO',
    'donde': 'DONDE',
    'con': 'CON',
    'todo': 'TODO',
    'y': 'Y',
    'o': 'O',
    'verdadero': 'VERDADERO',
    'falso': 'FALSO',
}

# Lista de tokens
tokens = list(reservadas.values()) + [
    'ID', 'CADENA', 'NUMERO',
    'LLAVE_IZQ', 'LLAVE_DER',
    'CORCHETE_IZQ', 'CORCHETE_DER',
    'DOS_PUNTOS', 'COMA', 'PUNTO_COMA',
    'IGUAL_IGUAL', 'DIFERENTE',
    'MAYOR_IGUAL', 'MENOR_IGUAL',
    'MAYOR', 'MENOR',
]

# Tokens simples (un solo caracter o secuencia fija)
t_LLAVE_IZQ = r'\{'
t_LLAVE_DER = r'\}'
t_CORCHETE_IZQ = r'\['
t_CORCHETE_DER = r'\]'
t_DOS_PUNTOS = r':'
t_COMA = r','
t_PUNTO_COMA = r';'

# Operadores de comparacion (los mas largos primero para que no haya conflicto)
t_IGUAL_IGUAL = r'=='
t_DIFERENTE = r'!='
t_MAYOR_IGUAL = r'>='
t_MENOR_IGUAL = r'<='
t_MAYOR = r'>'
t_MENOR = r'<'

# Numeros (enteros o decimales)
def t_NUMERO(t):
    r'\d+(\.\d+)?'
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t

# Cadenas entre comillas dobles
def t_CADENA(t):
    r'\"[^\"]*\"'
    t.value = t.value[1:-1]
    return t

# Identificadores y palabras reservadas
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    # Revisar si es palabra reservada (case insensitive)
    t.type = reservadas.get(t.value.lower(), 'ID')
    return t

# Ignorar espacios y tabs
t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejo de errores
def t_error(t):
    print(f"Error lexico: caracter no reconocido '{t.value[0]}' en linea {t.lineno}")
    t.lexer.skip(1)

# Crear el lexer
lexer = lex.lex()
