from flask import Flask, render_template, request, Response, jsonify, redirect, url_for
import database as dbase
from product import Product

db = dbase.dbConnection() # accedemos a la funcion dentro de la configuracion

app = Flask(__name__)  #instancia de flask

# routes app
@app.route('/')
def home():
    products = db['products']
    productsReceived = products.find()
    
    return render_template('index.html', products = productsReceived)

# POST
@app.route('/product', methods =['POST'])
def addProduct():
    products = db['products']
    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']
    
    if name and price and quantity:
        product = Product(name, price, quantity)
        #insertamos en la base de datos
        products.insert_one(product.toDBCollection()) # toDBCollection es el modelo en product
        
        response = jsonify({
            'name': name,
            'price': price,
            'quantity': quantity,
        })
        return redirect(url_for('home'))
    else:
        return notFound()
    
# DELETE
@app.route('/delete/<string:product_name>')
def delete(product_name):
    products = db['products']
    products.delete_one({'name': product_name})
    return redirect(url_for('home'))

# PUT
@app.route('/edit/<string:product_name>', methods=['PUT'])
def edit(product_name):
    products = db['products']
    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']
    
    if name and price and quantity:
        products.update_one({'name': product_name}, {'$set': {'name': name, 'price': price, 'quantity': quantity}})
        response = jsonify({'message': 'Producto' + product_name + 'actualizado correctamente'})
        return redirect(url_for('home'))
    else:
        return notFound()
        
@app.errorhandler(404)
def notFound(error=None):
    message = {
        'message': 'No encontrado' + request.url,
        'status': '404 Not Found'
    }
    response = jsonify(message)
    response.status_code = 404
    return response  
        
# para lanzar la aplicacion
 
if __name__ == 'main':
  app.run(debug=true, port=4000)

