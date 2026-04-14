"""
Punto 5: Parser descendente recursivo con algoritmo de emparejamiento.

Gramatica para operaciones de asignacion y condicionales:

  programa    -> sentencias
  sentencias  -> sentencia sentencias | vacio
  sentencia   -> ID '=' expresion ';'
               | IF '(' expresion ')' '{' sentencias '}' parte_else
  parte_else  -> ELSE '{' sentencias '}' | vacio
  expresion   -> expr_simple comparacion
  comparacion -> OP_REL expr_simple | vacio
  expr_simple -> termino resto_e
  resto_e     -> '+' termino resto_e | '-' termino resto_e | vacio
  termino     -> factor resto_t
  resto_t     -> '*' factor resto_t | '/' factor resto_t | vacio
  factor      -> ID | NUM | '(' expresion ')'

Tokens:
  ID, NUM, IF, ELSE,
  ASIGNAR (=), PUNTO_COMA (;),
  MAS (+), MENOS (-), POR (*), DIVIDIR (/),
  PAREN_IZQ, PAREN_DER, LLAVE_IZQ, LLAVE_DER,
  OP_REL (==, !=, >, <, >=, <=)
"""


# ===================== LEXER =====================

class Token:
    def __init__(self, tipo, valor, linea=0):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea

    def __repr__(self):
        return f"Token({self.tipo}, {self.valor})"


PALABRAS_CLAVE = {'if': 'IF', 'else': 'ELSE'}


def tokenizar(texto):
    """Analisis lexico: convierte texto en lista de tokens"""
    tokens = []
    i = 0
    linea = 1

    while i < len(texto):
        # Saltar espacios
        if texto[i] in ' \t':
            i += 1
            continue
        if texto[i] == '\n':
            linea += 1
            i += 1
            continue

        # Identificadores y palabras clave
        if texto[i].isalpha() or texto[i] == '_':
            j = i
            while j < len(texto) and (texto[j].isalnum() or texto[j] == '_'):
                j += 1
            palabra = texto[i:j]
            tipo = PALABRAS_CLAVE.get(palabra, 'ID')
            tokens.append(Token(tipo, palabra, linea))
            i = j

        # Numeros
        elif texto[i].isdigit():
            j = i
            while j < len(texto) and texto[j].isdigit():
                j += 1
            tokens.append(Token('NUM', int(texto[i:j]), linea))
            i = j

        # Operadores de dos caracteres
        elif texto[i] == '=' and i + 1 < len(texto) and texto[i + 1] == '=':
            tokens.append(Token('OP_REL', '==', linea))
            i += 2
        elif texto[i] == '!' and i + 1 < len(texto) and texto[i + 1] == '=':
            tokens.append(Token('OP_REL', '!=', linea))
            i += 2
        elif texto[i] == '>' and i + 1 < len(texto) and texto[i + 1] == '=':
            tokens.append(Token('OP_REL', '>=', linea))
            i += 2
        elif texto[i] == '<' and i + 1 < len(texto) and texto[i + 1] == '=':
            tokens.append(Token('OP_REL', '<=', linea))
            i += 2

        # Operadores de un caracter
        elif texto[i] == '>':
            tokens.append(Token('OP_REL', '>', linea))
            i += 1
        elif texto[i] == '<':
            tokens.append(Token('OP_REL', '<', linea))
            i += 1
        elif texto[i] == '=':
            tokens.append(Token('ASIGNAR', '=', linea))
            i += 1
        elif texto[i] == '+':
            tokens.append(Token('MAS', '+', linea))
            i += 1
        elif texto[i] == '-':
            tokens.append(Token('MENOS', '-', linea))
            i += 1
        elif texto[i] == '*':
            tokens.append(Token('POR', '*', linea))
            i += 1
        elif texto[i] == '/':
            tokens.append(Token('DIVIDIR', '/', linea))
            i += 1
        elif texto[i] == '(':
            tokens.append(Token('PAREN_IZQ', '(', linea))
            i += 1
        elif texto[i] == ')':
            tokens.append(Token('PAREN_DER', ')', linea))
            i += 1
        elif texto[i] == '{':
            tokens.append(Token('LLAVE_IZQ', '{', linea))
            i += 1
        elif texto[i] == '}':
            tokens.append(Token('LLAVE_DER', '}', linea))
            i += 1
        elif texto[i] == ';':
            tokens.append(Token('PUNTO_COMA', ';', linea))
            i += 1
        else:
            raise ValueError(f"Caracter no reconocido: '{texto[i]}' en linea {linea}")

    return tokens


# ===================== PARSER =====================

class ParserDescendente:
    """
    Parser descendente recursivo con algoritmo de emparejamiento.

    El algoritmo de emparejamiento (match) es el mecanismo central:
    compara el token actual con el token esperado. Si coinciden,
    avanza al siguiente token. Si no coinciden, reporta error.
    """

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.nivel = 0  # para indentar el output

    def token_actual(self):
        """Retorna el token en la posicion actual (lookahead)"""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def emparejar(self, tipo_esperado):
        """
        ALGORITMO DE EMPAREJAMIENTO (match):
        1. Obtener el token actual
        2. Comparar su tipo con el tipo esperado
        3. Si coinciden: consumir el token (avanzar posicion) y retornarlo
        4. Si no coinciden: lanzar error de sintaxis

        Este es el mecanismo fundamental del parser descendente recursivo.
        Cada vez que una regla de la gramatica espera un terminal especifico,
        llama a emparejar() para verificar que el token actual corresponde.
        """
        tok = self.token_actual()

        if tok is None:
            raise SyntaxError(
                f"Error: se esperaba '{tipo_esperado}' pero se llego al final de la entrada"
            )

        if tok.tipo != tipo_esperado:
            raise SyntaxError(
                f"Error en linea {tok.linea}: se esperaba '{tipo_esperado}', "
                f"se encontro '{tok.tipo}' (valor: '{tok.valor}')"
            )

        # Emparejamiento exitoso: consumir token
        self.pos += 1
        indent = "  " * self.nivel
        print(f"{indent}Emparejado: {tok}")
        return tok

    def _log(self, regla):
        """Imprime que regla se esta aplicando"""
        indent = "  " * self.nivel
        print(f"{indent}{regla}")

    # ---- Reglas de la gramatica ----

    def programa(self):
        """programa -> sentencias"""
        self._log("programa -> sentencias")
        self.nivel += 1
        self.sentencias()
        self.nivel -= 1

        # Verificar que se consumieron todos los tokens
        if self.pos < len(self.tokens):
            tok = self.token_actual()
            raise SyntaxError(
                f"Error: tokens sobrantes en linea {tok.linea}, token: {tok}"
            )
        print("\n>>> Parseo exitoso!")

    def sentencias(self):
        """sentencias -> sentencia sentencias | vacio"""
        tok = self.token_actual()
        # Si el token actual puede iniciar una sentencia (ID o IF)
        if tok and tok.tipo in ('ID', 'IF'):
            self._log("sentencias -> sentencia sentencias")
            self.nivel += 1
            self.sentencia()
            self.sentencias()  # recursion para mas sentencias
            self.nivel -= 1
        else:
            self._log("sentencias -> vacio")

    def sentencia(self):
        """sentencia -> ID '=' expresion ';' | IF '(' expresion ')' '{' sentencias '}' parte_else"""
        tok = self.token_actual()
        if tok.tipo == 'ID':
            # Asignacion
            self._log("sentencia -> ID '=' expresion ';'")
            self.nivel += 1
            self.emparejar('ID')
            self.emparejar('ASIGNAR')
            self.expresion()
            self.emparejar('PUNTO_COMA')
            self.nivel -= 1

        elif tok.tipo == 'IF':
            # Condicional
            self._log("sentencia -> IF '(' expresion ')' '{' sentencias '}' parte_else")
            self.nivel += 1
            self.emparejar('IF')
            self.emparejar('PAREN_IZQ')
            self.expresion()
            self.emparejar('PAREN_DER')
            self.emparejar('LLAVE_IZQ')
            self.sentencias()
            self.emparejar('LLAVE_DER')
            self.parte_else()
            self.nivel -= 1

        else:
            raise SyntaxError(
                f"Error en linea {tok.linea}: se esperaba una sentencia "
                f"(ID o IF), se encontro '{tok.tipo}'"
            )

    def parte_else(self):
        """parte_else -> ELSE '{' sentencias '}' | vacio"""
        tok = self.token_actual()
        if tok and tok.tipo == 'ELSE':
            self._log("parte_else -> ELSE '{' sentencias '}'")
            self.nivel += 1
            self.emparejar('ELSE')
            self.emparejar('LLAVE_IZQ')
            self.sentencias()
            self.emparejar('LLAVE_DER')
            self.nivel -= 1
        else:
            self._log("parte_else -> vacio")

    def expresion(self):
        """expresion -> expr_simple comparacion"""
        self._log("expresion -> expr_simple comparacion")
        self.nivel += 1
        self.expr_simple()
        self.comparacion()
        self.nivel -= 1

    def comparacion(self):
        """comparacion -> OP_REL expr_simple | vacio"""
        tok = self.token_actual()
        if tok and tok.tipo == 'OP_REL':
            self._log("comparacion -> OP_REL expr_simple")
            self.nivel += 1
            self.emparejar('OP_REL')
            self.expr_simple()
            self.nivel -= 1
        else:
            self._log("comparacion -> vacio")

    def expr_simple(self):
        """expr_simple -> termino resto_e"""
        self._log("expr_simple -> termino resto_e")
        self.nivel += 1
        self.termino()
        self.resto_e()
        self.nivel -= 1

    def resto_e(self):
        """resto_e -> '+' termino resto_e | '-' termino resto_e | vacio"""
        tok = self.token_actual()
        if tok and tok.tipo == 'MAS':
            self._log("resto_e -> '+' termino resto_e")
            self.nivel += 1
            self.emparejar('MAS')
            self.termino()
            self.resto_e()
            self.nivel -= 1
        elif tok and tok.tipo == 'MENOS':
            self._log("resto_e -> '-' termino resto_e")
            self.nivel += 1
            self.emparejar('MENOS')
            self.termino()
            self.resto_e()
            self.nivel -= 1
        else:
            self._log("resto_e -> vacio")

    def termino(self):
        """termino -> factor resto_t"""
        self._log("termino -> factor resto_t")
        self.nivel += 1
        self.factor()
        self.resto_t()
        self.nivel -= 1

    def resto_t(self):
        """resto_t -> '*' factor resto_t | '/' factor resto_t | vacio"""
        tok = self.token_actual()
        if tok and tok.tipo == 'POR':
            self._log("resto_t -> '*' factor resto_t")
            self.nivel += 1
            self.emparejar('POR')
            self.factor()
            self.resto_t()
            self.nivel -= 1
        elif tok and tok.tipo == 'DIVIDIR':
            self._log("resto_t -> '/' factor resto_t")
            self.nivel += 1
            self.emparejar('DIVIDIR')
            self.factor()
            self.resto_t()
            self.nivel -= 1
        else:
            self._log("resto_t -> vacio")

    def factor(self):
        """factor -> ID | NUM | '(' expresion ')'"""
        tok = self.token_actual()
        if tok is None:
            raise SyntaxError("Error: se esperaba un factor pero se llego al final")

        if tok.tipo == 'ID':
            self._log("factor -> ID")
            self.nivel += 1
            self.emparejar('ID')
            self.nivel -= 1
        elif tok.tipo == 'NUM':
            self._log("factor -> NUM")
            self.nivel += 1
            self.emparejar('NUM')
            self.nivel -= 1
        elif tok.tipo == 'PAREN_IZQ':
            self._log("factor -> '(' expresion ')'")
            self.nivel += 1
            self.emparejar('PAREN_IZQ')
            self.expresion()
            self.emparejar('PAREN_DER')
            self.nivel -= 1
        else:
            raise SyntaxError(
                f"Error en linea {tok.linea}: se esperaba ID, NUM o '(' "
                f"pero se encontro '{tok.tipo}'"
            )


# ===================== PRUEBAS =====================

def ejecutar_prueba(nombre, codigo):
    print(f"\n{'='*60}")
    print(f" Prueba: {nombre}")
    print(f"{'='*60}")
    print(f" Codigo: {codigo.strip()}")
    print(f"{'-'*60}")

    try:
        tokens = tokenizar(codigo)
        print(f" Tokens: {tokens}")
        print()
        parser = ParserDescendente(tokens)
        parser.programa()
    except (SyntaxError, ValueError) as e:
        print(f"\n>>> ERROR: {e}")


if __name__ == "__main__":
    print("*" * 60)
    print("  PARSER DESCENDENTE RECURSIVO")
    print("  Con algoritmo de emparejamiento")
    print("*" * 60)

    # Prueba 1: Asignacion simple
    ejecutar_prueba("Asignacion simple", "x = 5;")

    # Prueba 2: Asignacion con expresion
    ejecutar_prueba("Asignacion con expresion", "resultado = 3 + 4 * 2;")

    # Prueba 3: Condicional simple
    ejecutar_prueba("Condicional simple (if)", """
    if (x > 0) {
        y = 1;
    }
    """)

    # Prueba 4: Condicional con else
    ejecutar_prueba("Condicional con else", """
    if (x >= 10) {
        y = x + 1;
    } else {
        y = 0;
    }
    """)

    # Prueba 5: Multiples sentencias
    ejecutar_prueba("Multiples sentencias", """
    a = 10;
    b = 20;
    c = a + b;
    """)

    # Prueba 6: Condicionales anidados
    ejecutar_prueba("Condicionales anidados", """
    if (x > 0) {
        if (x < 100) {
            y = x * 2;
        } else {
            y = 100;
        }
    }
    """)

    # Prueba 7: Expresion con parentesis
    ejecutar_prueba("Expresion con parentesis", "z = (a + b) * (c - d);")

    # Prueba 8: Comparacion en asignacion... bueno, en condicional
    ejecutar_prueba("Condicional con comparacion !=", """
    if (valor != 0) {
        resultado = 100 / valor;
    }
    """)

    # Prueba 9: Error - falta punto y coma
    ejecutar_prueba("Error: falta punto y coma", "x = 5")

    # Prueba 10: Error - falta parentesis
    ejecutar_prueba("Error: falta llave", """
    if (x > 0)
        y = 1;
    """)
