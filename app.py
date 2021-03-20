from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


app = Flask(__name__)


def router():
    from controllers.user import user_page
    from controllers.item import item_page

    app.register_blueprint(item_page)
    app.register_blueprint(user_page)


if app.config["ENV"] == "prod":
    app.config.from_object("config.production.ProductionConfig")
elif app.config["ENV"] == "test":
    app.config.from_object("config.testing.TestingConfig")
else:
    app.config.from_object("config.development.DevelopmentConfig")

engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
Session = sessionmaker(bind=engine)
Base = declarative_base()


@app.before_first_request
def create_db():
    """ Create database first """
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    router()
    app.run(port=5000)
