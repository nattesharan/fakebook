from flask_socketio import join_room,rooms,leave_room,emit
from flask import request
from fakebook.models import FakeBookUser
from utils import get_id_from_rooms, get_active_user_ids
from api.utils import get_all_online_friends
def connect():
    join_room('main')
    print "Successfully connected"

def disconnect():
    user_rooms = rooms()
    for user_room in user_rooms:
        leave_room(user_room)
    user_id = get_id_from_rooms(user_rooms)
    user = FakeBookUser.objects.get(id=user_id)
    user.become_offline()
    active_users = get_active_user_ids()
    online_friends = get_all_online_friends(user)
    for friend in online_friends:
        emit('refresh_online_friends',room = str(friend.id))
    emit('disconnected_offline',{'users':active_users},room='main')
    

def create_room(data):
    user_id = data['user_id']
    user = FakeBookUser.objects.get(id=user_id)
    user.become_online()
    if user_id not in rooms():
        join_room(data['user_id'])
    active_users = get_active_user_ids()
    online_friends = get_all_online_friends(user)
    for friend in online_friends:
        emit('refresh_online_friends',room = str(friend.id))
    emit('connected_online',{'users':active_users},room='main')
    