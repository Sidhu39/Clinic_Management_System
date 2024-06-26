from flask import Blueprint, render_template
from flask_login import login_required, current_user

bp = Blueprint('doctor', __name__)

@bp.route('/doctor')
@login_required
def doctor_dashboard():
    if current_user.role != 'doctor':
        return redirect(url_for('routes.index'))
    return render_template('doctor/dashboard.html', title='Doctor Dashboard')
