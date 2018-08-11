from flask_socketio import join_room,rooms,leave_room,emit
from flask import request
from flask_login import current_user
from fakebook.models import FakeBookUser, FakeBookChat, FakeBookMessages
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

def send_message(data):
    sender_rooms = rooms()
    sender_id = get_id_from_rooms(sender_rooms)
    receiver = FakeBookUser.objects.get(id=data['sent_to'])
    sender = FakeBookUser.objects.get(id=sender_id)
    chat = FakeBookChat.get_or_create_chat(sender,receiver)
    message = FakeBookMessages.new_message(data['message'],sender,receiver)
    chat.messages.insert(0,message)
    chat.save()
    if receiver.is_online:
        emit('new_message',room=str(receiver.id))
    emit('refresh_sender',room=str(sender.id))

def typing_message(data):
    friend = FakeBookUser.objects.get(id=data['friend'])
    if friend.is_online:
        emit('sender_is_typing',room=str(friend.id))

def no_longer_typing(data):
    friend = FakeBookUser.objects.get(id=data['friend'])
    if friend.is_online:
        emit('sender_stopped_typing',room=str(friend.id))