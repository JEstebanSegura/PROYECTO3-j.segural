from flask import Flask
from config.config import Config
from config.db import db
from config.routes import register_routes


app = Flask(__name__, template_folder = "views")
app.config.from_object(Config)
db.init_app(app)
register_routes(app)

if __name__ == "__main__":
    with app.app_context():
      db.create_all()
    app.run(debug=True)