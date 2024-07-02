from flask import Blueprint
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for

bp = Blueprint('nurse', __name__)

@bp.route('/')
@bp.route('/nurse')
@login_required
def nurse_dashboard():
    if current_user.role != 'nurse':
        return redirect(url_for('routes.index'))
    return render_template('nurse/dashboard.html', title='Nurse Dashboard')
