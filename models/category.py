from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.exc import SQLAlchemyError

from app import Base, Session

session = Session()


class CategoryModel(Base):
    """Interface for the categories database"""

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)

    items = relationship("ItemModel")

    def __init__(self, name):
        self.name = name

    @classmethod
    def find_by_name(cls, name):
        return session.query(cls).filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id):
        return session.query(cls).get(_id)

    def save_to_db(self):
        try:
            session.add(self)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise e
