from app import socketio
def notify_user(notification):
    socketio.emit('received_friend_request',notification,room=notification['user_to_notify'])