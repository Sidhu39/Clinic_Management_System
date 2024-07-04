from flask import Blueprint, render_template, flash, redirect, url_for
from app import db
from app.forms import AppointmentForm
from app.models import User, Appointment, Queue
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
            patient_id=form.patient_id.data,
            date=form.date.data,
            time=form.time.data,
            doctor_id=form.doctor.id,
            doctor_name=form.doctor.data,
            reason=form.reason.data,
            patient_name=form.patient_name.data,
            patient_weight=form.patient_weight.data,
            patient_blood_group=form.patient_blood_group.data,
            patient_height=form.patient_height.data,
        )
        db.session.add(appointment)
        db.session.commit()
        queue = Queue(appointment_id=appointment.id, position=Queue.query.count() + 1)
        db.session.add(queue)
        db.session.commit()
        flash('Appointment booked successfully!', 'success')
        return redirect(url_for('routes.view_queue'))

    return render_template('appointment.html', title='Book Appointment', form=form)
