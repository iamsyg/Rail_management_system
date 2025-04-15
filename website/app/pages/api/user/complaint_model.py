from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import uuid4
from models import db
import enum
from sqlalchemy import Enum, Float

db = SQLAlchemy()

class StatusEnum(enum.Enum):
    complaintsNotProcesed = "complaintsNotProcesed"
    complaintsProcesed = "complaintsProcesed"
    complaintsClosed = "complaintsClosed"

class Complaint(db.Model):

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))

    user_id: Mapped[str] = mapped_column(db.ForeignKey('user.id'), nullable=False)

    trainNumber: Mapped[str] = mapped_column(nullable=False)

    pnrNumber: Mapped[str] = mapped_column(nullable=False, unique=True)

    coachNumber: Mapped[str] = mapped_column(nullable=False)

    seatNumber: Mapped[str] = mapped_column(nullable=False, unique=True)

    sourceStation: Mapped[str] = mapped_column(nullable=False)

    destinationStation: Mapped[str] = mapped_column(nullable=False)

    complaint: Mapped[str] = mapped_column(nullable=False)

    classification: Mapped[str] = mapped_column(nullable=True)

    sentiment: Mapped[str] = mapped_column(nullable=True)

    sentimentScore: Mapped[float] = mapped_column(Float,  nullable=True)

    status: Mapped[StatusEnum] = mapped_column(Enum(StatusEnum), nullable=False, default=StatusEnum.complaintsNotProcesed) 

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