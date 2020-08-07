import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a78d2066beb0d180'
    RECAPTCHA_PUBLIC_KEY = os.environ.get('SECRET_KEY') or '6LfBzbsZAAAAAN7UX684Cn18Grq7PSoiWBtJ52_j'
    RECAPTCHA_PRIVATE_KEY = os.environ.get('SECRET_KEY') or '6LfBzbsZAAAAAA0phBnPKdepwhpA4ev6CRPBo2wv'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    CHIA_MAIL_SUBJECT_PREFIX = '[CHIA]'
    CHIA_MAIL_SENDER = 'CHIA Admin <chia@chia.com>'
    CHIA_ADMIN = os.environ.get('CHIA_ADMIN')
    SSL_REDIRECT = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    CHIA_POSTS_PER_PAGE = 20
    CHIA_FOLLOWERS_PER_PAGE = 50
    CHIA_COMMENTS_PER_PAGE = 30
    CHIA_SLOW_DB_QUERY_TIME = 0.5

    # PRESERVE_CONTEXT_ON_EXCEPTION = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # FLASK_ENV = os.environ.get('FLASK_ENV') or 'development'
    # FLASK_ENV = 'development' or os.environ.get('FLASK_ENV')
    ENV = 'development'
    DATABASE_HOST = '192.168.6.6'
    DATABASE_PORT = '32778'
    DATABASE = os.environ.get('FLASK_DATABASE')
    USERNAME = os.environ.get('FLASK_DATABASE_USERNAME')
    PASSWORD = os.environ.get('FLASK_DATABASE_PASSWORD')
    DB_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(username=USERNAME,
                                                                                            password=PASSWORD,
                                                                                            host=DATABASE_HOST,
                                                                                            port=DATABASE_PORT,
                                                                                            db=DATABASE)
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or DB_URI


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite://'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # email errors to the administrators
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.CHIA_MAIL_SENDER,
            toaddrs=[cls.CHIA_ADMIN],
            subject=cls.CHIA_MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
