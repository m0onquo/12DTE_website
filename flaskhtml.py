from flask import Flask, render_template, request
import sqlite3
app = Flask(__name__)


def searchdatabase(query):
    temp = "'" + query + "'" 
    with sqlite3.connect("flask/Databases/testing.db") as database:
        try:
            cursor = database.cursor()
            search = cursor.execute("SELECT * FROM Students WHERE Name= " + temp + ";" )
            result = cursor.fetchall()
        except sqlite3.OperationalError: return "Not Found"

    if len(result) == 0: return "No Found"
    return ", ".join(str(item) for item in result[0])
#end


@app.route('/')
def home():
    return render_template('webpage.html', NAME = __name__)
#end

@app.route("/search", methods = ["POST"])
def search():
    query = request.form.get("query_box")    
    return render_template('webpage.html', search_query = searchdatabase(query), )
#end

if __name__ == '__main__':
    app.run(debug=True)
#end