
import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import URL, create_engine

# Load environment variables from .env
load_dotenv()
if not os.getenv("DB_PASSWORD"):
    raise ValueError("DB_PASSWORD is missing from .env")

db_url = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password=os.getenv("DB_PASSWORD"),
    host="localhost",
    port=5432,
    database="telusko",
)

engine = create_engine(db_url)

session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
