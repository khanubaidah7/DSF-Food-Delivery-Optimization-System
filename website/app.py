from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/restaurants')
def restaurants():
    return render_template('restaurants.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route("/order")
def order_page():
    return render_template("order.html")

@app.route("/cart")
def cart():
    cursor.execute("SELECT * FROM orders ORDER BY id DESC")
    orders = cursor.fetchall()
    return render_template("cart.html", orders=orders)

if __name__ == "__main__":
    app.run(debug=True)