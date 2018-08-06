from flask_socketio import join_room,rooms,leave_room
from flask import request
from fakebook.models import FakeBookUser
def connect():
    print "Successfully connected"

def disconnect():
    user_rooms = rooms()
    for user_room in user_rooms:
        leave_room(user_room)
    user_rooms.remove(request.sid)
    user_id = user_rooms[0]
    user = FakeBookUser.objects.get(id=user_id)
    user.become_offline()
    print "Successfully Disconnected"

def create_room(data):
    user_id = data['user_id']
    user = FakeBookUser.objects.get(id=user_id)
    user.become_online()
    if user_id not in rooms():
        join_room(data['user_id'])