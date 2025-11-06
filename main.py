import models
from api import api_router
from db import base, session
from fastapi import FastAPI

base.Base.metadata.create_all(bind=session.engine)
app = FastAPI(title="Glen Backend API")
app.include_router(api_router, prefix="/api/v1")
