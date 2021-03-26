from sqlalchemy import Column, Boolean, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash

from app import Base, Session

session = Session()


class UserModel(Base):
    """Interface for the users database"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(20), nullable=False)
    hashed_password = Column(String(200), nullable=False)
    not_in_use = Column(Boolean)

    item = relationship("ItemModel")

    def __init__(self, username, password):
        self.username = username
        self.hashed_password = generate_password_hash(password)
        self.not_in_use = False

    def save_to_db(self):
        try:
            session.add(self)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise e

    @classmethod
    def clear_db(cls):
        # This method is for tests only
        for user in session.query(cls).all():
            user.not_in_use = True
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise e

    @classmethod
    def find_by_username(cls, username):
        return session.query(cls).filter_by(not_in_use=False, username=username).one_or_none()

    @classmethod
    def find_by_id(cls, _id):
        user = session.query(cls).get(_id)
        if user:
            if user.not_in_use:
                return None
        return user

    def verify_password(self, password):
        return check_password_hash(self.hashed_password, password)
