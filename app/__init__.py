from flask import Flask
from flask_mongoengine import MongoEngine
from settings import MONGODB_SETTINGS
app = Flask(__name__)
app.secret_key = 'FAKEBOOKSECRET'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MONGODB_SETTINGS'] = MONGODB_SETTINGS
app.config['WTF_CSRF_SECRET_KEY']="SECRETCSRFKEY"
db = MongoEngine(app)
def load_blueprints():
    from auth.views import auth_views
    app.register_blueprint(auth_views)
load_blueprints()