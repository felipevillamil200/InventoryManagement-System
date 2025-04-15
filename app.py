from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Crear base de datos y tablas si no existen
def init_db():
    conexion = sqlite3.connect('inventario.db')
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT,
            precio REAL,
            stock INTEGER
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movimientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER,
            tipo TEXT,
            cantidad INTEGER,
            fecha TEXT,
            FOREIGN KEY (producto_id) REFERENCES productos(id)
        )
    ''')
    conexion.commit()
    conexion.close()

init_db()

@app.route('/')
def index():
    conexion = sqlite3.connect('inventario.db')
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conexion.close()
    return render_template('index.html', productos=productos)

@app.route('/agregar', methods=['POST'])
def agregar_producto():
    nombre = request.form['nombre']
    categoria = request.form['categoria']
    precio = float(request.form['precio'])
    stock = int(request.form['stock'])

    conexion = sqlite3.connect('inventario.db')
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO productos (nombre, categoria, precio, stock) VALUES (?, ?, ?, ?)",
                   (nombre, categoria, precio, stock))
    conexion.commit()
    conexion.close()
    return redirect(url_for('index'))

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        precio = float(request.form['precio'])
        stock = int(request.form['stock'])

        cursor.execute("""
            UPDATE productos
            SET nombre = ?, categoria = ?, precio = ?, stock = ?
            WHERE id = ?
        """, (nombre, categoria, precio, stock, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    else:
        cursor.execute("SELECT * FROM productos WHERE id = ?", (id,))
        producto = cursor.fetchone()
        conn.close()
        return render_template('editar.html', producto=producto)


@app.route('/eliminar/<int:id>')
def eliminar_producto(id):
    conexion = sqlite3.connect('inventario.db')
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM productos WHERE id=?", (id,))
    conexion.commit()
    conexion.close()
    return redirect(url_for('index'))

@app.route('/movimiento/<int:id>', methods=['GET', 'POST'])
def registrar_movimiento(id):
    conexion = sqlite3.connect('inventario.db')
    cursor = conexion.cursor()

    if request.method == 'POST':
        tipo = request.form['tipo']
        cantidad = int(request.form['cantidad'])
        fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute("INSERT INTO movimientos (producto_id, tipo, cantidad, fecha) VALUES (?, ?, ?, ?)",
                       (id, tipo, cantidad, fecha))

        if tipo == 'entrada':
            cursor.execute("UPDATE productos SET stock = stock + ? WHERE id = ?", (cantidad, id))
        elif tipo == 'salida':
            cursor.execute("UPDATE productos SET stock = stock - ? WHERE id = ?", (cantidad, id))

        conexion.commit()
        conexion.close()
        return redirect(url_for('index'))

    cursor.execute("SELECT nombre FROM productos WHERE id = ?", (id,))
    producto = cursor.fetchone()
    conexion.close()
    return render_template('movimiento.html', producto=producto, id=id)

@app.route('/movimientos')
def ver_movimientos():
    conexion = sqlite3.connect('inventario.db')
    cursor = conexion.cursor()
    cursor.execute('''
        SELECT m.id, p.nombre, m.tipo, m.cantidad, m.fecha
        FROM movimientos m
        JOIN productos p ON m.producto_id = p.id
    ''')
    movimientos = cursor.fetchall()
    conexion.close()
    return render_template('movimientos.html', movimientos=movimientos)

if __name__ == '__main__':
    app.run(debug=True)
