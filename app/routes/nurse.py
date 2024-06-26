from flask import Blueprint, render_template
from flask_login import login_required, current_user

bp = Blueprint('nurse', __name__)

@bp.route('/nurse')
@login_required
def nurse_dashboard():
    if current_user.role != 'nurse':
        return redirect(url_for('routes.index'))
    return render_template('nurse/dashboard.html', title='Nurse Dashboard')
