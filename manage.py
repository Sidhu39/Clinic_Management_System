from app import create_app
from app.models import Appointment, Queue

app = create_app()
with app.app_context():
    appointments = Appointment.query.all()
    queues = Queue.query.all()
    print(appointments)
    print(queues)

    print(app.url_map)

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)

# Add the 'db' command to the manager
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

