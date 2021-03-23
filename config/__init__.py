class Config(object):
    """Base configuration
    """
    SECRET_KEY = "fds74a"
    JWT_BLACKLIST_ENABLE = True
    PROPAGATE_EXCEPTIONS = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
