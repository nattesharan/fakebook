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

def get_notifications_sorted_by_date(user_id):
    return FakebookNotification.objects.filter(user_to_notify=user_id).order_by('-id')

def get_notifications_for_dashboard(user_id):
    notifications = get_notifications_sorted_by_date(user_id)
    return [notification.notif_json for notification in notifications[:5]]

def get_all_notifications(skip,limit):
    notifications = get_notifications_sorted_by_date(current_user.id)
    user_notifications = notifications.skip(skip).limit(limit)
    return [notification.notif_json for notification in user_notifications]