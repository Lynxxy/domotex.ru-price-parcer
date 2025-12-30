from flask import Flask, render_template, redirect
from models import db, Product, Link, PriceLog
from flask import request
from parser.domotex import parse_name


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///prices.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def index():
    items = []

    products = Product.query.all()
    for p in products:
        price_log = (
            PriceLog.query
            .filter_by(product_id=p.id)
            .order_by(PriceLog.price.asc())
            .first()
        )

        min_price = price_log.price if price_log else None
        shop = price_log.shop if price_log else None

        items.append({
            "id": p.id,
            "name": p.name,
            "price": min_price,
            "shop": shop
        })


    items = sorted(
        items,
        key=lambda x: x["price"] if x["price"] is not None else float("inf")
    )

    return render_template("index.html", items=items)




@app.route("/run", methods=["POST"])
def run_parser():

    from parser.run_domotex import run_domotex_parser

    run_domotex_parser()
    return redirect("/")

@app.route("/add", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        url = request.form["url"]

        name = parse_name(url)
        if not name:
            name = "Товар без названия"

        product = Product(name=name)
        db.session.add(product)
        db.session.commit()

        link = Link(
            product_id=product.id,
            url=url,
            shop="domotex.ru"
        )
        db.session.add(link)
        db.session.commit()

        return redirect("/")

    return render_template("add.html")

@app.route("/delete/<int:product_id>", methods=["POST"])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)

    # удаляем историю цен
    PriceLog.query.filter_by(product_id=product_id).delete()

    # удаляем ссылки
    Link.query.filter_by(product_id=product_id).delete()

    # удаляем сам товар
    db.session.delete(product)
    db.session.commit()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
