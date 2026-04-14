"""
Comparacion de rendimiento entre el parser CYK y el parser Predictivo.

CYK tiene complejidad O(n^3 * |G|) donde n = longitud de la entrada
Predictivo (LL1) tiene complejidad O(n)

Se generan expresiones de distintos tamanios y se mide el tiempo de
cada parser para poder comparar.
"""
import time
import random
from cyk_parser import tokenizar, cyk_reconocer
from predictivo import ParserPredictivo


def generar_expresion(num_operaciones):
    """Genera una expresion aleatoria con el numero dado de operaciones"""
    operadores = ['+', '-', '*']  # evitamos / para no tener division por cero
    partes = [str(random.randint(1, 99))]
    for _ in range(num_operaciones):
        op = random.choice(operadores)
        num = str(random.randint(1, 99))
        partes.append(op)
        partes.append(num)
    return ' '.join(partes)


def medir_cyk(tokens, repeticiones):
    """Mide el tiempo promedio del parser CYK"""
    inicio = time.time()
    for _ in range(repeticiones):
        cyk_reconocer(tokens)
    fin = time.time()
    return (fin - inicio) / repeticiones


def medir_predictivo(tokens, repeticiones):
    """Mide el tiempo promedio del parser Predictivo"""
    inicio = time.time()
    for _ in range(repeticiones):
        try:
            p = ParserPredictivo(list(tokens))
            p.parsear()
        except SyntaxError:
            pass
    fin = time.time()
    return (fin - inicio) / repeticiones


def main():
    print("=" * 70)
    print("  COMPARACION DE RENDIMIENTO: CYK vs PREDICTIVO")
    print("=" * 70)
    print()

    # Diferentes tamanios de expresion (numero de operaciones)
    tamanios = [2, 5, 10, 20, 40, 60, 80]
    repeticiones = 10  # cuantas veces repetir para promediar

    print(f"  Cada medicion se repite {repeticiones} veces y se promedia.")
    print()

    # Encabezado de la tabla
    print(f"  {'Operaciones':>12} | {'Tokens':>8} | {'CYK (ms)':>12} | {'Predict (ms)':>13} | {'Razon':>8}")
    print("  " + "-" * 63)

    resultados = []

    for num_ops in tamanios:
        # Generar expresion y tokenizar
        expr = generar_expresion(num_ops)
        tokens = tokenizar(expr)
        num_tokens = len(tokens)

        # Medir tiempos
        tiempo_cyk = medir_cyk(tokens, repeticiones)
        tiempo_pred = medir_predictivo(tokens, repeticiones)

        # Calcular razon
        if tiempo_pred > 0:
            razon = tiempo_cyk / tiempo_pred
        else:
            razon = float('inf')

        resultados.append((num_ops, num_tokens, tiempo_cyk, tiempo_pred, razon))

        print(f"  {num_ops:>12} | {num_tokens:>8} | {tiempo_cyk*1000:>12.4f} | {tiempo_pred*1000:>13.4f} | {razon:>7.1f}x")

    print()
    print("  " + "-" * 63)
    print()

    # Analisis
    print("  ANALISIS DE RESULTADOS:")
    print("  -----------------------")
    print()
    print("  - El parser CYK tiene complejidad O(n^3), por lo que su tiempo")
    print("    crece cubicamente con respecto al tamanio de la entrada.")
    print()
    print("  - El parser Predictivo (LL1) tiene complejidad O(n), por lo que")
    print("    su tiempo crece linealmente.")
    print()
    print("  - A medida que la entrada crece, la diferencia entre ambos se")
    print("    hace mas grande. Esto se ve reflejado en la columna 'Razon'")
    print("    que muestra cuantas veces mas lento es CYK respecto al Predictivo.")
    print()

    if len(resultados) >= 2:
        primera = resultados[0]
        ultima = resultados[-1]
        print(f"  - Con {primera[0]} operaciones ({primera[1]} tokens), CYK es {primera[4]:.1f}x mas lento.")
        print(f"  - Con {ultima[0]} operaciones ({ultima[1]} tokens), CYK es {ultima[4]:.1f}x mas lento.")
        print()

    print("  CONCLUSION:")
    print("  El parser Predictivo es significativamente mas rapido que CYK")
    print("  para gramaticas que lo permiten (LL1). Sin embargo, CYK tiene la")
    print("  ventaja de funcionar con CUALQUIER gramatica libre de contexto,")
    print("  mientras que el Predictivo requiere que la gramatica sea LL(1).")
    print()
    print("  CYK es util cuando la gramatica es compleja o ambigua y no se")
    print("  puede adaptar facilmente a LL(1). El Predictivo es preferible")
    print("  cuando la eficiencia es importante y la gramatica lo permite.")


if __name__ == "__main__":
    random.seed(42)  # semilla para reproducibilidad
    main()
