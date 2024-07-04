import random
import string

from flask_wtf import FlaskForm
from wtforms import IntegerField, FloatField, DateTimeField
from wtforms import DateField,TimeField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('patient', 'Patient'), ('doctor', 'Doctor'), ('nurse', 'Nurse'), ('cashier', 'Cashier')], validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
class QueueForm(FlaskForm):
    queue_position = IntegerField('Queue Position', validators=[DataRequired()])
    submit = SubmitField('Update Queue Position')

def generate_random_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
class AppointmentForm(FlaskForm):
    patient_name = StringField('Patient Name', validators=[DataRequired()])
    patient_id = StringField('Patient ID', validators=[DataRequired()])
    patient_weight = FloatField('Patient Weight', validators=[DataRequired()])
    patient_blood_group = StringField('Patient Blood Group', validators=[DataRequired()])
    patient_height = FloatField('Patient Height', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()])
    doctor = SelectField('Doctor', validators=[DataRequired()], coerce=str)
    reason = StringField('Reason for Appointment')
    submit = SubmitField('Book Appointment')

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.doctor.choices = [(doctor.id, doctor.username) for doctor in User.query.filter_by(role='doctor').all()]

class PrescriptionForm(FlaskForm):
    medications = TextAreaField('Medications', validators=[DataRequired()])
    follow_up = BooleanField('Follow-up Required')
    submit = SubmitField('Submit Prescription')

class BillingForm(FlaskForm):
    amount = FloatField('Amount', validators=[DataRequired()])
    submit = SubmitField('Generate Bill')
