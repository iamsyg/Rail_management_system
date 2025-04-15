from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager
from models import db
from flask_jwt_extended import create_refresh_token, create_access_token
import enum
from sqlalchemy import Enum

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

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

    complaints = relationship('Complaint', back_populates='user')

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