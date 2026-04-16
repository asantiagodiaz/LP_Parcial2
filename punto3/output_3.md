=================================================================
 DEMOSTRACION DE AMBIGUEDAD
=================================================================

Gramatica original:
  prop --> if expr then prop
         | prop_emparejada

  prop_emparejada --> if expr then prop_emparejada else prop
                    | otras

Cadena a analizar:
  if E1 then if E2 then otras else if E3 then otras else otras

-----------------------------------------------------------------
ARBOL DE DERIVACION 1:
(el segundo 'else' se asocia con 'if E3')
-----------------------------------------------------------------

  prop
  |-> if E1 then prop                    [prop -> if expr then prop]
                  |
                  |-> prop_emparejada     [prop -> prop_emparejada]
                      |
                      |-> if E2 then (otras) else prop
                                              |
                                              |-> prop_emparejada
                                                  |
                                                  |-> if E3 then (otras) else prop
                                                                          |
                                                                          |-> otras

  Derivacion paso a paso:
    prop
    => if E1 then prop
    => if E1 then prop_emparejada
    => if E1 then if E2 then prop_emparejada else prop
    => if E1 then if E2 then otras else prop
    => if E1 then if E2 then otras else prop_emparejada
    => if E1 then if E2 then otras else if E3 then prop_emparejada else prop
    => if E1 then if E2 then otras else if E3 then otras else prop
    => if E1 then if E2 then otras else if E3 then otras else otras

  Interpretacion: if E1 then (if E2 then otras else (if E3 then otras else otras))
  --> E1 no tiene else propio
  --> El segundo else pertenece a E3

-----------------------------------------------------------------
ARBOL DE DERIVACION 2:
(el segundo 'else' se asocia con 'if E1')
-----------------------------------------------------------------

  prop
  |-> prop_emparejada                       [prop -> prop_emparejada]
      |
      |-> if E1 then (prop_emparejada) else prop
                      |                      |
                      |                      |-> otras
                      |
                      |-> if E2 then (otras) else prop
                                              |
                                              |-> if E3 then prop
                                                          |
                                                          |-> otras

  Derivacion paso a paso:
    prop
    => prop_emparejada
    => if E1 then prop_emparejada else prop
    => if E1 then (if E2 then prop_emparejada else prop) else prop
    => if E1 then (if E2 then otras else prop) else prop
    => if E1 then (if E2 then otras else if E3 then prop) else prop
    => if E1 then (if E2 then otras else if E3 then otras) else prop
    => if E1 then (if E2 then otras else if E3 then otras) else otras

  Interpretacion: if E1 then (if E2 then otras else (if E3 then otras)) else otras
  --> E1 SI tiene else (el ultimo 'otras')
  --> E3 NO tiene else

=================================================================
 CONCLUSION
=================================================================

  La misma cadena tiene DOS arboles de derivacion distintos.
  Por lo tanto, la gramatica ES AMBIGUA.

  La causa es que en la produccion:
    prop_emparejada -> if expr then prop_emparejada else prop

  El 'prop' despues del 'else' permite proposiciones sin emparejar
  (if sin else), lo que causa que un 'else' posterior pueda
  asociarse con un 'if' externo en lugar del mas cercano.

=================================================================
 GRAMATICA CORREGIDA (NO AMBIGUA)
=================================================================

  prop --> prop_emparejada
         | prop_no_emparejada

  prop_emparejada --> if expr then prop_emparejada else prop_emparejada
                    | otras

  prop_no_emparejada --> if expr then prop
                       | if expr then prop_emparejada else prop_no_emparejada

  Explicacion de la correccion:
  -------------------------------------------------------
  1) 'prop_emparejada' ahora exige que TANTO la parte 'then'
     como la parte 'else' sean proposiciones emparejadas.
     Esto garantiza que entre un 'then' y un 'else' no queden
     'if' sin su respectivo 'else'.

  2) 'prop_no_emparejada' tiene dos opciones:
     a) if sin else: if expr then prop
     b) if con else pero donde la parte else es no emparejada:
        if expr then prop_emparejada else prop_no_emparejada
     Esto obliga a que las proposiciones sin emparejar solo
     aparezcan en la rama else mas externa.

  Con esta correccion, cada 'else' se asocia con el 'if'
  sin emparejar MAS CERCANO (regla del else mas cercano).

=================================================================
 VERIFICACION CON LA CADENA PROBLEMATICA
=================================================================

  Cadena: if E1 then if E2 then otras else if E3 then otras else otras

  Intentamos derivar con la gramatica corregida:

  Intento viable:
    prop -> prop_no_emparejada -> if E1 then prop
    prop -> prop_emparejada -> if E2 then (otras) else prop_emparejada
    prop_emparejada -> if E3 then (otras) else prop_emparejada
    prop_emparejada -> otras
    EXITO: if E1 then (if E2 then otras else (if E3 then otras else otras))

  Intento alternativo:
    prop -> prop_emparejada -> if E1 then (prop_emparejada) else (prop_emparejada)
    Necesitamos que prop_emparejada derive 'if E2 then otras else if E3 then otras'
    prop_emparejada -> if E2 then (otras) else prop_emparejada
    Necesitamos prop_emparejada = 'if E3 then otras'
    Pero prop_emparejada requiere else! 'if E3 then otras' NO tiene else.
    FALLA: No se puede derivar por este camino

  Resultado: Solo existe UN arbol de derivacion.
  La gramatica corregida NO es ambigua para esta cadena.
[rerun: b8]