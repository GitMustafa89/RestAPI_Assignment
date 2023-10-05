from flask import Flask, render_template, request,jsonify
from flask_mysqldb import MySQL

app= Flask(__name__)
mysql = MySQL(app)


app.config ['MYSQL_HOST'] = 'localhost'
app.config ['MYSQL_USER'] = 'mustafa'
app.config ['MYSQL_PASSWORD'] = "Mustafa@1989"
app.config ['MYSQL_DB'] = 'my_db_product'

@app.route("/", methods = ['GET','POST']) 
def index():
    if request.method == 'POST':
        username= request.form['username']
        email= request.form['email']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name,email) values (%s,%s)",(username,email))
        mysql.connection.commit()
        cur.close()
        return "Successfully updated Record in Database"
    return render_template('index.html')

@app.route("/users")
def getusers():
    cur = mysql.connection.cursor()
    user = cur.execute("SELECT * FROM users")
    if user >0:
        userDetails = cur.fetchall()
    return render_template('users.html', myuser=userDetails)

# Manage Orders
orders = []
@app.route('/order', methods=['GET', 'POST'])
def manage_orders():
    if request.method == 'GET':
        # Return a list of orders
        return jsonify(orders)
    elif request.method == 'POST':
        # Create a new order
        data = request.json
        if 'customer' in data and 'product' in data and 'quantity' in data:
            new_order = {
                'customer': data['customer'],
                'product': data['product'],
                'quantity': data['quantity']
            }
            orders.append(new_order)
            return jsonify({'message': 'Order created successfully'}), 201
        else:
            return jsonify({'error': 'Incomplete order data'}), 400

orders = [
   {
        "customer": "Mustafa",
        "product": "product1",
        "quantity": "1"
    },
    {
        "customer": "Altaf",
        "product": "product1",
        "quantity": "2"
    },
    {
        "customer": "Usama",
        "product": "product3",
        "quantity": "3"
    },
]

# Show orders
@app.route('/allorders', methods=['GET'])
def get_all_orders():
    return jsonify({'orders': orders})


# Sample product data (you would typically fetch this from a database)
products = [
    {"id": 1, "name": "Tea", "price": 280},
    {"id": 2, "name": "Sugar", "price": 150},
    {"id": 3, "name": "Rice", "price": 320},
]

@app.route('/getallproducts', methods=['GET'])
def get_all_products():
    return jsonify(products)

# Add new products
@app.route('/addproduct', methods=['POST'])
def add_product():
  
        # Parse JSON data from the request
        data = request.get_json()

        # Validate the request data
        if 'name' not in data or 'price' not in data:
            return jsonify({"error": "Name and price are required"}), 400

        # Create a new product
        product = {
            "id":data["id"],
            'name': data['name'],
            'price': data['price']
        }
        products.append(product)

        # Add the product to the list
        products.append(product)

        return jsonify({"message": "Product added successfully"}), 201

# Update a product
@app.route('/updateproduct/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
    name = data['name']
    description = data['description']
    price = data['price']

    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE products SET name=%s, description=%s, price=%s WHERE id=%s", (name, description, price, product_id))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "Product updated successfully"}), 200


# # Update a product
# @app.route('/updateproduct/<int:product_id>', methods=['PUT'])
   
# def update_product(product_id):
#     id=product_id
#     if id not in products:
#         return jsonify({"error": "Product not found"}), 404

#     data = request.get_json()
#     if "name" in data:
#         products[id]["name"] = data["name"]
#     if "price" in data:
#         products[id]["price"] = data["price"]

#     return jsonify(products[id])

# Delete a product
@app.route('/deleteproduct/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM products WHERE id=%s", (product_id,))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "Product deleted successfully"}), 200


# # Delete a product
# @app.route('/deleteproduct/<int:product_id>', methods=['DELETE'])
# def delete_product(product_id):
#     if product_id not in products:
#         return jsonify({"error": "Product not found"}), 404

#     del products[product_id]
#     return jsonify({"message": "Product deleted"})

        
if __name__ == "__main__":
    app.run(debug=True)
        