from config import Config


class DevelopmentConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:your_password@localhost:3306/kiot"
