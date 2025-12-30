from app import app
from models import db, Product, Link

with app.app_context():
    product = Product(name="Тестовый товар")
    db.session.add(product)
    db.session.commit()

    link = Link(
        product_id=product.id,
        url="https://www.domotex.ru/catalog/umyvalniki/pedestaly_1/sanita_luxe_polupedestal_best_color_sea_morskaya_volna/",
        shop="domotex.ru"
    )
    db.session.add(link)
    db.session.commit()

    print("Товар и ссылка добавлены")
