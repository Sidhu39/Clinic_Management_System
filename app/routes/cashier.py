from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

bp = Blueprint('cashier', __name__)

@bp.route('/')
@bp.route('/cashier')
@login_required
def cashier_dashboard():
    if current_user.role != 'cashier':
        return redirect(url_for('routes.index'))
    return render_template('cashier/dashboard.html', title='Cashier Dashboard')
