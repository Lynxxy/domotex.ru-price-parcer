from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///prices.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

import models  

with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return "DB initialized"


if __name__ == "__main__":
    app.run(debug=True)
