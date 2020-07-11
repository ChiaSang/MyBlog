# -*- coding:utf-8 -*-
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from Apps import create_app
from Apps.user.model import User
from Apps.article.model import *
from extents import db

app = create_app()
manager = Manager(app=app)
migrate = Migrate(app=app, db=db)
manager.add_command('db', MigrateCommand)

# app.add_template_filter(replace_hello, 'replace')  # 自定义函数


if __name__ == "__main__":
    manager.run()
