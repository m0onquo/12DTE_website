from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

username = os.getlogin()
globalstuff = {
    "NAME": __name__,
    "USERNAME": username
}

@app.route('/')
def home():
    return render_template('webpage.html', **globalstuff)
#end

if __name__ == '__main__':
    app.run(debug=True)
#end