from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_refresh_token, create_access_token
import enum
from sqlalchemy import Enum, Float

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from datetime import datetime

db = SQLAlchemy()
jwt = JWTManager()

class RoleEnum(enum.Enum):
    user = "user"
    admin = "admin"

class User(db.Model):
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    phoneNumber: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum), nullable=False, default=RoleEnum.user)
    refresh_token = mapped_column(db.String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default = datetime.utcnow)

    complaints = relationship('Complaint', back_populates='user', lazy='dynamic')

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name}, email={self.email})"
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def generate_access_token(self):
        return create_access_token(
            identity=self.id,  # Primary identity is a string
            additional_claims={  # Additional data as claims
                "name": self.name,
                "email": self.email,
                "phone_number": self.phoneNumber,
                "role": self.role.value
        })
    
    def generate_refresh_token(self):
        return create_refresh_token(
            identity=self.id,  # Primary identity is a string
            additional_claims={  # Additional data as claims
                "name": self.name,
                "email": self.email,
                "phone_number": self.phoneNumber,
                "role": self.role.value
            }
        )

    @classmethod
    def get_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()





class StatusEnum(enum.Enum):
    resolved = "Resolved"
    inProgress = "In Progress"
    pending = "Pending"

class Complaint(db.Model):

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))

    user_id: Mapped[str] = mapped_column(db.ForeignKey('user.id'), nullable=False)

    trainNumber: Mapped[str] = mapped_column(nullable=False)

    pnrNumber: Mapped[str] = mapped_column(nullable=False)

    coachNumber: Mapped[str] = mapped_column(nullable=False)

    seatNumber: Mapped[str] = mapped_column(nullable=False)

    sourceStation: Mapped[str] = mapped_column(nullable=False)

    destinationStation: Mapped[str] = mapped_column(nullable=False)

    complaint: Mapped[str] = mapped_column(nullable=False)

    classification: Mapped[str] = mapped_column(nullable=True)

    sentiment: Mapped[str] = mapped_column(nullable=True)

    sentimentScore: Mapped[float] = mapped_column(Float,  nullable=True)

    status: Mapped[StatusEnum] = mapped_column(Enum(StatusEnum), nullable=False, default=StatusEnum.pending)

    resolution: Mapped[str] = mapped_column(nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(default = datetime.utcnow)

    user = relationship("User", back_populates="complaints")

    def __repr__(self) -> str:
        return f"Complaint(id={self.id}, PNR={self.pnrNumber}, complaint={self.complaint})"

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e