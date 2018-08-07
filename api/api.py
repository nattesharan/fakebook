from flask import Blueprint
from flask_restful import Api
from resources import Test
api_blueprint = Blueprint('api',__name__)
api = Api(api_blueprint)

api.add_resource(Test,'/test')