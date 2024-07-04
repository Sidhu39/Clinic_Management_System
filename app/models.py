"""from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app import db, login
from werkzeug import generate_password_hash, check_password_hash



@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(64), index=True)  # Add a role field

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    doctor = db.Column(db.String(120), nullable=False)
    notes = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    queue_position = db.Column(db.Integer, nullable=True)  # Add this line

    def __repr__(self):
        return f'<Appointment {self.id} - {self.date} {self.time} with {self.doctor}>'


class Billing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Unpaid')

    def __repr__(self):
        return f'<Billing {self.id} - Appointment {self.appointment_id} - {self.amount} - {self.status}>'
    """
import random
import string
# app/models.py

from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from flask_login import UserMixin



def generate_random_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(64))
    appointments = db.relationship('Appointment', backref='patient', lazy='dynamic')
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def get_id(self):
        return str(self.id)
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    appointment_id = db.Column(db.String(64), unique=True, nullable=False, default=generate_random_id)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    doctor_id = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(256))
    patient_name = db.Column(db.String(64))
    doctor_name = db.Column(db.String(64), nullable=False)
    patient_weight = db.Column(db.Float)
    patient_blood_group = db.Column(db.String(8))
    patient_height = db.Column(db.Float)
    status = db.Column(db.String(50), nullable=False, default="waiting")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    prescription = db.Column(db.Text, nullable=True)

class Queue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'))
    position = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(64), nullable=False, default='waiting')
    appointment = db.relationship('Appointment', backref=db.backref('queues', lazy=True))
class Prescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'))
    medications = db.Column(db.Text)
    follow_up = db.Column(db.Boolean, default=False)

class Billing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'))
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Unpaid')
    appointment = db.relationship('Appointment', backref=db.backref('billings', lazy=True))