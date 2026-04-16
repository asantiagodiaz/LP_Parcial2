from lexer import lexer
from parser_nosql import parser

# Pruebas del lenguaje NoSQL
pruebas = [
    # 1. Crear base de datos
    'CREAR BASE miTienda;',

    # 2. Usar base de datos
    'USAR miTienda;',

    # 3. Crear coleccion
    'CREAR COLECCION productos;',

    # 4. Insertar un documento
    'INSERTAR EN productos DOCUMENTO {"nombre": "Laptop", "precio": 2500000, "disponible": verdadero};',

    # 5. Insertar con documento anidado
    'INSERTAR EN productos DOCUMENTO {"nombre": "Celular", "precio": 1200000, "specs": {"ram": 8, "almacenamiento": 128}};',

    # 6. Insertar con lista
    'INSERTAR EN productos DOCUMENTO {"nombre": "Tablet", "colores": ["negro", "blanco", "azul"]};',

    # 7. Buscar todos los documentos
    'BUSCAR EN productos TODO;',

    # 8. Buscar con condicion
    'BUSCAR EN productos DONDE "precio" > 1000000;',

    # 9. Buscar con condiciones compuestas
    'BUSCAR EN productos DONDE "precio" >= 500000 Y "disponible" == verdadero;',

    # 10. Actualizar un documento
    'ACTUALIZAR EN productos DONDE "nombre" == "Laptop" CON {"precio": 2300000};',

    # 11. Eliminar un documento
    'ELIMINAR EN productos DONDE "nombre" == "Tablet";',

    # 12. Varias sentencias juntas
    'CREAR BASE universidad; USAR universidad; CREAR COLECCION estudiantes;',

    # 13. Insertar y buscar
    'INSERTAR EN estudiantes DOCUMENTO {"nombre": "Carlos", "semestre": 5, "activo": verdadero}; BUSCAR EN estudiantes TODO;',
]

# Tambien probamos algunos casos que deben dar error
pruebas_error = [
    # Falta el punto y coma
    'CREAR BASE test',
    # Palabra no reconocida
    'SELECCIONAR EN productos TODO;',
    # Documento mal formado
    'INSERTAR EN col DOCUMENTO {"nombre": };',
]


if __name__ == "__main__":
    print("=" * 60)
    print("  PRUEBAS DEL PARSER NOSQL")
    print("  Implementado con PLY (Python Lex-Yacc)")
    print("=" * 60)

    for i, prueba in enumerate(pruebas, 1):
        print(f"\n--- Prueba {i} ---")
        print(f"Entrada: {prueba}")
        lexer.lineno = 1
        try:
            resultado = parser.parse(prueba, lexer=lexer)
        except Exception as e:
            print(f"Excepcion: {e}")

    print("\n" + "=" * 60)
    print("  PRUEBAS CON ERRORES (deben mostrar error)")
    print("=" * 60)

    for i, prueba in enumerate(pruebas_error, 1):
        print(f"\n--- Error {i} ---")
        print(f"Entrada: {prueba}")
        lexer.lineno = 1
        try:
            resultado = parser.parse(prueba, lexer=lexer)
        except Exception as e:
            print(f"Excepcion: {e}")
