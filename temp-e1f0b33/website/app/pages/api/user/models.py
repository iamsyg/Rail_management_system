from sqlalchemy import Column, String, Float, Enum, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
from jose import jwt
import enum
from datetime import datetime, timedelta
import os
from .database import Base
from .config import load_dotenv
load_dotenv()

# Base = declarative_base()

# JWT Configuration
JWT_SECRET_KEY = os.environ.get("FLASK_JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=2)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)

if not JWT_SECRET_KEY:
    raise ValueError("Missing FLASK_JWT_SECRET_KEY in environment variables")

class RoleEnum(enum.Enum):
    user = "user"
    admin = "admin"

class User(Base):
    __tablename__ = "user"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phoneNumber = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.user)
    refresh_token = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    complaints = relationship('Complaint', back_populates='user', lazy='dynamic')

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name}, email={self.email})"
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def generate_access_token(self):
        payload = {
            "sub": self.id,
            "name": self.name,
            "email": self.email,
            "phone_number": self.phoneNumber,
            "role": self.role.value,
            "exp": datetime.utcnow() + JWT_ACCESS_TOKEN_EXPIRES,
            "type": "access"
        }
        return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    
    def generate_refresh_token(self):
        payload = {
            "sub": self.id,
            "name": self.name,
            "email": self.email,
            "phone_number": self.phoneNumber,
            "role": self.role.value,
            "exp": datetime.utcnow() + JWT_REFRESH_TOKEN_EXPIRES,
            "type": "refresh"
        }
        return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    @classmethod
    def get_user_by_email(cls, email: str, db: Session):
        return db.query(cls).filter(cls.email == email).first()

    def save(self, db: Session):
        db.add(self)
        db.commit()
        db.refresh(self)

    def delete(self, db: Session):
        db.delete(self)
        db.commit()

class StatusEnum(enum.Enum):
    resolved = "Resolved"
    inProgress = "In Progress"
    pending = "Pending"

class Complaint(Base):
    __tablename__ = "complaint"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, ForeignKey('user.id'), nullable=False)
    trainNumber = Column(String, nullable=False)
    pnrNumber = Column(String, nullable=False)
    coachNumber = Column(String, nullable=False)
    seatNumber = Column(String, nullable=False)
    sourceStation = Column(String, nullable=False)
    destinationStation = Column(String, nullable=False)
    complaint = Column(String, nullable=False)
    classification = Column(String, nullable=True)
    sentiment = Column(String, nullable=True)
    sentimentScore = Column(Float, nullable=True)
    status = Column(Enum(StatusEnum), nullable=False, default=StatusEnum.pending)
    resolution = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="complaints")

    def __repr__(self) -> str:
        return f"Complaint(id={self.id}, PNR={self.pnrNumber}, complaint={self.complaint})"

    def save(self, db: Session):
        try:
            db.add(self)
            db.commit()
            db.refresh(self)
        except Exception as e:
            db.rollback()
            raise e

    def delete(self, db: Session):
        try:
            db.delete(self)
            db.commit()
        except Exception as e:
            db.rollback()
            raise e