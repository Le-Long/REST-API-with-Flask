from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from app import Base, Session

session = Session()


class ItemModel(Base):
    """ Interface for the items database"""

    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    price = Column(Float)
    category_id = Column(Integer, ForeignKey('categories.id'))
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))

    category = relationship('CategoryModel')
    user = relationship('UserModel')

    def __init__(self, name, price, category, user):
        self.name = name
        self.price = price
        self.category_id = category
        self.user_id = user

    @classmethod
    def find_by_name(cls, name):
        return session.query(cls).filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id):
        return session.query(cls).get(_id)

    @classmethod
    def clear_db(cls):
        for item in session.query(cls).all():
            session.delete(item)
        session.commit()

    @classmethod
    def query_with_part_of_name(cls, name):
        return session.query(cls).filter(cls.name.contains(name))

    @classmethod
    def pagination(cls, name, perpage, page):
        query = cls.query_with_part_of_name(name)
        start = (page - 1) * perpage  # start is the index of the first object of a page
        if query.count() < start:
            start = 0  # if start is out of range, we set it to 0
        return query.slice(start, page*perpage).all()

    def save_to_db(self):
        session.add(self)
        session.commit()

    def update_to_db(self, name, price, category):
        self.name = name
        self.price = price
        self.category_id = category
        session.commit()

    def delete_from_db(self):
        session.delete(self)
        session.commit()


class CategoryModel(Base):
    """ Interface for the categories database"""

    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(80))

    items = relationship('ItemModel')

    def __init__(self, name):
        self.name = name

    @classmethod
    def find_by_name(cls, name):
        return session.query(cls).filter_by(name=name).first()

    def save_to_db(self):
        session.add(self)
        session.commit()

