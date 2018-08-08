from flask_restful import Resource
from flask import request,jsonify
from flask_login import login_required,current_user
from app.settings import NOTIFICATION_TYPES
from fakebook.models import FakeBookUser,FakebookNotification
from utils import create_notification
from fakebook.sockets import notify_user
class FriendRequestHandler(Resource):
    @login_required
    def post(self):
        data = request.get_json()
        user = FakeBookUser.objects.get(id=data['person_id'])
        if current_user not in user.pending_friends:
            user.pending_friends.append(current_user.id)
            user.save()
            notification = create_notification(NOTIFICATION_TYPES['FRIENDLY'],user)
            notify_user(notification.json)
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

class DashboardNotificationsHandler(Resource):
    @login_required
    def get(self):
        notifications = FakebookNotification.objects.filter(user_to_notify=current_user.id).order_by('-id')
        notifications = [notification.notif_json for notification in notifications[:5]]
        return jsonify({
            'notifications': notifications
        })
    @login_required
    def put(self):
        notifications = request.get_json()['read_notifications']
        read_notifications = []
        for notification in notifications:
            notif = FakebookNotification.objects.get(id=notification['id'])
            read_notifications.append(notif.mark_as_read())
        return jsonify({
            'notifications': read_notifications
        })