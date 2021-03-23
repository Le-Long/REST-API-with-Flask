from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash

from app import Base, Session

session = Session()


class UserModel(Base):
    """ Interface for the users database """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True)
    password = Column(String(200))

    item = relationship("ItemModel")

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

    def save_to_db(self):
        try:
            session.add(self)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise e

    @classmethod
    def clear_db(cls):
        for user in session.query(cls).all():
            session.delete(user)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise e

    @classmethod
    def find_by_username(cls, username):
        return session.query(cls).filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return session.query(cls).get(_id)

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)
