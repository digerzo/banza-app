import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite://"
SQLALCHEMY_DATABASE_URL = "sqlite:///./app-prod.db"
# MYSQL_DATABASE = "mysql://root:admin@localhost:3306/test"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

url = os.getenv("SQLALCHEMY_DATABASE_URL")
if url:
    # estoy corriendo en docker
    engine = create_engine(url)
else:
    # estoy corriendo local
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
        #MYSQL_DATABASE
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
