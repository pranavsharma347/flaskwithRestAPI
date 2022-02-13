from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand

from api.config import db
from app import flaskAppInstance
migrate = Migrate(flaskAppInstance, db)
manager = Manager(flaskAppInstance)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()