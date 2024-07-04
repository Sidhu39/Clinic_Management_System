from flask import Blueprint, render_template, redirect, url_for, flash, request
from sqlalchemy.exc import SQLAlchemyError

#from app.routes import bp
from app import db
from app.forms import LoginForm, RegistrationForm, AppointmentForm, PrescriptionForm, BillingForm
from app.models import  Queue, Prescription, User, Appointment, Billing
from flask_login import current_user, login_user, logout_user, login_required

bp = Blueprint('routes', __name__)


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('routes.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('routes.index'))
    return render_template('login.html', title='Sign In', form=form)
    pass

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('routes.index'))

#@bp.route('/register', methods=['GET', 'POST'])
#def register():
#    if current_user.is_authenticated:
#        return redirect(url_for('routes.index'))
#    form = RegistrationForm()
#    if form.validate_on_submit():
#        user = User(username=form.username.data, email=form.email.data, role=form.role.data)
#        user.set_password(form.password.data)
#        db.session.add(user)
#        db.session.commit()
#        flash('Congratulations, you are now a registered user!')
#        return redirect(url_for('routes.login'))
#    return render_template('register.html', title='Register', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, role=form.role.data)
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
            patient_id=form.patient_id.data,
            date=form.date.data,
            time=form.time.data,
            doctor_id=form.doctor.data,
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
        return redirect(url_for('routes.index'))
    return render_template('appointment.html', title='Book Appointment', form=form)

@bp.route('/queue')
@login_required
def view_queue():
    waiting_queue = db.session.query(Queue).join(Appointment).filter(Queue.status == 'waiting').order_by(Queue.position).all()
    billing_queue = db.session.query(Queue).join(Appointment).filter(Queue.status == 'billing').order_by(Queue.position).all()
    return render_template('view_queue.html', waiting_queue=waiting_queue, billing_queue=billing_queue)

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

@bp.route('/billing/<int:queue_id>', methods=['GET', 'POST'])
@login_required
def billing(queue_id):
    queue = Queue.query.get_or_404(queue_id)
    appointment = queue.appointment
    if request.method == 'POST':
        amount = request.form['amount']
        billing = Billing(appointment_id=appointment.id, amount=amount, status='paid')
        queue.status = 'completed'
        db.session.add(billing)
        db.session.commit()
        db.session.delete(queue)
        db.session.commit()
        return redirect(url_for('routes.view_queue'))
    return render_template('billing.html', appointment=appointment)

@bp.route('/select_queue/<int:queue_id>', methods=['POST'])
@login_required
def select_queue(queue_id):
    queue = Queue.query.get(queue_id)
    if queue:
        if queue.status == 'waiting' and current_user.role == 'doctor':
            queue.status = 'completed'
        elif queue.status == 'billing' and current_user.role == 'cashier':
            queue.status = 'paid'
        db.session.commit()
    return redirect(url_for('routes.view_queue'))

@bp.route('/appointment/<int:appointment_id>', methods=['GET', 'POST'])
@login_required
def appointment_details(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    if request.method == 'POST':
        appointment.prescription = request.form['prescription']
        queue = Queue.query.filter_by(appointment_id=appointment.id).first()
        queue.status = 'completed'
        existing_billing_item = Queue.query.filter_by(
            appointment_id=queue.appointment.id,
            status='billing'
        ).first()

        # Only add to billing queue if not already present
        if not existing_billing_item:
            new_queue_item = Queue(
                appointment_id=queue.appointment.id,
                position=Queue.query.filter_by(status='billing').count() + 1,
                status='billing'
            )
            db.session.add(new_queue_item)

        db.session.commit()
        return redirect(url_for('routes.view_queue'))
    return render_template('appointment_details.html', appointment=appointment)


