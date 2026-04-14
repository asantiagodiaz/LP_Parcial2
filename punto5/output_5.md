************************************************************
  PARSER DESCENDENTE RECURSIVO
  Con algoritmo de emparejamiento
************************************************************

============================================================
 Prueba: Asignacion simple
============================================================
 Codigo: x = 5;
------------------------------------------------------------
 Tokens: [Token(ID, x), Token(ASIGNAR, =), Token(NUM, 5), Token(PUNTO_COMA, ;)]

programa -> sentencias
  sentencias -> sentencia sentencias
    sentencia -> ID '=' expresion ';'
      Emparejado: Token(ID, x)
      Emparejado: Token(ASIGNAR, =)
      expresion -> expr_simple comparacion
        expr_simple -> termino resto_e
          termino -> factor resto_t
            factor -> NUM
              Emparejado: Token(NUM, 5)
            resto_t -> vacio
          resto_e -> vacio
        comparacion -> vacio
      Emparejado: Token(PUNTO_COMA, ;)
    sentencias -> vacio

>>> Parseo exitoso!

============================================================
 Prueba: Asignacion con expresion
============================================================
 Codigo: resultado = 3 + 4 * 2;
------------------------------------------------------------
 Tokens: [Token(ID, resultado), Token(ASIGNAR, =), Token(NUM, 3), Token(MAS, +), Token(NUM, 4), Token(POR, *), Token(NUM, 2), Token(PUNTO_COMA, ;)]

programa -> sentencias
  sentencias -> sentencia sentencias
    sentencia -> ID '=' expresion ';'
      Emparejado: Token(ID, resultado)
      Emparejado: Token(ASIGNAR, =)
      expresion -> expr_simple comparacion
        expr_simple -> termino resto_e
          termino -> factor resto_t
            factor -> NUM
              Emparejado: Token(NUM, 3)
            resto_t -> vacio
          resto_e -> '+' termino resto_e
            Emparejado: Token(MAS, +)
            termino -> factor resto_t
              factor -> NUM
                Emparejado: Token(NUM, 4)
              resto_t -> '*' factor resto_t
                Emparejado: Token(POR, *)
                factor -> NUM
                  Emparejado: Token(NUM, 2)
                resto_t -> vacio
            resto_e -> vacio
        comparacion -> vacio
      Emparejado: Token(PUNTO_COMA, ;)
    sentencias -> vacio

>>> Parseo exitoso!

============================================================
 Prueba: Condicional simple (if)
============================================================
 Codigo: if (x > 0) {
        y = 1;
    }
------------------------------------------------------------
 Tokens: [Token(IF, if), Token(PAREN_IZQ, (), Token(ID, x), Token(OP_REL, >), Token(NUM, 0), Token(PAREN_DER, )), Token(LLAVE_IZQ, {), Token(ID, y), Token(ASIGNAR, =), Token(NUM, 1), Token(PUNTO_COMA, ;), Token(LLAVE_DER, })]

programa -> sentencias
  sentencias -> sentencia sentencias
    sentencia -> IF '(' expresion ')' '{' sentencias '}' parte_else
      Emparejado: Token(IF, if)
      Emparejado: Token(PAREN_IZQ, ()
      expresion -> expr_simple comparacion
        expr_simple -> termino resto_e
          termino -> factor resto_t
            factor -> ID
              Emparejado: Token(ID, x)
            resto_t -> vacio
          resto_e -> vacio
        comparacion -> OP_REL expr_simple
          Emparejado: Token(OP_REL, >)
          expr_simple -> termino resto_e
            termino -> factor resto_t
              factor -> NUM
                Emparejado: Token(NUM, 0)
              resto_t -> vacio
            resto_e -> vacio
      Emparejado: Token(PAREN_DER, ))
      Emparejado: Token(LLAVE_IZQ, {)
      sentencias -> sentencia sentencias
        sentencia -> ID '=' expresion ';'
          Emparejado: Token(ID, y)
          Emparejado: Token(ASIGNAR, =)
          expresion -> expr_simple comparacion
            expr_simple -> termino resto_e
              termino -> factor resto_t
                factor -> NUM
                  Emparejado: Token(NUM, 1)
                resto_t -> vacio
              resto_e -> vacio
            comparacion -> vacio
          Emparejado: Token(PUNTO_COMA, ;)
        sentencias -> vacio
      Emparejado: Token(LLAVE_DER, })
      parte_else -> vacio
    sentencias -> vacio

>>> Parseo exitoso!

============================================================
 Prueba: Condicional con else
============================================================
 Codigo: if (x >= 10) {
        y = x + 1;
    } else {
        y = 0;
    }
------------------------------------------------------------
 Tokens: [Token(IF, if), Token(PAREN_IZQ, (), Token(ID, x), Token(OP_REL, >=), Token(NUM, 10), Token(PAREN_DER, )), Token(LLAVE_IZQ, {), Token(ID, y), Token(ASIGNAR, =), Token(ID, x), Token(MAS, +), Token(NUM, 1), Token(PUNTO_COMA, ;), Token(LLAVE_DER, }), Token(ELSE, else), Token(LLAVE_IZQ, {), Token(ID, y), Token(ASIGNAR, =), Token(NUM, 0), Token(PUNTO_COMA, ;), Token(LLAVE_DER, })]

programa -> sentencias
  sentencias -> sentencia sentencias
    sentencia -> IF '(' expresion ')' '{' sentencias '}' parte_else
      Emparejado: Token(IF, if)
      Emparejado: Token(PAREN_IZQ, ()
      expresion -> expr_simple comparacion
        expr_simple -> termino resto_e
          termino -> factor resto_t
            factor -> ID
              Emparejado: Token(ID, x)
            resto_t -> vacio
          resto_e -> vacio
        comparacion -> OP_REL expr_simple
          Emparejado: Token(OP_REL, >=)
          expr_simple -> termino resto_e
            termino -> factor resto_t
              factor -> NUM
                Emparejado: Token(NUM, 10)
              resto_t -> vacio
            resto_e -> vacio
      Emparejado: Token(PAREN_DER, ))
      Emparejado: Token(LLAVE_IZQ, {)
      sentencias -> sentencia sentencias
        sentencia -> ID '=' expresion ';'
          Emparejado: Token(ID, y)
          Emparejado: Token(ASIGNAR, =)
          expresion -> expr_simple comparacion
            expr_simple -> termino resto_e
              termino -> factor resto_t
                factor -> ID
                  Emparejado: Token(ID, x)
                resto_t -> vacio
              resto_e -> '+' termino resto_e
                Emparejado: Token(MAS, +)
                termino -> factor resto_t
                  factor -> NUM
                    Emparejado: Token(NUM, 1)
                  resto_t -> vacio
                resto_e -> vacio
            comparacion -> vacio
          Emparejado: Token(PUNTO_COMA, ;)
        sentencias -> vacio
      Emparejado: Token(LLAVE_DER, })
      parte_else -> ELSE '{' sentencias '}'
        Emparejado: Token(ELSE, else)
        Emparejado: Token(LLAVE_IZQ, {)
        sentencias -> sentencia sentencias
          sentencia -> ID '=' expresion ';'
            Emparejado: Token(ID, y)
            Emparejado: Token(ASIGNAR, =)
            expresion -> expr_simple comparacion
              expr_simple -> termino resto_e
                termino -> factor resto_t
                  factor -> NUM
                    Emparejado: Token(NUM, 0)
                  resto_t -> vacio
                resto_e -> vacio
              comparacion -> vacio
            Emparejado: Token(PUNTO_COMA, ;)
          sentencias -> vacio
        Emparejado: Token(LLAVE_DER, })
    sentencias -> vacio

>>> Parseo exitoso!

============================================================
 Prueba: Multiples sentencias
============================================================
 Codigo: a = 10;
    b = 20;
    c = a + b;
------------------------------------------------------------
 Tokens: [Token(ID, a), Token(ASIGNAR, =), Token(NUM, 10), Token(PUNTO_COMA, ;), Token(ID, b), Token(ASIGNAR, =), Token(NUM, 20), Token(PUNTO_COMA, ;), Token(ID, c), Token(ASIGNAR, =), Token(ID, a), Token(MAS, +), Token(ID, b), Token(PUNTO_COMA, ;)]

programa -> sentencias
  sentencias -> sentencia sentencias
    sentencia -> ID '=' expresion ';'
      Emparejado: Token(ID, a)
      Emparejado: Token(ASIGNAR, =)
      expresion -> expr_simple comparacion
        expr_simple -> termino resto_e
          termino -> factor resto_t
            factor -> NUM
              Emparejado: Token(NUM, 10)
            resto_t -> vacio
          resto_e -> vacio
        comparacion -> vacio
      Emparejado: Token(PUNTO_COMA, ;)
    sentencias -> sentencia sentencias
      sentencia -> ID '=' expresion ';'
        Emparejado: Token(ID, b)
        Emparejado: Token(ASIGNAR, =)
        expresion -> expr_simple comparacion
          expr_simple -> termino resto_e
            termino -> factor resto_t
              factor -> NUM
                Emparejado: Token(NUM, 20)
              resto_t -> vacio
            resto_e -> vacio
          comparacion -> vacio
        Emparejado: Token(PUNTO_COMA, ;)
      sentencias -> sentencia sentencias
        sentencia -> ID '=' expresion ';'
          Emparejado: Token(ID, c)
          Emparejado: Token(ASIGNAR, =)
          expresion -> expr_simple comparacion
            expr_simple -> termino resto_e
              termino -> factor resto_t
                factor -> ID
                  Emparejado: Token(ID, a)
                resto_t -> vacio
              resto_e -> '+' termino resto_e
                Emparejado: Token(MAS, +)
                termino -> factor resto_t
                  factor -> ID
                    Emparejado: Token(ID, b)
                  resto_t -> vacio
                resto_e -> vacio
            comparacion -> vacio
          Emparejado: Token(PUNTO_COMA, ;)
        sentencias -> vacio

>>> Parseo exitoso!

============================================================
 Prueba: Condicionales anidados
============================================================
 Codigo: if (x > 0) {
        if (x < 100) {
            y = x * 2;
        } else {
            y = 100;
        }
    }
------------------------------------------------------------
 Tokens: [Token(IF, if), Token(PAREN_IZQ, (), Token(ID, x), Token(OP_REL, >), Token(NUM, 0), Token(PAREN_DER, )), Token(LLAVE_IZQ, {), Token(IF, if), Token(PAREN_IZQ, (), Token(ID, x), Token(OP_REL, <), Token(NUM, 100), Token(PAREN_DER, )), Token(LLAVE_IZQ, {), Token(ID, y), Token(ASIGNAR, =), Token(ID, x), Token(POR, *), Token(NUM, 2), Token(PUNTO_COMA, ;), Token(LLAVE_DER, }), Token(ELSE, else), Token(LLAVE_IZQ, {), Token(ID, y), Token(ASIGNAR, =), Token(NUM, 100), Token(PUNTO_COMA, ;), Token(LLAVE_DER, }), Token(LLAVE_DER, })]

programa -> sentencias
  sentencias -> sentencia sentencias
    sentencia -> IF '(' expresion ')' '{' sentencias '}' parte_else
      Emparejado: Token(IF, if)
      Emparejado: Token(PAREN_IZQ, ()
      expresion -> expr_simple comparacion
        expr_simple -> termino resto_e
          termino -> factor resto_t
            factor -> ID
              Emparejado: Token(ID, x)
            resto_t -> vacio
          resto_e -> vacio
        comparacion -> OP_REL expr_simple
          Emparejado: Token(OP_REL, >)
          expr_simple -> termino resto_e
            termino -> factor resto_t
              factor -> NUM
                Emparejado: Token(NUM, 0)
              resto_t -> vacio
            resto_e -> vacio
      Emparejado: Token(PAREN_DER, ))
      Emparejado: Token(LLAVE_IZQ, {)
      sentencias -> sentencia sentencias
        sentencia -> IF '(' expresion ')' '{' sentencias '}' parte_else
          Emparejado: Token(IF, if)
          Emparejado: Token(PAREN_IZQ, ()
          expresion -> expr_simple comparacion
            expr_simple -> termino resto_e
              termino -> factor resto_t
                factor -> ID
                  Emparejado: Token(ID, x)
                resto_t -> vacio
              resto_e -> vacio
            comparacion -> OP_REL expr_simple
              Emparejado: Token(OP_REL, <)
              expr_simple -> termino resto_e
                termino -> factor resto_t
                  factor -> NUM
                    Emparejado: Token(NUM, 100)
                  resto_t -> vacio
                resto_e -> vacio
          Emparejado: Token(PAREN_DER, ))
          Emparejado: Token(LLAVE_IZQ, {)
          sentencias -> sentencia sentencias
            sentencia -> ID '=' expresion ';'
              Emparejado: Token(ID, y)
              Emparejado: Token(ASIGNAR, =)
              expresion -> expr_simple comparacion
                expr_simple -> termino resto_e
                  termino -> factor resto_t
                    factor -> ID
                      Emparejado: Token(ID, x)
                    resto_t -> '*' factor resto_t
                      Emparejado: Token(POR, *)
                      factor -> NUM
                        Emparejado: Token(NUM, 2)
                      resto_t -> vacio
                  resto_e -> vacio
                comparacion -> vacio
              Emparejado: Token(PUNTO_COMA, ;)
            sentencias -> vacio
          Emparejado: Token(LLAVE_DER, })
          parte_else -> ELSE '{' sentencias '}'
            Emparejado: Token(ELSE, else)
            Emparejado: Token(LLAVE_IZQ, {)
            sentencias -> sentencia sentencias
              sentencia -> ID '=' expresion ';'
                Emparejado: Token(ID, y)
                Emparejado: Token(ASIGNAR, =)
                expresion -> expr_simple comparacion
                  expr_simple -> termino resto_e
                    termino -> factor resto_t
                      factor -> NUM
                        Emparejado: Token(NUM, 100)
                      resto_t -> vacio
                    resto_e -> vacio
                  comparacion -> vacio
                Emparejado: Token(PUNTO_COMA, ;)
              sentencias -> vacio
            Emparejado: Token(LLAVE_DER, })
        sentencias -> vacio
      Emparejado: Token(LLAVE_DER, })
      parte_else -> vacio
    sentencias -> vacio

>>> Parseo exitoso!

============================================================
 Prueba: Expresion con parentesis
============================================================
 Codigo: z = (a + b) * (c - d);
------------------------------------------------------------
 Tokens: [Token(ID, z), Token(ASIGNAR, =), Token(PAREN_IZQ, (), Token(ID, a), Token(MAS, +), Token(ID, b), Token(PAREN_DER, )), Token(POR, *), Token(PAREN_IZQ, (), Token(ID, c), Token(MENOS, -), Token(ID, d), Token(PAREN_DER, )), Token(PUNTO_COMA, ;)]

programa -> sentencias
  sentencias -> sentencia sentencias
    sentencia -> ID '=' expresion ';'
      Emparejado: Token(ID, z)
      Emparejado: Token(ASIGNAR, =)
      expresion -> expr_simple comparacion
        expr_simple -> termino resto_e
          termino -> factor resto_t
            factor -> '(' expresion ')'
              Emparejado: Token(PAREN_IZQ, ()
              expresion -> expr_simple comparacion
                expr_simple -> termino resto_e
                  termino -> factor resto_t
                    factor -> ID
                      Emparejado: Token(ID, a)
                    resto_t -> vacio
                  resto_e -> '+' termino resto_e
                    Emparejado: Token(MAS, +)
                    termino -> factor resto_t
                      factor -> ID
                        Emparejado: Token(ID, b)
                      resto_t -> vacio
                    resto_e -> vacio
                comparacion -> vacio
              Emparejado: Token(PAREN_DER, ))
            resto_t -> '*' factor resto_t
              Emparejado: Token(POR, *)
              factor -> '(' expresion ')'
                Emparejado: Token(PAREN_IZQ, ()
                expresion -> expr_simple comparacion
                  expr_simple -> termino resto_e
                    termino -> factor resto_t
                      factor -> ID
                        Emparejado: Token(ID, c)
                      resto_t -> vacio
                    resto_e -> '-' termino resto_e
                      Emparejado: Token(MENOS, -)
                      termino -> factor resto_t
                        factor -> ID
                          Emparejado: Token(ID, d)
                        resto_t -> vacio
                      resto_e -> vacio
                  comparacion -> vacio
                Emparejado: Token(PAREN_DER, ))
              resto_t -> vacio
          resto_e -> vacio
        comparacion -> vacio
      Emparejado: Token(PUNTO_COMA, ;)
    sentencias -> vacio

>>> Parseo exitoso!

============================================================
 Prueba: Condicional con comparacion !=
============================================================
 Codigo: if (valor != 0) {
        resultado = 100 / valor;
    }
------------------------------------------------------------
 Tokens: [Token(IF, if), Token(PAREN_IZQ, (), Token(ID, valor), Token(OP_REL, !=), Token(NUM, 0), Token(PAREN_DER, )), Token(LLAVE_IZQ, {), Token(ID, resultado), Token(ASIGNAR, =), Token(NUM, 100), Token(DIVIDIR, /), Token(ID, valor), Token(PUNTO_COMA, ;), Token(LLAVE_DER, })]

programa -> sentencias
  sentencias -> sentencia sentencias
    sentencia -> IF '(' expresion ')' '{' sentencias '}' parte_else
      Emparejado: Token(IF, if)
      Emparejado: Token(PAREN_IZQ, ()
      expresion -> expr_simple comparacion
        expr_simple -> termino resto_e
          termino -> factor resto_t
            factor -> ID
              Emparejado: Token(ID, valor)
            resto_t -> vacio
          resto_e -> vacio
        comparacion -> OP_REL expr_simple
          Emparejado: Token(OP_REL, !=)
          expr_simple -> termino resto_e
            termino -> factor resto_t
              factor -> NUM
                Emparejado: Token(NUM, 0)
              resto_t -> vacio
            resto_e -> vacio
      Emparejado: Token(PAREN_DER, ))
      Emparejado: Token(LLAVE_IZQ, {)
      sentencias -> sentencia sentencias
        sentencia -> ID '=' expresion ';'
          Emparejado: Token(ID, resultado)
          Emparejado: Token(ASIGNAR, =)
          expresion -> expr_simple comparacion
            expr_simple -> termino resto_e
              termino -> factor resto_t
                factor -> NUM
                  Emparejado: Token(NUM, 100)
                resto_t -> '/' factor resto_t
                  Emparejado: Token(DIVIDIR, /)
                  factor -> ID
                    Emparejado: Token(ID, valor)
                  resto_t -> vacio
              resto_e -> vacio
            comparacion -> vacio
          Emparejado: Token(PUNTO_COMA, ;)
        sentencias -> vacio
      Emparejado: Token(LLAVE_DER, })
      parte_else -> vacio
    sentencias -> vacio

>>> Parseo exitoso!

============================================================
 Prueba: Error: falta punto y coma
============================================================
 Codigo: x = 5
------------------------------------------------------------
 Tokens: [Token(ID, x), Token(ASIGNAR, =), Token(NUM, 5)]

programa -> sentencias
  sentencias -> sentencia sentencias
    sentencia -> ID '=' expresion ';'
      Emparejado: Token(ID, x)
      Emparejado: Token(ASIGNAR, =)
      expresion -> expr_simple comparacion
        expr_simple -> termino resto_e
          termino -> factor resto_t
            factor -> NUM
              Emparejado: Token(NUM, 5)
            resto_t -> vacio
          resto_e -> vacio
        comparacion -> vacio

>>> ERROR: Error: se esperaba 'PUNTO_COMA' pero se llego al final de la entrada

============================================================
 Prueba: Error: falta llave
============================================================
 Codigo: if (x > 0)
        y = 1;
------------------------------------------------------------
 Tokens: [Token(IF, if), Token(PAREN_IZQ, (), Token(ID, x), Token(OP_REL, >), Token(NUM, 0), Token(PAREN_DER, )), Token(ID, y), Token(ASIGNAR, =), Token(NUM, 1), Token(PUNTO_COMA, ;)]

programa -> sentencias
  sentencias -> sentencia sentencias
    sentencia -> IF '(' expresion ')' '{' sentencias '}' parte_else
      Emparejado: Token(IF, if)
      Emparejado: Token(PAREN_IZQ, ()
      expresion -> expr_simple comparacion
        expr_simple -> termino resto_e
          termino -> factor resto_t
            factor -> ID
              Emparejado: Token(ID, x)
            resto_t -> vacio
          resto_e -> vacio
        comparacion -> OP_REL expr_simple
          Emparejado: Token(OP_REL, >)
          expr_simple -> termino resto_e
            termino -> factor resto_t
              factor -> NUM
                Emparejado: Token(NUM, 0)
              resto_t -> vacio
            resto_e -> vacio
      Emparejado: Token(PAREN_DER, ))

>>> ERROR: Error en linea 3: se esperaba 'LLAVE_IZQ', se encontro 'ID' (valor: 'y')
[rerun: b11]