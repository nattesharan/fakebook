from flask import Blueprint, render_template
from flask_login import login_required
fakebook_views = Blueprint('fakebook_views',__name__,template_folder='templates')

@fakebook_views.route('/index')
@login_required
def home():
    return render_template('home.html')