from flask import Flask , render_template,request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")    


@app.route("/signup", methods=["GET", "POST"])
def inscription():

    if request.method == "POST":
        # request.form contains the product data dictionnary

        name = request.form.get("name")
        price = request.form.get("price")
        return f"<h1>Product added</h1><p>Name : {name}</p><p>Price : {price}</p>"

    # GET request => show the form
    return render_template("inscription.html")


@app.route("/login", methods=["GET", "POST"])
def connection():
    return render_template("connection.html")
