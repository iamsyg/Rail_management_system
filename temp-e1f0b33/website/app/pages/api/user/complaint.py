import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..')))

from fastapi import APIRouter, HTTPException, Depends, status, BackgroundTasks, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, validator, field_validator, model_validator
from typing import Optional, List
import traceback
import threading

# importing ml pipeline 
from utils.classifier import classify_user_complaints

from .models import Complaint, StatusEnum, User
from .dependencies import get_db
from .auth import  verify_token

# Define router
complaint_router = APIRouter()

# Pydantic models for request validation
class ComplaintCreate(BaseModel):
    trainNumber: str
    pnrNumber: str
    coachNumber: str
    seatNumber: str
    sourceStation: str
    destinationStation: str
    complaint: str
    
    @field_validator('trainNumber')
    def validate_train_number(cls, v):
        if not v.isdigit():
            raise ValueError("Train number must be numeric")
        return v.strip()
    
    @field_validator('pnrNumber')
    def validate_pnr_number(cls, v):
        v = v.strip()
        if not v.isdigit() or len(v) != 10:
            raise ValueError("PNR must be a 10-digit number")
        return v
    
    @field_validator('seatNumber')
    def validate_seat_number(cls, v):
        if not v.isdigit():
            raise ValueError("Seat number must be numeric")
        return v.strip()
    
    @field_validator('complaint')
    def validate_complaint(cls, v):
        v = v.strip()
        if len(v) < 20:
            raise ValueError("Complaint description must be at least 20 characters")
        return v
    
    @model_validator(mode='after')
    def validate_stations(cls, model):
        if model.sourceStation.strip() == model.destinationStation.strip():
            raise ValueError("Source and destination stations cannot be the same")
        return model

    class Config:
        anystr_strip_whitespace = True

class ComplaintUpdate(BaseModel):
    status: Optional[str] = None
    resolution: Optional[str] = None

# Define valid statuses (using enum values from model)
VALID_STATUSES = {"pending", "inProgress", "resolved"}

# Background task for classification
def classify_in_background(user_id: str):
    try:
        print(f"Starting background classification for user {user_id}")
        # Note: If classify_user_complaints is async, you'll need to handle it differently
        # For now, assuming it can work synchronously or you have a sync version
        import asyncio
        asyncio.run(classify_user_complaints(user_id))
        print(f"Completed background classification for user {user_id}")
    except Exception as e:
        print(f"Error in background classification for user {user_id}: {e}")
        traceback.print_exc()

@complaint_router.post('/', status_code=201)
async def create_complaint(
    request: Request,
    complaint: ComplaintCreate, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    try:
        token = request.cookies.get("access_token_cookie")

        if not token:
            raise HTTPException(status_code=401, detail="Missing access token")
        
        token_data, payload  = verify_token(token)

        if not token_data:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        current_user = payload
        
        # Create new complaint using SQLAlchemy model
        new_complaint = Complaint(
            user_id=current_user.get("sub"),
            trainNumber=complaint.trainNumber,
            pnrNumber=complaint.pnrNumber,
            coachNumber=complaint.coachNumber,
            seatNumber=complaint.seatNumber,
            sourceStation=complaint.sourceStation,
            destinationStation=complaint.destinationStation,
            complaint=complaint.complaint,
            status=StatusEnum.pending  # Use enum from model
        )
        
        # Save complaint using model method
        new_complaint.save(db)
        
        # Schedule the classification in the background
        background_tasks.add_task(classify_in_background, current_user.get("sub"))

        return {
            "message": "Complaint created successfully",
            "complaint": {
                "id": new_complaint.id,
                "trainNumber": new_complaint.trainNumber,
                "pnrNumber": new_complaint.pnrNumber,
                "coachNumber": new_complaint.coachNumber,
                "seatNumber": new_complaint.seatNumber,
                "sourceStation": new_complaint.sourceStation,
                "destinationStation": new_complaint.destinationStation,
                "complaint": new_complaint.complaint,
                "status": new_complaint.status.value,
                "createdAt": new_complaint.created_at.isoformat()
            }
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

@complaint_router.get("/get-complaints")
async def get_complaints(
    request: Request,
    db: Session = Depends(get_db)
):
    try:
        # Query complaints for current user
        token = request.cookies.get("access_token_cookie")
        print(f"Token received: {token}")
        token_data, payload  = verify_token(token)
        current_user = token_data
        print(f"Current user: {current_user}")
        complaints = db.query(Complaint).filter(
            Complaint.user_id == current_user.user_id
        ).order_by(Complaint.created_at.desc()).all()

        complaints_list = [
            {
                "id": c.id,
                "trainNumber": c.trainNumber,
                "pnrNumber": c.pnrNumber,
                "coachNumber": c.coachNumber,
                "seatNumber": c.seatNumber,
                "sourceStation": c.sourceStation,
                "destinationStation": c.destinationStation,
                "complaint": c.complaint,
                "status": c.status.value,
                "classification": c.classification,
                "sentiment": c.sentiment,
                "sentimentScore": c.sentimentScore,
                "createdAt": c.created_at.isoformat()
            } for c in complaints
        ]

        return {
            "success": True,
            "message": "Complaints fetched successfully",
            "totalComplaints": len(complaints),
            "complaints": complaints_list
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@complaint_router.get("/get-all-complaints")
async def get_all_complaints(
    
    db: Session = Depends(get_db)
):
    try:
        # Admin can see all complaints
        complaints = db.query(Complaint).order_by(Complaint.created_at.desc()).all()

        if not complaints:
            raise HTTPException(status_code=404, detail="No complaints found")

        complaints_list = [
            {
                "id": c.id,
                "trainNumber": c.trainNumber,
                "pnrNumber": c.pnrNumber,
                "coachNumber": c.coachNumber,
                "seatNumber": c.seatNumber,
                "sourceStation": c.sourceStation,
                "destinationStation": c.destinationStation,
                "complaint": c.complaint,
                "status": c.status.value,
                "createdAt": c.created_at.isoformat(),
                "classification": c.classification,
                "sentiment": c.sentiment,
                "sentimentScore": c.sentimentScore,
                "resolution": c.resolution,
            } for c in complaints
        ]

        return {
            "success": True,
            "message": "Complaints fetched successfully",
            "totalComplaints": len(complaints),
            "complaints": complaints_list
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error fetching complaints {e}")

@complaint_router.put("/update/{complaint_id}")
async def update_complaint_status(
    complaint_id: str, 
    update_data: ComplaintUpdate,
    
    db: Session = Depends(get_db)
):
    try:
        # Find the complaint
        complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
        
        if not complaint:
            raise HTTPException(status_code=404, detail="Complaint not found")

        # Validate and update status if provided
        if update_data.status:
            if update_data.status not in VALID_STATUSES:
                raise HTTPException(status_code=400, detail="Invalid status")
            
            # Map string status to enum
            status_mapping = {
                "pending": StatusEnum.pending,
                "inProgress": StatusEnum.inProgress,
                "resolved": StatusEnum.resolved
            }
            complaint.status = status_mapping[update_data.status]
        
        # Update resolution if provided
        if update_data.resolution is not None:
            complaint.resolution = update_data.resolution
        
        # Save changes
        db.commit()
        db.refresh(complaint)

        return {
            "message": "Complaint updated successfully",
            "complaint": {
                "id": complaint.id,
                "trainNumber": complaint.trainNumber,
                "pnrNumber": complaint.pnrNumber,
                "coachNumber": complaint.coachNumber,
                "seatNumber": complaint.seatNumber,
                "sourceStation": complaint.sourceStation,
                "destinationStation": complaint.destinationStation,
                "complaint": complaint.complaint,
                "status": complaint.status.value,
                "resolution": complaint.resolution,
                "createdAt": complaint.created_at.isoformat()
            }
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

# Add a manual endpoint to trigger classification for debugging
@complaint_router.post("/trigger-classification")
async def trigger_classification(
    request: Request,
):
    try:
        token = request.cookies.get("access_token_cookie")
        token_data, payload = verify_token(token)
        current_user = token_data
        # Run classification in a separate thread to avoid blocking
        thread = threading.Thread(target=classify_in_background, args=(current_user.user_id,))
        thread.start()
        
        return {"message": "Classification triggered successfully"}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))