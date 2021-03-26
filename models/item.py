import math

from sqlalchemy import Column, Boolean, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.exc import SQLAlchemyError

from app import Base, Session

session = Session()


class ItemModel(Base):
    """Interface for the items database"""

    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    price = Column(Float, nullable=False)
    not_in_use = Column(Boolean)
    category_id = Column(Integer, ForeignKey("categories.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    category = relationship("CategoryModel")
    user = relationship("UserModel")

    def __init__(self, name, price, category, user_id):
        self.name = name
        self.price = price
        self.category_id = category
        self.user_id = user_id
        self.not_in_use = False

    @classmethod
    def find_by_id(cls, _id):
        item = session.query(cls).get(_id)
        if item:
            if item.not_in_use:
                return None
        return item

    @classmethod
    def clear_db(cls):
        try:
            for item in session.query(cls).filter_by(not_in_use=False).all():
                item.not_in_use = True
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise e

    @classmethod
    def query_with_condition(cls, condition):
        return session.query(cls).filter_by(not_in_use=False).filter(condition)

    @classmethod
    def paginate(cls, query, per_page, page):
        # start is the index of the first object of a page
        start = (page - 1) * per_page
        # end is the index of the first object of the next page (if exists)
        end = page * per_page
        number_of_page = math.ceil(query.count()/per_page)
        if query.count() <= start:
            # if start is out of range, we only get the first page
            return None, 1
        return query.slice(start, end).all(), number_of_page

    def save_to_db(self):
        try:
            session.add(self)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise e

    def update_to_db(self, name, price, category):
        self.name = name
        self.price = price
        self.category_id = category
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise e

    def delete_from_db(self):
        try:
            self.not_in_use = True
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise e
