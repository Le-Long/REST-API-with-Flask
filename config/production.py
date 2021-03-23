from config import Config


class ProductionConfig(Config):
    """
    Configuration in production environment
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:your_password@localhost:3306/kiot"
