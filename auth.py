import functools
import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from aws import get_login_info



bp = Blueprint('auth', __name__, url_prefix='/auth')
    
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        
        login_info = get_login_info()
        expected_username = login_info['username']
        expected_password = login_info['password']

        if username is None:
            error = 'Incorrect username.'
        elif not username == expected_username:
            error = 'Access denied.'
        elif not password == expected_password:
            error = 'Access denied.'

        if error is None:
            session.clear()
            session['user_id'] = expected_username
            return redirect(url_for('sleep.index'))

        flash(error)

    return render_template('auth/login.html')
    
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = user_id
        

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
    
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
