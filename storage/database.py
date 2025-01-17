from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from configuration.connection import POSTGRESDB

POSTGRESDB = POSTGRESDB()
SQLALCHEMY_DATABASE_URL = "postgresql://"+ POSTGRESDB.USERNAME1 +":"+ POSTGRESDB.PASSWORD +"@"+ POSTGRESDB.HOST +"/" + POSTGRESDB.SCHEMA

engine = create_engine(SQLALCHEMY_DATABASE_URL,pool_size=50, max_overflow=100, pool_recycle = 600  # 10 minutes
                       )

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

print(f"Connected DB Cred:{SQLALCHEMY_DATABASE_URL}")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()