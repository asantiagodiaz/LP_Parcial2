=======================================================
  PARSER CYK - CALCULADORA
=======================================================
  3 + 5                          = 8
  10 - 2 * 3                     = 4
  ( 4 + 6 ) * 2                  = 20
  100 / 4 + 3 * 2                = 31.0
  ( 1 + 2 ) * ( 3 + 4 )          = 21
  8                              = 8
  3 + 4 * 2 - 1                  = 10
  ( 10 + 5 ) / 3                 = 5.0

Expresiones invalidas:
  + 3 5                          -> INVALIDA
  3 + + 5                        -> INVALIDA
  ( 3 + 5                        -> INVALIDA
  3 5 +                          -> INVALIDA
[rerun: b9]


=======================================================
  PARSER PREDICTIVO (LL1) - CALCULADORA
=======================================================
  3 + 5                          = 8
  10 - 2 * 3                     = 4
  ( 4 + 6 ) * 2                  = 20
  100 / 4 + 3 * 2                = 31.0
  ( 1 + 2 ) * ( 3 + 4 )          = 21
  8                              = 8
  3 + 4 * 2 - 1                  = 10
  ( 10 + 5 ) / 3                 = 5.0
[rerun: b10]



======================================================================
  COMPARACION DE RENDIMIENTO: CYK vs PREDICTIVO
======================================================================

  Cada medicion se repite 10 veces y se promedia.

   Operaciones |   Tokens |     CYK (ms) |  Predict (ms) |    Razon
  ---------------------------------------------------------------
             2 |        5 |       0.0690 |        0.0057 |    12.2x
             5 |       11 |       0.5656 |        0.0062 |    90.5x
            10 |       21 |       3.8018 |        0.0118 |   320.8x
            20 |       41 |      27.5207 |        0.0229 |  1201.1x
            40 |       81 |     154.2806 |        0.0224 |  6884.0x
            60 |      121 |     437.0384 |        0.0363 | 12028.0x
            80 |      161 |    1066.0757 |        0.0454 | 23472.2x

  ---------------------------------------------------------------

  ANALISIS DE RESULTADOS:
  -----------------------

  - El parser CYK tiene complejidad O(n^3), por lo que su tiempo
    crece cubicamente con respecto al tamanio de la entrada.

  - El parser Predictivo (LL1) tiene complejidad O(n), por lo que
    su tiempo crece linealmente.

  - A medida que la entrada crece, la diferencia entre ambos se
    hace mas grande. Esto se ve reflejado en la columna 'Razon'
    que muestra cuantas veces mas lento es CYK respecto al Predictivo.

  - Con 2 operaciones (5 tokens), CYK es 12.2x mas lento.
  - Con 80 operaciones (161 tokens), CYK es 23472.2x mas lento.

  CONCLUSION:
  El parser Predictivo es significativamente mas rapido que CYK
  para gramaticas que lo permiten (LL1). Sin embargo, CYK tiene la
  ventaja de funcionar con CUALQUIER gramatica libre de contexto,
  mientras que el Predictivo requiere que la gramatica sea LL(1).

  CYK es util cuando la gramatica es compleja o ambigua y no se
  puede adaptar facilmente a LL(1). El Predictivo es preferible
  cuando la eficiencia es importante y la gramatica lo permite.
[rerun: b15]