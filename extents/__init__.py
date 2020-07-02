from flask_sqlalchemy import SQLAlchemy

# python app.py runserver db init 初始化
# python app.py runserver db migrate 迁移
# python app.py runserver db upgrade 同步
db = SQLAlchemy()
