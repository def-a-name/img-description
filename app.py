from flask import Flask
from config import Config
import db
from db.models import user_datastore
from route import main_bp

app = Flask(__name__)
app.config.from_object(Config)

db.db.init_app(app)
with app.app_context():
    db.db.create_all()

db.security.init_app(app, user_datastore)

app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(debug=True)
