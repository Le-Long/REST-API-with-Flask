import os

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


app = Flask(__name__)


def router():
    """ Add URL from blueprints to application """
    from controllers.user import user_page
    from controllers.item import item_page
    from marshmallow import ValidationError
    from sqlalchemy.exc import SQLAlchemyError

    app.register_blueprint(item_page)
    app.register_blueprint(user_page)

    @app.errorhandler(ValidationError)
    def validation_handler(e):
        """Handle validation error"""
        return str(e), 400

    @app.errorhandler(SQLAlchemyError)
    def sqlalchemy_handler(e):
        """Handle sqlalchemy error"""
        return {"msg": "An error occurred in database!"}, 500

    @app.errorhandler(UnboundLocalError)
    def log_handler(e):
        """Handle logging error"""
        return {"msg": "An error occurred in log!"}, 500


app.config["ENV"] = os.environ["ENV"]
# Change environment according to the ENV param
if app.config["ENV"] == "prod":
    app.config.from_object("config.production.ProductionConfig")
elif app.config["ENV"] == "test":
    app.config.from_object("config.testing.TestingConfig")
else:
    app.config.from_object("config.development.DevelopmentConfig")

# Create a session maker connected to database and a base class for all models
engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
Session = sessionmaker(bind=engine)
Base = declarative_base()


@app.before_first_request
def create_db():
    """ Create all tables first """
    Base.metadata.create_all(engine)


if __name__ == "__main__":

    router()
    app.run(port=5000)
