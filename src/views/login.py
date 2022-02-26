from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from src import db
from src.models.user import User
from src.forms.login import LoginForm

login = Blueprint('login', __name__)

@login.route('/login', methods=['GET','POST'])
def login_user():
    if session.get('username'):
        return redirect(url_for('home.index'))

    form = LoginForm()
    if form.validate_on_submit():
        email       = form.email.data
        password    = form.password.data

        user = db.session.query(User).filter(User.username == email).first()
        user_exist = user is not None

        if user_exist and user.password == password:
            flash(f'{user.first_name}, you are successfully logged in!')
            session['user_id'] = email
            session['username'] = user.first_name
            return redirect(url_for('home.index'))
        else:
            flash('Sorry, something went wrong.','danger')
    return render_template('login.html', title='Login', form=form, login=True )