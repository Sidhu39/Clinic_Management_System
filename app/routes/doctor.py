from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

from app.models import Queue, Appointment
from app.routes.routes import prescribe_medications as pl

bp = Blueprint('doctor', __name__)

@bp.route('/')
@bp.route('/doctor')
@login_required
def doctor_dashboard():
    if current_user.role != 'doctor':
        return redirect(url_for('routes.index'))
    queue = Queue.query.join(Appointment).order_by(Queue.position).all()
    appointments = [
        {
            'id': 1,
            'patient_id': 'P001',
            'patient_name': 'John Doe',
            'appointment_time': '10:00 AM',
            'reason': 'Routine Checkup'
        },
        {
            'id': 2,
            'patient_id': 'P002',
            'patient_name': 'Jane Smith',
            'appointment_time': '11:00 AM',
            'reason': 'Flu Symptoms'
        }
    ]
    return render_template('doctor/dashboard.html',doctor_name=current_user.username, appointments=queue)
