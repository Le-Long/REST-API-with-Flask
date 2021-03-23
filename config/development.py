from config import Config


class DevelopmentConfig(Config):
    """Configuration in development environment
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:your_password@localhost:3306/kiot"
