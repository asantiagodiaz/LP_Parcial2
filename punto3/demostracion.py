"""
Punto 3 - Demostracion de ambiguedad en gramatica if-then-else

Gramatica propuesta:
    prop --> if expr then prop
           | prop_emparejada

    prop_emparejada --> if expr then prop_emparejada else prop
                      | otras
"""


def mostrar_demostracion():
    print("=" * 65)
    print(" DEMOSTRACION DE AMBIGUEDAD")
    print("=" * 65)
    print()
    print("Gramatica original:")
    print("  prop --> if expr then prop")
    print("         | prop_emparejada")
    print()
    print("  prop_emparejada --> if expr then prop_emparejada else prop")
    print("                    | otras")
    print()

    # La cadena que demuestra la ambiguedad
    cadena = "if E1 then if E2 then otras else if E3 then otras else otras"
    print(f"Cadena a analizar:")
    print(f"  {cadena}")
    print()

    # ------- Arbol 1 -------
    print("-" * 65)
    print("ARBOL DE DERIVACION 1:")
    print("(el segundo 'else' se asocia con 'if E3')")
    print("-" * 65)
    print()
    print("  prop")
    print("  |-> if E1 then prop                    [prop -> if expr then prop]")
    print("                  |")
    print("                  |-> prop_emparejada     [prop -> prop_emparejada]")
    print("                      |")
    print("                      |-> if E2 then (otras) else prop")
    print("                                              |")
    print("                                              |-> prop_emparejada")
    print("                                                  |")
    print("                                                  |-> if E3 then (otras) else prop")
    print("                                                                          |")
    print("                                                                          |-> otras")
    print()
    print("  Derivacion paso a paso:")
    print("    prop")
    print("    => if E1 then prop")
    print("    => if E1 then prop_emparejada")
    print("    => if E1 then if E2 then prop_emparejada else prop")
    print("    => if E1 then if E2 then otras else prop")
    print("    => if E1 then if E2 then otras else prop_emparejada")
    print("    => if E1 then if E2 then otras else if E3 then prop_emparejada else prop")
    print("    => if E1 then if E2 then otras else if E3 then otras else prop")
    print("    => if E1 then if E2 then otras else if E3 then otras else otras")
    print()
    print("  Interpretacion: if E1 then (if E2 then otras else (if E3 then otras else otras))")
    print("  --> E1 no tiene else propio")
    print("  --> El segundo else pertenece a E3")
    print()

    # ------- Arbol 2 -------
    print("-" * 65)
    print("ARBOL DE DERIVACION 2:")
    print("(el segundo 'else' se asocia con 'if E1')")
    print("-" * 65)
    print()
    print("  prop")
    print("  |-> prop_emparejada                       [prop -> prop_emparejada]")
    print("      |")
    print("      |-> if E1 then (prop_emparejada) else prop")
    print("                      |                      |")
    print("                      |                      |-> otras")
    print("                      |")
    print("                      |-> if E2 then (otras) else prop")
    print("                                              |")
    print("                                              |-> if E3 then prop")
    print("                                                          |")
    print("                                                          |-> otras")
    print()
    print("  Derivacion paso a paso:")
    print("    prop")
    print("    => prop_emparejada")
    print("    => if E1 then prop_emparejada else prop")
    print("    => if E1 then (if E2 then prop_emparejada else prop) else prop")
    print("    => if E1 then (if E2 then otras else prop) else prop")
    print("    => if E1 then (if E2 then otras else if E3 then prop) else prop")
    print("    => if E1 then (if E2 then otras else if E3 then otras) else prop")
    print("    => if E1 then (if E2 then otras else if E3 then otras) else otras")
    print()
    print("  Interpretacion: if E1 then (if E2 then otras else (if E3 then otras)) else otras")
    print("  --> E1 SI tiene else (el ultimo 'otras')")
    print("  --> E3 NO tiene else")
    print()

    # ------- Conclusion -------
    print("=" * 65)
    print(" CONCLUSION")
    print("=" * 65)
    print()
    print("  La misma cadena tiene DOS arboles de derivacion distintos.")
    print("  Por lo tanto, la gramatica ES AMBIGUA.")
    print()
    print("  La causa es que en la produccion:")
    print("    prop_emparejada -> if expr then prop_emparejada else prop")
    print()
    print("  El 'prop' despues del 'else' permite proposiciones sin emparejar")
    print("  (if sin else), lo que causa que un 'else' posterior pueda")
    print("  asociarse con un 'if' externo en lugar del mas cercano.")
    print()


def mostrar_gramatica_corregida():
    print("=" * 65)
    print(" GRAMATICA CORREGIDA (NO AMBIGUA)")
    print("=" * 65)
    print()
    print("  prop --> prop_emparejada")
    print("         | prop_no_emparejada")
    print()
    print("  prop_emparejada --> if expr then prop_emparejada else prop_emparejada")
    print("                    | otras")
    print()
    print("  prop_no_emparejada --> if expr then prop")
    print("                       | if expr then prop_emparejada else prop_no_emparejada")
    print()
    print("  Explicacion de la correccion:")
    print("  -------------------------------------------------------")
    print("  1) 'prop_emparejada' ahora exige que TANTO la parte 'then'")
    print("     como la parte 'else' sean proposiciones emparejadas.")
    print("     Esto garantiza que entre un 'then' y un 'else' no queden")
    print("     'if' sin su respectivo 'else'.")
    print()
    print("  2) 'prop_no_emparejada' tiene dos opciones:")
    print("     a) if sin else: if expr then prop")
    print("     b) if con else pero donde la parte else es no emparejada:")
    print("        if expr then prop_emparejada else prop_no_emparejada")
    print("     Esto obliga a que las proposiciones sin emparejar solo")
    print("     aparezcan en la rama else mas externa.")
    print()
    print("  Con esta correccion, cada 'else' se asocia con el 'if'")
    print("  sin emparejar MAS CERCANO (regla del else mas cercano).")
    print()


def verificar_con_cadena():
    """
    Verificamos que la gramatica corregida solo produce UN arbol
    para la cadena problematica
    """
    print("=" * 65)
    print(" VERIFICACION CON LA CADENA PROBLEMATICA")
    print("=" * 65)
    print()
    cadena = "if E1 then if E2 then otras else if E3 then otras else otras"
    print(f"  Cadena: {cadena}")
    print()

    print("  Intentamos derivar con la gramatica corregida:")
    print()

    # Intento 1: prop -> prop_no_emparejada -> if E1 then prop
    print("  Intento viable:")
    print("    prop -> prop_no_emparejada -> if E1 then prop")
    print("    prop -> prop_emparejada -> if E2 then (otras) else prop_emparejada")
    print("    prop_emparejada -> if E3 then (otras) else prop_emparejada")
    print("    prop_emparejada -> otras")
    print("    EXITO: if E1 then (if E2 then otras else (if E3 then otras else otras))")
    print()

    # Intento 2: prop -> prop_emparejada -> if E1 then prop_emparejada else prop_emparejada
    print("  Intento alternativo:")
    print("    prop -> prop_emparejada -> if E1 then (prop_emparejada) else (prop_emparejada)")
    print("    Necesitamos que prop_emparejada derive 'if E2 then otras else if E3 then otras'")
    print("    prop_emparejada -> if E2 then (otras) else prop_emparejada")
    print("    Necesitamos prop_emparejada = 'if E3 then otras'")
    print("    Pero prop_emparejada requiere else! 'if E3 then otras' NO tiene else.")
    print("    FALLA: No se puede derivar por este camino")
    print()

    print("  Resultado: Solo existe UN arbol de derivacion.")
    print("  La gramatica corregida NO es ambigua para esta cadena.")


if __name__ == "__main__":
    mostrar_demostracion()
    mostrar_gramatica_corregida()
    verificar_con_cadena()
