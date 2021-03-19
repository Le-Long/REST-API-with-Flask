import os
import tempfile

import pytest

from app import app, Base, engine, router
from models.user import UserModel
from models.item import ItemModel


@pytest.fixture
def client():
    """Create database and schema in the application context for testing"""
    # db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
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

    # os.close(db_fd)
    # os.unlink(app.config['DATABASE'])
