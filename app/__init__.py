# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['SECRET_KEY'] = 'hehe'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.models import User, Appointment

    @login.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes import routes, cashier, nurse, doctor, patient, appointment
    app.register_blueprint(routes.bp, url_prefix='/')
    app.register_blueprint(cashier.bp, url_prefix='/cashier')
    app.register_blueprint(nurse.bp, url_prefix='/nurse')
    app.register_blueprint(doctor.bp, url_prefix='/doctor')
    app.register_blueprint(patient.bp, url_prefix='/patient')
    app.register_blueprint(appointment.bp, url_prefix='/appointment')

    login.login_view = routes.login

    return app
create_app()