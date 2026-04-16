Generating LALR tables
============================================================
  PRUEBAS DEL PARSER NOSQL
  Implementado con PLY (Python Lex-Yacc)
============================================================

--- Prueba 1 ---
Entrada: CREAR BASE miTienda;
  [CREAR BD] nombre: miTienda
>>> Programa parseado correctamente

--- Prueba 2 ---
Entrada: USAR miTienda;
  [USAR BD] nombre: miTienda
>>> Programa parseado correctamente

--- Prueba 3 ---
Entrada: CREAR COLECCION productos;
  [CREAR COLECCION] nombre: productos
>>> Programa parseado correctamente

--- Prueba 4 ---
Entrada: INSERTAR EN productos DOCUMENTO {"nombre": "Laptop", "precio": 2500000, "disponible": verdadero};
  [INSERTAR] en coleccion: productos, documento: {'nombre': 'Laptop', 'precio': 2500000, 'disponible': True}
>>> Programa parseado correctamente

--- Prueba 5 ---
Entrada: INSERTAR EN productos DOCUMENTO {"nombre": "Celular", "precio": 1200000, "specs": {"ram": 8, "almacenamiento": 128}};
  [INSERTAR] en coleccion: productos, documento: {'nombre': 'Celular', 'precio': 1200000, 'specs': {'ram': 8, 'almacenamiento': 128}}
>>> Programa parseado correctamente

--- Prueba 6 ---
Entrada: INSERTAR EN productos DOCUMENTO {"nombre": "Tablet", "colores": ["negro", "blanco", "azul"]};
  [INSERTAR] en coleccion: productos, documento: {'nombre': 'Tablet', 'colores': ['negro', 'blanco', 'azul']}
>>> Programa parseado correctamente

--- Prueba 7 ---
Entrada: BUSCAR EN productos TODO;
  [BUSCAR] todos los documentos en: productos
>>> Programa parseado correctamente

--- Prueba 8 ---
Entrada: BUSCAR EN productos DONDE "precio" > 1000000;
  [BUSCAR] en productos donde precio > 1000000
>>> Programa parseado correctamente

--- Prueba 9 ---
Entrada: BUSCAR EN productos DONDE "precio" >= 500000 Y "disponible" == verdadero;
  [BUSCAR] en productos donde (precio >= 500000 Y disponible == True)
>>> Programa parseado correctamente

--- Prueba 10 ---
Entrada: ACTUALIZAR EN productos DONDE "nombre" == "Laptop" CON {"precio": 2300000};
  [ACTUALIZAR] en productos donde nombre == Laptop con {'precio': 2300000}
>>> Programa parseado correctamente

--- Prueba 11 ---
Entrada: ELIMINAR EN productos DONDE "nombre" == "Tablet";
  [ELIMINAR] de productos donde nombre == Tablet
>>> Programa parseado correctamente

--- Prueba 12 ---
Entrada: CREAR BASE universidad; USAR universidad; CREAR COLECCION estudiantes;
  [CREAR BD] nombre: universidad
  [USAR BD] nombre: universidad
  [CREAR COLECCION] nombre: estudiantes
>>> Programa parseado correctamente

--- Prueba 13 ---
Entrada: INSERTAR EN estudiantes DOCUMENTO {"nombre": "Carlos", "semestre": 5, "activo": verdadero}; BUSCAR EN estudiantes TODO;
  [INSERTAR] en coleccion: estudiantes, documento: {'nombre': 'Carlos', 'semestre': 5, 'activo': True}
  [BUSCAR] todos los documentos en: estudiantes
>>> Programa parseado correctamente

============================================================
  PRUEBAS CON ERRORES (deben mostrar error)
============================================================

--- Error 1 ---
Entrada: CREAR BASE test
  [CREAR BD] nombre: test
Error de sintaxis: se esperaban mas tokens

--- Error 2 ---
Entrada: SELECCIONAR EN productos TODO;
Error de sintaxis en 'SELECCIONAR', linea 1

--- Error 3 ---
Entrada: INSERTAR EN col DOCUMENTO {"nombre": };
Error de sintaxis en '}', linea 1
[rerun: b7]