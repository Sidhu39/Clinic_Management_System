from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

bp = Blueprint('patient', __name__)

@bp.route('/')
@bp.route('/patient')
@login_required
def patient_dashboard():
    if current_user.role != 'patient':
        return redirect(url_for('routes.index'))
    return render_template('patient/dashboard.html', title='Patient Dashboard')
