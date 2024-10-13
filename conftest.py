from os import getenv
from pytest import fixture

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import close_all_sessions, sessionmaker, scoped_session

from core.settings import FileSettings


def clear_data(session):
    session.execute(text("DELETE FROM study_record"))
    session.commit()


def clear_files():
    file_settings = FileSettings()
    dir = file_settings.user_file_dir()
    for i in dir.glob("**/*"):
        if not i.is_file():
            continue
        i.unlink()


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
    clear_files()

    # sql_app/main.py の get_db() を差し替える
    # https://fastapi.tiangolo.com/advanced/testing-dependencies/
    def get_db_for_testing():
        try:
            yield db
            db.commit()
        except SQLAlchemyError as e:
            assert e is not None
            db.rollback()

    app.dependency_overrides["get_db"] = get_db_for_testing

    # テストケース実行
    yield db

    # 後処理
    db.rollback()
    close_all_sessions()
    engine.dispose()


@fixture
def client(session):
    from fastapi.testclient import TestClient

    from main import app

    yield TestClient(app)
