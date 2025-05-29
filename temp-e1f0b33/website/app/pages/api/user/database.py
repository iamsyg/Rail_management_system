import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from .config import settings

# Get the absolute path of this file
THIS_FILE = os.path.abspath(__file__)

# Calculate the root directory by going up 5 levels from this file (adjust if needed)
# Explanation: database.py is inside website/app/pages/api/user/
# So going up 5 levels should reach rail_management_system root
ROOT_DIR = THIS_FILE
for _ in range(6):
    ROOT_DIR = os.path.dirname(ROOT_DIR)

# Construct path to instance directory in the root
INSTANCE_DIR = os.path.join(ROOT_DIR, "instance")

# Make sure instance directory exists
os.makedirs(INSTANCE_DIR, exist_ok=True)

# SQLite DB path inside instance folder at root
DATABASE_PATH = os.path.join(INSTANCE_DIR, "user.db")

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# engine =create_async_engine(url=settings.DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
