from flask_restful import Resource
from flask import request,jsonify
from flask_login import login_required,current_user
from app.settings import NOTIFICATION_TYPES
from fakebook.models import FakeBookUser,FakebookNotification
from utils import create_notification, get_notifications_for_dashboard, get_all_notifications
from app import notify_user
class FriendRequestHandler(Resource):
    @login_required
    def post(self):
        data = request.get_json()
        user = FakeBookUser.objects.get(id=data['person_id'])
        sending_user = FakeBookUser.objects.get(id=current_user.id)
        if sending_user not in user.received_friend_requests and sending_user not in user.sent_friend_requests \
            and user not in sending_user.received_friend_requests and user not in sending_user.sent_friend_requests:
            user.received_friend_requests.append(current_user.id)
            sending_user.sent_friend_requests.append(user.id)
            user.save()
            sending_user.save()
            notification = create_notification(NOTIFICATION_TYPES['FRIENDLY'],user)
            notify_user(str(user.id))
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
                'message': 'Request to connect already in progress'
            })

class DashboardNotificationsHandler(Resource):
    @login_required
    def get(self):
        notifications = get_notifications_for_dashboard(current_user.id)
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

class UserNotificationsHandler(Resource):
    @login_required
    def get(self):
        limit = request.args.get('limit')
        skip = request.args.get('skip')
        notifications = get_all_notifications(int(skip),int(limit))
        return jsonify({
            'notifications': notifications
        })

class FriendsHandler(Resource):
    @login_required
    def get(self):
        people = FakeBookUser.objects.filter(id__ne=current_user.id)
        people = [person.json for person in people]
        return jsonify({
            'friends': people
        })