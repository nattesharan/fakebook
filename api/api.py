from flask import Blueprint
from flask_restful import Api
from resources import FriendRequestHandler,DashboardNotificationsHandler
api_blueprint = Blueprint('api',__name__)
api = Api(api_blueprint)

api.add_resource(FriendRequestHandler,'/api/friend-request')
api.add_resource(DashboardNotificationsHandler,'/api/notifications')