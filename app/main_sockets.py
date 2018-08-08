from flask_socketio import join_room,rooms,leave_room,emit
from flask import request
from fakebook.models import FakeBookUser
from utils import get_id_from_rooms, get_active_user_ids
def connect():
    join_room('main')
    print "Successfully connected"

def disconnect():
    user_rooms = rooms()
    for user_room in user_rooms:
        leave_room(user_room)
    user_id = get_id_from_rooms(user_rooms)
    print user_id
    user = FakeBookUser.objects.get(id=user_id)
    user.become_offline()
    active_users = get_active_user_ids()
    emit('disconnected_offline',{'users':active_users},room='main')

def create_room(data):
    user_id = data['user_id']
    user = FakeBookUser.objects.get(id=user_id)
    user.become_online()
    if user_id not in rooms():
        join_room(data['user_id'])
    active_users = get_active_user_ids()
    emit('connected_online',{'users':active_users},room='main')