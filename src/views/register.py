from crypt import methods
from flask import Blueprint, flash, redirect, render_template, session, url_for
from src import db
from src.models.user import User
from src.forms.register import RegisterForm

register = Blueprint('register', __name__)

@register.route('/register', methods=['POST','GET'])
def register_user():
    if session.get('username'):
        return redirect(url_for('home.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        email       = form.email.data
        password    = form.password.data
        first_name  = form.first_name.data
        last_name   = form.last_name.data

        user = User(username=email, password=password, first_name=first_name, last_name=last_name)
        db.session.add(user)
        db.session.commit()
        flash('You are successfully registered!','success')
        return redirect(url_for('home.index'))
    return render_template('register.html', title='Register', form=form, register=True)

    
