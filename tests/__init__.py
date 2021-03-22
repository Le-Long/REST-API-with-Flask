import pytest

from app import app, Base, engine, router
from models.user import UserModel
from models.item import ItemModel


@pytest.fixture
def client():
    """Create a database in the application context for testing"""
    router()

    with app.test_client() as client:
        with app.app_context():
            Base.metadata.create_all(engine)
            ItemModel.clear_db()
            UserModel.clear_db()
            if UserModel.find_by_username("admin") is None:
                admin = UserModel("admin", "12345")
                admin.save_to_db()
        yield client
