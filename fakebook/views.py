from flask import Blueprint, render_template
from flask_login import login_required,current_user
from fakebook.models import FakeBookUser
fakebook_views = Blueprint('fakebook_views',__name__,template_folder='templates')

@fakebook_views.route('/dashboard')
@login_required
def home():
    return render_template('dashboard.html',user=current_user)

@fakebook_views.route('/profile')
@login_required
def profile():
    return render_template('user_profile.html',user=current_user)

@fakebook_views.route('/tables')
@login_required
def tables():
    return render_template('tables.html',user=current_user)

@fakebook_views.route('/notifications')
@login_required
def typography():
    return render_template('typography.html',user=current_user)

@fakebook_views.route('/find-friends')
@login_required
def icons():
    return render_template('find_friends.html', user=current_user)

@fakebook_views.route('/maps')
@login_required
def maps():
    return render_template('maps.html',user=current_user)

@fakebook_views.route('/sample-notifications')
@login_required
def notifications():
    return render_template('notifications.html',user=current_user)

