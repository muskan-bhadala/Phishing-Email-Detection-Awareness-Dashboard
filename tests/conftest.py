import tempfile, os, pytest
from app import create_app

@pytest.fixture()
def app():
    db = tempfile.NamedTemporaryFile(delete=False)
    db.close()
    app = create_app({"TESTING": True, "DATABASE": db.name, "SECRET_KEY": "test"})
    yield app
    os.unlink(db.name)

@pytest.fixture()
def client(app):
    return app.test_client()
