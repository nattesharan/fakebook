from flask import Flask,session,redirect,render_template
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_mongoengine import MongoEngine
from fakebook.models import FakeBookUser
from settings import MONGODB_SETTINGS
import main_sockets
app = Flask(__name__)
app.secret_key = 'FAKEBOOKSECRET'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MONGODB_SETTINGS'] = MONGODB_SETTINGS
app.config['WTF_CSRF_SECRET_KEY']="SECRETCSRFKEY"
CORS(app)
socketio = SocketIO(manage_session=False)
socketio.init_app(app)
login_manager = LoginManager(app)
db = MongoEngine(app)
socketio.on_event('connect',main_sockets.connect)
socketio.on_event('create_room',main_sockets.create_room)
socketio.on_event('disconnect',main_sockets.disconnect)

def notify_user(notification):
    print notification
    socketio.emit('received_friend_request',notification,room=notification['user_to_notify'])
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
    from api.api import api_blueprint
    app.register_blueprint(api_blueprint)
load_blueprints()