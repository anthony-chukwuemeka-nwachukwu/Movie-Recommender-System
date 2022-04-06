from flask import Blueprint, redirect, url_for

from src import session
from src.param import signed_in

logout = Blueprint('logout', __name__)


@logout.route('/logout')
def logout_user():
    session['user'] = None
    session['user_id'] = None
    session['sign_in_out'] = signed_in
    return redirect(url_for('login.login_user'))
