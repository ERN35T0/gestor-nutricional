from app.db.database import test_connection


result = test_connection()

print(f"Database connection result: {result}")
