from flask import Blueprint,render_template,request,flash,redirect,url_for
from forms import LoginForm,RegistrationForm
from flask_login import login_user,logout_user,login_required
from fakebook.models import FakeBookUser
auth_views = Blueprint('auth_views',__name__,template_folder='templates')

@auth_views.route('/')
def fakebook_index():
    return render_template("fakebook.html",loginform=LoginForm(), registrationform=RegistrationForm())

@auth_views.route('/login',methods=['POST'])
def login():
    form = LoginForm(request.form)
    if form.validate():
        user = FakeBookUser.objects.get(email=form.loginemail.data)
        if user and user.verify_password(form.loginpassword.data):
            login_user(user,remember=True)
            return redirect(url_for('fakebook_views.home'))
        form.loginemail.errors.append("Email or password invalid")
    return render_template("fakebook.html", loginform=form,registrationform=RegistrationForm())

@auth_views.route('/register',methods=['POST'])
def register():
    form = RegistrationForm(request.form)
    if form.validate():
        if FakeBookUser.find_user(form.email.data):
            form.email.errors.append("Email address already registered")
            return render_template('fakebook.html',loginform=LoginForm(), registrationform=form)
        else:
            user = FakeBookUser(email=form.email.data)
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.set_password(form.password.data)
            user.save()
            flash('Successfully registered','success')
            return redirect(url_for('auth_views.fakebook_index'))
    return render_template("fakebook.html", loginform=LoginForm(),registrationform=form)

@auth_views.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_views.fakebook_index'))