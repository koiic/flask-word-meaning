from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import app

migrate = Migrate(app)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	manager.run()

