import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import set_route
from init_app import app, db

app.config.from_object(os.environ['APP_SETTINGS'])
app, db = set_route(app, db)
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()