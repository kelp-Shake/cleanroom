import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from app.main import appy
from app.db import get_session
from app.models import Base

engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestSession = sessionmaker(autocommit = False, autoflush=False, bind = engine)
Base.metadata.create_all(bind=engine)



