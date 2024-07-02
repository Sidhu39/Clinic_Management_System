from flask import Blueprint, render_template, flash, redirect, url_for
from app import db
from app.forms import AppointmentForm
from app.models import User, Appointment
from flask_login import current_user, login_required

bp = Blueprint('appointment', __name__)

@bp.route('/')
@bp.route('/book_appointment', methods=['GET', 'POST'])
@login_required
def book_appointment():
    form = AppointmentForm()

    # Get list of doctors to populate the doctor_name field choices
    form.doctor.choices = [(doctor.username, doctor.username) for doctor in User.query.filter_by(role='doctor').all()]

    if form.validate_on_submit():
        appointment = Appointment(
            patient_name=form.patient_name.data,
            doctor_name=form.doctor.data,
            appointment_time=form.time.data,
            reason=form.reason.data,
            user_id=form.patient_id.data
        )
        db.session.add(appointment)
        db.session.commit()
        flash('Appointment booked successfully!')
        return redirect(url_for('routes.index'))

    return render_template('appointment.html', title='Book Appointment', form=form)
