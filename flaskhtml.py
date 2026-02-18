from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

username = os.getlogin()
globalstuff = {
    "NAME": __name__,
    "USERNAME": username,

    "ITEM_COUNT": "12" #placeholder
}

@app.route('/') # Flask lwk confusing i cant link css or html how it's normally done
def home():
    return render_template('home.html', **globalstuff)
#end

@app.route('/shop')
def shop():

    with sqlite3.connect("Databases/products.db") as database:
        c = database.cursor()
        c.execute("SELECT * from Products")
        products = c.fetchall()
        
        products_globals = []

        for p in products:
            products_globals.append({
                "name": p[0],
                "price": p[1],
                "image": p[2]
            })
            print(products_globals)
            #end
        #end
    #end

    return render_template('shop.html', **globalstuff, PRODUCTS = products_globals)
#end

@app.route('/search', methods = ["POST"])
def search():
    searched = request.form.get("SEARCH_BOX").strip()
    return render_template('search.html', **globalstuff, SEARCH_QUERY = searched)
#end

if __name__ == '__main__':
    app.run(debug=True)
#end