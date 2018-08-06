from flask import Flask,session,redirect,render_template
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_mongoengine import MongoEngine
from fakebook.models import FakeBookUser
from settings import MONGODB_SETTINGS
app = Flask(__name__)
app.secret_key = 'FAKEBOOKSECRET'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MONGODB_SETTINGS'] = MONGODB_SETTINGS
app.config['WTF_CSRF_SECRET_KEY']="SECRETCSRFKEY"
CORS(app)
socketio = SocketIO(app)
login_manager = LoginManager(app)
db = MongoEngine(app)
@socketio.on('connect')
def connect():
    print "hello"
@login_manager.user_loader
def loaduser(user_id):
    user = FakeBookUser.objects.get(id=user_id)
    return user
@login_manager.unauthorized_handler
def unauthorized():
    session.clear()
    return redirect("/")
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
def load_blueprints():
    from auth.views import auth_views
    app.register_blueprint(auth_views)
    from fakebook.views import fakebook_views
    app.register_blueprint(fakebook_views)
load_blueprints()