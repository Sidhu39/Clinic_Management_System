from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

bp = Blueprint('pharmacist', __name__)

@bp.route('/')
@bp.route('/pharmacist')
@login_required
def pharmacist_dashboard():
    if current_user.role != 'pharmacist':
        return redirect(url_for('routes.index'))
    return render_template('pharmacist/dashboard.html', title='Pharmacist Dashboard')
