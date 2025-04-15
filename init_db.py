import sqlite3

conexion = sqlite3.connect('inventario.db')
cursor = conexion.cursor()

# Crear tabla de productos
cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        categoria TEXT NOT NULL,
        precio REAL NOT NULL,
        stock INTEGER NOT NULL
    )
''')

# Crear tabla de movimientos
cursor.execute('''
    CREATE TABLE IF NOT EXISTS movimientos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        producto_id INTEGER,
        tipo TEXT NOT NULL,
        cantidad INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        FOREIGN KEY (producto_id) REFERENCES productos (id)
    )
''')

conexion.commit()
conexion.close()

print("✅ Base de datos inicializada con éxito.")
