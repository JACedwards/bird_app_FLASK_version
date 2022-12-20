from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import User, db
from .authforms import LoginForm, RegistrationForm, ResetRequestForm
from werkzeug.security import check_password_hash
from flask_login import login_user, current_user, login_required, logout_user
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, TimedSerializer


auth = Blueprint('auth', __name__, template_folder='auth_templates', url_prefix='/auth')


@auth.route('/login', methods=['GET','POST'])
def login():
   
    lform = LoginForm()

    if request.method == 'POST':
        if lform.validate_on_submit():
            user = User.query.filter_by(username=lform.username.data).first()
            print(user)
            if user and check_password_hash(user.password, lform.password.data):
                login_user(user)
                print('current user:', current_user.__dict__)
                flash(f'Success -- You have been signed in, {user.username}.', category = 'success')
                return redirect(url_for('home'))

        flash(f'Incorrect username or password.  Please try again.', category = 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('signin.html', form = lform)


@auth.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            newuser = User(form.username.data, form.email.data, form.password.data)
            print(newuser)

            try:
                db.session.add(newuser)
                db.session.commit()
            except:
                flash('Username or email already taken.  Please try a different ones.', category='danger')
                return redirect(url_for('auth.register'))

            login_user(newuser)
            flash(f'Welcome, {newuser.username}! Thank you for signing up!', category = 'info')
            return redirect(url_for('home'))
        else:
            flash("Sorry, your passwords don't match.  Please try again.", category = 'danger')
            return redirect(url_for('auth.register'))

    elif request.method == 'GET':
        return render_template('register.html', form=form)

def send_mail():
    pass

    # <!-- starting to work on reset   **ready to start on email through Itsdangerous
    # (Using this video here; was using another video in routes)
    # https://www.youtube.com/watch?v=zYWpEJAHvaI (currently at minute 12:31 (created template reset-request.html already))-->

@auth.route('/reset_password', methods=['GET','POST'])
def reset_request():
    form=ResetRequestForm()

    if request.method == 'POST':
        print('Post method')
        if form.validate_on_submit():
            user=User.query.filter_by(email=form.email.data).first()
            if user:
                send_mail()

                flash(f'Reset request sent. Please, check your email.', category = 'success')
                return redirect(url_for('auth.login', form=None))
    return render_template('reset_request.html', title='Reset Request', form=form)





@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been signed out.', category = 'info')
    return redirect(url_for('auth.login'))

