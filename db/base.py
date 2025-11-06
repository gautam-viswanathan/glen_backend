import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base, sessionmaker

# 👇 Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__),"..", ".env")
print(f"Loading .env from: {dotenv_path}")
load_dotenv(dotenv_path)

# 👇 Get DB URL from env
DATABASE_URL = os.getenv("DATABASE_URL")
print(f"Database URL: {DATABASE_URL}")

# Create engine (connect to DB)
engine = create_engine(DATABASE_URL)

# Create session factory
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

