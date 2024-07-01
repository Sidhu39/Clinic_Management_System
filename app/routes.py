from flask import render_template, redirect, url_for, flash
from app import db
from app.models import Queue, Prescription, User, Appointment, Billing
from app.forms import LoginForm, RegistrationForm, AppointmentForm, BillingForm, PrescriptionForm
from flask_login import current_user, login_user, logout_user, login_required

#from flask import Blueprint



#bp = Blueprint('routes', __name__)


#@bp.route('/')
#@bp.route('/index')
#@login_required
#def index():
#    return render_template('index.html', title='Home')

#@bp.route('/login', methods=['GET', 'POST'])
#def login():
#    if current_user.is_authenticated:
#        return redirect(url_for('routes.index'))
#    form = LoginForm()
#    if form.validate_on_submit():
#        user = User.query.filter_by(username=form.username.data).first()
#        if user is None or not user.check_password(form.password.data):
#            flash('Invalid username or password')
#            return redirect(url_for('routes.login'))
#        login_user(user, remember=form.remember_me.data)
#        return redirect(url_for('routes.index'))
#    return render_template('login.html', title='Sign In', form=form)

'''
@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('routes.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        print("User added",form.username.data)
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('routes.login'))
    return render_template('register.html', title='Register', form=form)


@bp.route('/book_appointment', methods=['GET', 'POST'])
@login_required
def book_appointment():
    form = AppointmentForm()
    if form.validate_on_submit():
        appointment = Appointment(
            patient_id=current_user.id,
            date=form.date.data,
            time=form.time.data,
            doctor_id=form.doctor.data,
            reason=form.reason.data,
            patient_name=form.patient_name.data,
            patient_weight=form.patient_weight.data,
            patient_blood_group=form.patient_blood_group.data,
            patient_height=form.patient_height.data
        )
        db.session.add(appointment)
        db.session.commit()
        queue = Queue(appointment_id=appointment.id, position=Queue.query.count() + 1)
        db.session.add(queue)
        db.session.commit()
        flash('Appointment booked successfully!', 'success')
        return redirect(url_for('main.index'))
    return render_template('appointment.html', title='Book Appointment', form=form)

@bp.route('/queue')
@login_required
def view_queue():
    if current_user.role != 'doctor':
        return redirect(url_for('main.index'))
    queue = Queue.query.join(Appointment).order_by(Queue.position).all()
    return render_template('view_queue.html', title='View Queue', queue=queue)

@bp.route('/prescription/<int:appointment_id>', methods=['GET', 'POST'])
@login_required
def prescribe_medications(appointment_id):
    if current_user.role != 'doctor':
        return redirect(url_for('main.index'))
    appointment = Appointment.query.get_or_404(appointment_id)
    form = PrescriptionForm()
    if form.validate_on_submit():
        prescription = Prescription(
            appointment_id=appointment_id,
            medications=form.medications.data,
            follow_up=form.follow_up.data
        )
        db.session.add(prescription)
        db.session.commit()
        flash('Prescription submitted successfully!', 'success')
        return redirect(url_for('main.view_queue'))
    return render_template('prescribe_medications.html', title='Prescribe Medications', form=form, appointment=appointment)

@bp.route('/billing/<int:appointment_id>', methods=['GET', 'POST'])
@login_required
def generate_bill(appointment_id):
    if current_user.role != 'doctor':
        return redirect(url_for('main.index'))
    appointment = Appointment.query.get_or_404(appointment_id)
    prescription = Prescription.query.filter_by(appointment_id=appointment_id).first()
    form = BillingForm()
    if form.validate_on_submit():
        bill = Billing(
            appointment_id=appointment_id,
            amount=form.amount.data,
            status='Unpaid'
        )
        db.session.add(bill)
        db.session.commit()
        flash('Bill generated successfully!', 'success')
        return redirect(url_for('main.index'))
    return render_template('generate_bill.html', title='Generate Bill', form=form, appointment=appointment, prescription=prescription)
'''