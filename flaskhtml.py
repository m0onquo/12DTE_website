from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
import os
import uuid

# For Webhook
import json
import requests

myID = uuid.uuid4()
app = Flask(__name__)
app.secret_key = "very_cool_password"

username = os.getlogin()
globalstuff = {
    "NAME": __name__,
    "USERNAME": username,
}

products_globals = []
with sqlite3.connect("Databases/products.db") as database:
        c = database.cursor()
        c.execute("SELECT * FROM Products")
        products = c.fetchall()

        for p in products:
            products_globals.append({
                "name": p[0],
                "price": p[1],
                "image": p[2],
                "keywords": p[3],
                "id":   p[4]
            })
            #end
        #end
    #end
#end

def sortproducts(by, itemlist):
    if by == "NONE": return itemlist #end
    
    sortedstuff = sorted(itemlist, key=lambda product: product[by])
    return sortedstuff
#end

@app.route('/') # Flask lwk confusing i cant link css or html how it's normally done
def home():
    return render_template('home.html', **globalstuff, globalProducts = products_globals)
#end

@app.route('/shop/') # cool you can do multiple so now you can add a default value and not have to specify no filter each time you go to shop page
@app.route('/shop/<string:SORT>')
def shop(SORT="NONE"):
    sort_key = SORT.lower() if SORT.lower() in ["name", "price", "id"] else "id"
    
    p = sortproducts(sort_key, products_globals)
    
    return render_template('shop.html', **globalstuff, globalProducts = p)
#end

@app.route('/search', methods = ["POST"])
def search():
    searched = request.form.get("SEARCH_BOX").strip()
    if not searched.isalpha():
        cleaned_chars = [char for char in searched if char.isalpha()]
        cleaned_text = "".join(cleaned_chars)
            #end
        #end
    #end

    search_term = f"%{searched}%" # Not sure why it has to be this way but this lets you search without needing exact match

    with sqlite3.connect("Databases/products.db") as database:
        c = database.cursor()
        c.execute("SELECT * FROM Products WHERE keywords LIKE ?", (search_term,)) # No funny SQL stuff
        products = c.fetchall()
        
        productsL = []

        for p in products:
            productsL.append({
                "name": p[0],
                "price": p[1],
                "image": p[2],
                "keywords": p[3],
                "id":   p[4]
            })
            #end
        #end
    #end
    return render_template('search.html', **globalstuff, SEARCH_QUERY = searched, PRODUCTS = productsL, globalProducts = products_globals)
#end

@app.route('/product/<int:ID>')
def display_product(ID):
    with sqlite3.connect("Databases/products.db") as database:
        c = database.cursor()
        c.execute("SELECT * FROM Products WHERE ID = ?", (ID,))
        product = c.fetchone()
    #end
    return render_template('display_product.html', **globalstuff, PRODUCT=product, globalProducts=products_globals)
#end

@app.route('/cart_add/<int:item_id>')
def add_cart(item_id):
    cart = session.get('cart', {})

    string_id = str(item_id) 
    cart[string_id] = cart.get(string_id, 0) + 1
    session['cart'] = cart
    session.modified = True
    return redirect(url_for('view_cart', globalProducts=products_globals))
#end
@app.route('/cart_remove/<int:item_id>')
def remove_from_cart(item_id):
    cart = session.get('cart', {})
    string_id = str(item_id)

    if string_id in cart:
        if cart[string_id] > 1:
            cart[string_id] -= 1
        else:
            cart.pop(string_id)
        #end
    #end
            
    session['cart'] = cart
    session.modified = True
    return redirect(url_for('view_cart', globalProducts=products_globals))
#end

@app.route('/cart')
def view_cart():
    cart = session.get('cart', {})
    display_cart = []
    total_price = 0

    with sqlite3.connect("Databases/products.db") as database:
        c = database.cursor()
        for item_id, quantity in cart.items():
            if not str(item_id).isdigit():
                continue 
            
            c.execute("SELECT Item, Price, Image FROM Products WHERE ID = ?", (int(item_id),))
            product = c.fetchone()
            
            if product:
                name, price, image = product[0], product[1], product[2]
                
                subtotal = price * quantity
                total_price += subtotal
                
                display_cart.append({
                    "id": item_id,
                    "name": name,
                    "price": price,
                    "image": image,
                    "quantity": quantity,
                    "subtotal": f"{subtotal:.2f}"
                })

    return render_template('cart.html', **globalstuff, CART_ITEMS=display_cart, TOTAL=f"{total_price:.2f}", globalProducts=products_globals) # Rounding the annoying decimals
#end

@app.route("/purchase")
def purchase():
    return render_template("purchase.html", **globalstuff, globalProducts=products_globals)
#end

if __name__ == '__main__':
    app.run(debug=True)
#end