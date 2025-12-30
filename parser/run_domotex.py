import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import app
from models import db, Product, Link, PriceLog
from parser.domotex import parse_price
from logger import logger


def run_domotex_parser():
    with app.app_context():
        links = Link.query.filter_by(shop="domotex.ru").all()

        for link in links:
            price = parse_price(link.url)

            if price is None:
                logger.warning(f"Не удалось получить цену: {link.url}")
                continue

            price_log = PriceLog(
                product_id=link.product_id,
                shop=link.shop,
                price=price
            )

            db.session.add(price_log)
            db.session.commit()

            logger.info(
                f"Цена сохранена | товар_id={link.product_id} | "
                f"магазин={link.shop} | цена={price}"
            )


if __name__ == "__main__":
    run_domotex_parser()
