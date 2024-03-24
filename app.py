from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
db = SQLAlchemy(app)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    status = db.Column(db.String(20))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        status = request.form["status"]
        new_order = Order(name=name, description=description, status=status)
        db.session.add(new_order)
        db.session.commit()
        return redirect(url_for("index"))  # Перенаправляем пользователя на главную страницу после создания заказа

    orders = Order.query.all()
    return render_template("index.html", orders=orders)

@app.route("/delete_all_orders", methods=["POST"])
def delete_all_orders():
    Order.query.delete()  # Удаляем все заказы из базы данных
    db.session.commit()
    return redirect(url_for("index"))  # Перенаправляем пользователя на главную страницу после удаления всех заказов

@app.route("/update_order/<int:order_id>", methods=["POST"])
def update_order(order_id):
    new_status = request.form["new_status"]
    order = Order.query.get(order_id)
    if order:
        order.status = new_status
        db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete_order/<int:order_id>", methods=["POST"])
def delete_order(order_id):
    order = Order.query.get(order_id)
    if order:
        db.session.delete(order)
        db.session.commit()
    return redirect(url_for("index"))

@app.route("/active_orders")
def active_orders():
    active_orders = Order.query.all()
    return render_template("active_orders.html", active_orders=active_orders)

if __name__ == "__main__":
    app.run(debug=True)
