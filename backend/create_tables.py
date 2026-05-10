from sqlalchemy import inspect, text

from app.database import Base, engine
from app.models import (
    User,
    PanDetails,
    PlatformData,
    Prediction,
    LenderProfile,
    LoanScheme,
    LoanApplication,
)

print("ENGINE URL:", engine.url)
print("ENGINE DATABASE:", engine.url.database)
print("ENGINE HOST:", engine.url.host)
print("ENGINE PORT:", engine.url.port)
print("REGISTERED TABLES:", list(Base.metadata.tables.keys()))

with engine.connect() as conn:
    print("CONNECTED DATABASE:", conn.execute(text("SELECT current_database();")).scalar())
    print("CONNECTED SCHEMA:", conn.execute(text("SELECT current_schema();")).scalar())
    print("CONNECTED USER:", conn.execute(text("SELECT current_user;")).scalar())

Base.metadata.create_all(bind=engine)

inspector = inspect(engine)
print("INSPECTOR TABLES:", inspector.get_table_names(schema="public"))

with engine.connect() as conn:
    result = conn.execute(text("""
        SELECT table_schema, table_name
        FROM information_schema.tables
        WHERE table_type = 'BASE TABLE'
        ORDER BY table_schema, table_name;
    """)).fetchall()

    print("INFORMATION_SCHEMA TABLES:")
    for row in result:
        print(row)