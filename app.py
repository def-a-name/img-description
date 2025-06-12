from flask import Flask
from config import Config
from db import db
from db.models import user_datastore
from db.ops import get_user_by_uuid
from flask_login import LoginManager
from route import main_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()
    if not user_datastore.find_role('admin'):
        user_datastore.create_role(name='admin')
        db.session.commit()

login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_uuid):
    return get_user_by_uuid(user_uuid)

app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(debug=True)
