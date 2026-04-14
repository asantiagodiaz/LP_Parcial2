"""
Parser Predictivo (LL1) para operaciones de calculadora.

Gramatica LL(1) (sin recursion por la izquierda):
  E  -> T E'
  E' -> + T E' | - T E' | vacio
  T  -> F T'
  T' -> * F T' | / F T' | vacio
  F  -> ( E ) | num

Este parser es de tipo descendente predictivo: en cada paso
sabe que produccion aplicar mirando el token actual (lookahead).
"""


def tokenizar(expresion):
    """Convierte una cadena en lista de tokens"""
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
            raise ValueError(f"Caracter no esperado: '{expresion[i]}'")
    return tokens


class ParserPredictivo:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def token_actual(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consumir(self, tipo_esperado=None):
        tok = self.token_actual()
        if tok is None:
            raise SyntaxError("Se esperaba un token pero se llego al final")
        if tipo_esperado and tok[0] != tipo_esperado:
            raise SyntaxError(f"Se esperaba '{tipo_esperado}', se encontro '{tok[0]}'")
        self.pos += 1
        return tok

    def parsear(self):
        resultado = self.E()
        if self.pos != len(self.tokens):
            raise SyntaxError("Tokens sobrantes despues de la expresion")
        return resultado

    # E -> T E'
    def E(self):
        valor = self.T()
        return self.E_prima(valor)

    # E' -> + T E' | - T E' | vacio
    def E_prima(self, valor_heredado):
        tok = self.token_actual()
        if tok and tok[0] == '+':
            self.consumir()
            valor_t = self.T()
            return self.E_prima(valor_heredado + valor_t)
        elif tok and tok[0] == '-':
            self.consumir()
            valor_t = self.T()
            return self.E_prima(valor_heredado - valor_t)
        # vacio: no consumir nada
        return valor_heredado

    # T -> F T'
    def T(self):
        valor = self.F()
        return self.T_prima(valor)

    # T' -> * F T' | / F T' | vacio
    def T_prima(self, valor_heredado):
        tok = self.token_actual()
        if tok and tok[0] == '*':
            self.consumir()
            valor_f = self.F()
            return self.T_prima(valor_heredado * valor_f)
        elif tok and tok[0] == '/':
            self.consumir()
            valor_f = self.F()
            if valor_f == 0:
                print("  Advertencia: division por cero")
                return self.T_prima(float('inf'))
            return self.T_prima(valor_heredado / valor_f)
        return valor_heredado

    # F -> ( E ) | num
    def F(self):
        tok = self.token_actual()
        if tok is None:
            raise SyntaxError("Se esperaba un factor pero se llego al final")
        if tok[0] == 'num':
            self.consumir()
            return tok[1]
        elif tok[0] == '(':
            self.consumir()
            valor = self.E()
            self.consumir(')')
            return valor
        else:
            raise SyntaxError(f"Token inesperado: '{tok[0]}'")


def predictivo_reconocer(tokens):
    """Solo verifica si la expresion es valida (sin evaluar el resultado)"""
    try:
        p = ParserPredictivo(tokens)
        p.parsear()
        return True
    except SyntaxError:
        return False


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

    print("=" * 55)
    print("  PARSER PREDICTIVO (LL1) - CALCULADORA")
    print("=" * 55)

    for expr in expresiones:
        tokens = tokenizar(expr)
        try:
            parser = ParserPredictivo(tokens)
            resultado = parser.parsear()
            print(f"  {expr:30s} = {resultado}")
        except SyntaxError as e:
            print(f"  {expr:30s} -> Error: {e}")
