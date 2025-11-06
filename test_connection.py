# test_db_connection.py
from db.base import engine
from sqlalchemy import text

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("✅ Database connection successful!", result.scalar())
except Exception as e:
    print("❌ Database connection failed:", e)
