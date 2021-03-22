from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app import Base, Session

session = Session()


class UserModel(Base):
    """ Interface for the users database"""

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True)
    password = Column(String(20))

    item = relationship('ItemModel')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        session.add(self)
        session.commit()

    @classmethod
    def clear_db(cls):
        for user in session.query(cls).all():
            session.delete(user)
        session.commit()

    @classmethod
    def find_by_username(cls, username):
        return session.query(cls).filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return session.query(cls).get(_id)
