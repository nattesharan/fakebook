from fakebook.models import FakebookNotification
from flask_login import current_user
def create_notification(notif_type,notify_to):
    notification = FakebookNotification(notification_type=notif_type)
    if notif_type == 'FRIEND_REQUEST':
        notification.notification_message = 'Recieved a Friend request from {}'.format(current_user.name)
    notification.user_to_notify = notify_to.id
    notification.initiated_by = current_user.id
    notification.save()
    return notification