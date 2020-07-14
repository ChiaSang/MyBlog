# -*- coding:utf-8 -*-
import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from Apps import create_app
from Apps.user.model import User
from Apps.article.model import *
from extents import db

# ======================================================
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app=app)
migrate = Migrate(app=app, db=db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)


# manager.add_command('db', MigrateCommand)
#
# if __name__ == "__main__":
#     manager.run()


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
