from os import getenv
from pytest import fixture

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import close_all_sessions, sessionmaker, scoped_session


def clear_data(session):
    # session.execute(text("DELETE FROM xxx"))
    session.commit()


@fixture
def set_project_test_true(monkeypatch):
    original_value = getenv("PROJECT_TEST", "true")
    monkeypatch.setenv("PROJECT_TEST", "true")
    yield
    monkeypatch.setenv("PROJECT_TEST", original_value)


@fixture
def session(set_project_test_true):
    from core.settings import DBSettings
    from main import app

    db_settings = DBSettings()
    engine = create_engine(db_settings.database_uri)

    TestingSessionLocal = scoped_session(
        sessionmaker(
            bind=engine,
            autocommit=False,
            autoflush=True,
            expire_on_commit=False,
        )
    )

    db = TestingSessionLocal()

    clear_data(db)

    # override get_db() in sql_app/main.py.
    # https://fastapi.tiangolo.com/advanced/testing-dependencies/
    def get_db_for_testing():
        try:
            yield db
            db.commit()
        except SQLAlchemyError as e:
            assert e is not None
            db.rollback()

    app.dependency_overrides["get_db"] = get_db_for_testing

    # execute test.
    yield db

    # post-process.
    db.rollback()
    close_all_sessions()
    engine.dispose()


@fixture
def client(session):
    from fastapi.testclient import TestClient

    from main import app

    yield TestClient(app)
