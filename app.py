from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "fasteat_secret_key"

# DB CONNECTION
db = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="Thisismysql.123",
    database="Food_Delivery"
)

cursor = db.cursor(dictionary=True)

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")

# ---------------- AUTH PAGE ----------------
@app.route("/auth")
def auth():
    return render_template("auth.html")

# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["POST"])
def signup():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    cursor.execute(
        "INSERT INTO users (name, email, password) VALUES (%s,%s,%s)",
        (name, email, password)
    )
    db.commit()

    return redirect(url_for("auth"))

# ---------------- LOGIN ----------------
@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    cursor.execute(
        "SELECT * FROM users WHERE email=%s AND password=%s",
        (email, password)
    )
    user = cursor.fetchone()

    if user:
        session["user_id"] = user["id"]
        session["user_name"] = user["name"]
        return redirect(url_for("home"))

    return "Invalid login"

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# ---------------- RESTAURANTS ----------------
@app.route("/restaurants")
def restaurants():
    return render_template("restaurants.html")

# ---------------- ABOUT ----------------
@app.route("/about")
def about():
    return render_template("about.html")

# ---------------- CONTACT ----------------
@app.route("/contact")
def contact():
    return render_template("contact.html")

# ---------------- ORDER PAGE ----------------
@app.route("/order")
def order_page():
    return render_template("order.html")

# ---------------- PLACE ORDER ----------------
@app.route("/place_order", methods=["POST"])
def place_order():

    if not session.get("user_id"):
        return redirect(url_for("auth"))

    item = request.form.get("item")
    price = int(request.form.get("price"))
    restaurant = request.form.get("restaurant")
    quantity = int(request.form.get("quantity"))
    total = price * quantity

    user_id = session.get("user_id")

    cursor.execute("""
        INSERT INTO orders (item_name, price, restaurant, quantity, total_price, user_id)
        VALUES (%s,%s,%s,%s,%s,%s)
    """, (item, price, restaurant, quantity, total, user_id))

    db.commit()

    return redirect(url_for("cart"))

# ---------------- CART ----------------
@app.route("/cart")
def cart():

    if not session.get("user_id"):
        return redirect(url_for("auth"))

    cursor.execute(
        "SELECT * FROM orders WHERE user_id=%s ORDER BY id DESC",
        (session["user_id"],)
    )
    orders = cursor.fetchall()

    # ✅ TOTAL CALCULATION (CORRECT)
    total_amount = sum(
        (order["total_price"] if order["total_price"] else order["price"] * order["quantity"])
        for order in orders
    )

    return render_template("cart.html", orders=orders, total_amount=total_amount)

# ---------------- DELETE ORDER ----------------
@app.route("/delete_order/<int:order_id>")
def delete_order(order_id):

    cursor.execute("DELETE FROM orders WHERE id=%s AND user_id=%s",
                   (order_id, session["user_id"]))
    db.commit()

    return redirect(url_for("cart"))

if __name__ == "__main__":
    app.run(debug=True)