import sqlite3

# Crear la base de datos y las tablas
conexion = sqlite3.connect('inventario.db')
cursor = conexion.cursor()

# Crear tabla de productos
cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        categoria TEXT,
        precio REAL,
        stock INTEGER
    )
''')

# Crear tabla de movimientos (entradas/salidas de productos)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS movimientos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        producto_id INTEGER,
        tipo TEXT,  # 'entrada' o 'salida'
        cantidad INTEGER,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (producto_id) REFERENCES productos(id)
    )
''')

# Crear índices para optimización en nombre y categoría
cursor.execute('CREATE INDEX IF NOT EXISTS idx_nombre ON productos(nombre)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_categoria ON productos(categoria)')

# Insertar productos de ejemplo
productos = [
    ("Laptop Lenovo", "Tecnología", 2200.00, 5),
    ("Mouse Logitech", "Accesorios", 45.00, 20),
    ("Monitor Samsung", "Pantallas", 850.00, 10)
]

cursor.executemany("INSERT INTO productos (nombre, categoria, precio, stock) VALUES (?, ?, ?, ?)", productos)

conexion.commit()
conexion.close()

print("✅ Base de datos creada con índices para optimización.")
