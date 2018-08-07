from flask_restful import Resource
from flask_login import login_required
class Test(Resource):
    @login_required
    def get(self):
        return {
            'test': True
        }