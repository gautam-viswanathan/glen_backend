from db import base
from db.session import engine


def init_db():
    base.Base.metadata.create_all(bind=engine)
