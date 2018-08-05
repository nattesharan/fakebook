from flask import Blueprint,render_template
from forms import LoginForm,RegistrationForm
auth_views = Blueprint('auth_views',__name__,template_folder='templates')

@auth_views.route('/')
def fakebook_index():
    return render_template("fakebook.html",loginform=LoginForm(), registrationform=RegistrationForm())