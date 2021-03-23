from config import Config


class TestingConfig(Config):
    """Configuration in testing environment
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:your_password@localhost:3306/kiot"
