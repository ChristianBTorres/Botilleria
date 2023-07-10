from flask import Flask, render_template, request, redirect, url_for
from db import dbConnection
from models import Producto, Proveedor
from bson.objectid import ObjectId

db = dbConnection()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def obtener_proveedores():
    productos = db['productos']
    proveedores = db['proveedores']
    lista_productos = []
    for x in productos.find():
        try:
            new_supplier = proveedores.find_one({'_id': ObjectId(x['proveedor'])})
            x['proveedor'] = new_supplier['nombre']
        except:
            x['proveedor'] = 'Sin proveedor'

        try: 
            x['precio'] = int(x['precio'])
            x['precio'] = f"${x['precio']:,.0f}"
        except:
            x['precio'] = "Sin precio"
        lista_productos.append(x)
    return lista_productos


# PROVEEDORES
@app.route('/suppliers')
def suppliers():
    proveedores = db['proveedores']
    return render_template('proveedor.html', proveedores=proveedores.find())


@app.route('/add/supplier', methods=['POST'])
def add_supplier():
    if request.method == 'POST':
        proveedores = db['proveedores']
        name = request.form['nombre']
        rut = request.form['rut']
        phone = request.form['telefono']
        email = request.form['correo']
        address = request.form['direccion']
        proveedor = Proveedor(name, rut, phone, email, address)
        proveedores.insert_one(proveedor.toDbCollection())
        return redirect(url_for('suppliers'))


@app.route('/delete/supplier/<id>')
def delete_supplier(id):
    proveedores = db['proveedores']
    proveedores.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('suppliers'))


@app.route('/edit/supplier/<id>', methods=['GET', 'POST'])
def edit_supplier(id):
    proveedores = db['proveedores']
    if request.method == 'GET':
        proveedor = proveedores.find_one({'_id': ObjectId(id)})
        return render_template('edit_supplier.html', proveedor=proveedor, proveedores=proveedores.find())
    else:
        name = request.form['nombre']
        rut = request.form['rut']
        phone = request.form['telefono']
        email = request.form['correo']
        address = request.form['direccion']
        proveedores.update_one({'_id': ObjectId(id)}, {'$set': {
                               'nombre': name, 'rut': rut, 'telefono': phone, 'correo': email, 'direccion': address}})
        return redirect(url_for('suppliers'))


# PRODUCTOS
@app.route('/products')  # MOSTRAR PRODUCTOS
def products():
    proveedores = db['proveedores']
    return render_template('producto.html', productos=obtener_proveedores(), proveedores=proveedores.find())


@app.route('/add/product', methods=['POST'])  # AGREGAR PRODUCTOS
def add_product():
    if request.method == 'POST':
        productos = db['productos']
        name = request.form['nombre']
        price = request.form['precio']
        stock = request.form['stock']
        supplier = request.form['proveedor']
        producto = Producto(name, int(price), int(stock), supplier)
        productos.insert_one(producto.toDbCollection())
        return redirect(url_for('products'))


@app.route('/delete/product/<id>')  # ELIMINAR PRODUCTOS
def delete_product(id):
    productos = db['productos']
    productos.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('products'))


@app.route('/edit/product/<id>', methods=['GET', 'POST'])  # EDITAR PRODUCTOS
def edit_product(id):
    productos = db['productos']
    db_proveedores = db['proveedores']
    if request.method == 'GET':  # MOSTRAR FORMULARIO EDICION
        producto = productos.find_one({'_id': ObjectId(id)})
        return render_template('edit_product.html', producto=producto, proveedores_list=db_proveedores.find(), productos=obtener_proveedores())
    else:  # GUARDAR EDICION
        name = request.form['nombre']
        price = request.form['precio']
        stock = request.form['stock']
        supplier = request.form['proveedor']
        productos.update_one({'_id': ObjectId(id)}, {'$set': {
                             'nombre': name, 'precio': price, 'stock': stock, 'proveedor': supplier}})
        return redirect(url_for('products'))


if __name__ == '__main__':
    app.run(debug=True, port=8000)
