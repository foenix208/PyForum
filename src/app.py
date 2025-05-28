from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import  hashlib # importe librairy pour hashage  

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")    


@app.route("/signup", methods=["GET", "POST"])
def inscription():
    base = sqlite3.connect("data/database.sqlite3",timeout=10)
    cursor = base.cursor()
    
    # ! Modifier dans un scripts d'init
    cursor.execute("""CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    admin INTEGER,
    user VARCHAR(64),
    email VARCHAR(64),
    password VARCHAR(64),
    dt DATETIME DEFAULT CURRENT_TIMESTAMP)""")
    

    if request.method == "POST":

        #todo whith ... 
        user = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        
        password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()


        if not user or not email or not password:
            return "400 erreur - tous les champs sont requis", 400

        cursor.execute("INSERT INTO Users (admin, user,email,password) VALUES (0,?,?,?);",(user,email,password_hash))
        base.commit()

        return redirect(url_for('connection'))  # redirige vers la page de login
    
    # GET request => show the form
    base.close()
    return render_template("inscription.html")


@app.route("/login", methods=["GET", "POST"])
def connection():
    return render_template("connection.html")
