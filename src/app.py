from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import  hashlib # importe librairy pour hashage  
import os
import bcrypt
import re

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
    user VARCHAR(32),
    email VARCHAR(320),
    password VARCHAR(64),
    salt VARCHAR(64),
    dt DATETIME DEFAULT CURRENT_TIMESTAMP)""")
    
    if request.method == "POST":
        #todo whith ... 
        user = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt) 
        # encryptage du password et ajoute d'une chaine de caracter pour rendre les Rainbow table null.
        
        if not user or not email or not password:
            return "400 erreur - tous les champs sont requis", 400

        user_regexs = r'[A-Za-z0-9_-]{6,32}'
        if not re.fullmatch(user_regexs,user):
            return "400 erreur - user invalide", 400

        email_regex = r'^([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}){0,320}$'
        if not re.fullmatch(email_regex,email): 
            return "400 erreur - email invalide", 400

        if len(password)<6: #todo verifer le format du mot de pass regex
            return "400 erreur - password invalide", 400

        cursor.execute("SELECT * FROM Users user=? or email=?",(user,))
        if(cursor.fetchone()):
            return "400 erreur - inscription invalide", 400

        cursor.execute("INSERT INTO Users (admin, user, email, password, salt) VALUES (?, ?, ?, ?, ?);",(0, user, email, hashed_password.decode(), salt.decode()))
        base.commit()
        return redirect(url_for('connection'))  # redirige vers la page de login

    base.close()
    return render_template("inscription.html")




@app.route("/login", methods=["GET", "POST"])
def connection():
    return render_template("connection.html")
