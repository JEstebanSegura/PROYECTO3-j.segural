
from flask import Flask,  redirect, url_for
from config.config import Config
from config.db import db
from config.marshmallow import marshmallow
from config.auth import login_manager
from config.routes import register_routes


app = Flask(__name__, template_folder = "views")
app.config.from_object(Config)
db.init_app(app)
marshmallow.init_app(app)
register_routes(app)
login_manager.init_app(app)

@app.route("/")
def home():
    return redirect(url_for("auth.login"))

if __name__ == "__main__":
    with app.app_context():
      db.create_all()
    app.run(debug=True)
