from flask_restful import Resource
from flask import request,jsonify
from flask_login import login_required,current_user
from app.settings import NOTIFICATION_TYPES
from fakebook.models import FakeBookUser
from utils import create_and_send_notification
class FriendRequestHandler(Resource):
    @login_required
    def post(self):
        data = request.get_json()
        user = FakeBookUser.objects.get(id=data['person_id'])
        if current_user not in user.pending_friends:
            user.pending_friends.append(current_user)
            user.save()
            create_and_send_notification(NOTIFICATION_TYPES['FRIENDLY'],user)
            return jsonify({
                'success': True,
                'message': 'Friend Request Sent to {}'.format(user.name)
            })
        elif current_user in user.friends:
            return jsonify({
                'success': False,
                'message': 'Already Friends'
            })
        else:
            return jsonify({
                'status': False,
                'message': 'Request Already Sent'
            })
