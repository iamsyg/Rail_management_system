# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..')))

# from fastapi import APIRouter, Depends, HTTPException, Request, BackgroundTasks
# from fastapi.responses import JSONResponse
# from fastapi_jwt_auth import AuthJWT
# from pydantic import BaseModel, Field, validator
# from typing import Optional, List
# import traceback

# # importing ml pipeline 
# from utils.classifier import classify_user_complaints
# import asyncio

# from database.lib.prisma import get_prisma_client, prisma

# # Define router
# complaint_router = APIRouter()

# # Pydantic models for request validation
# class ComplaintCreate(BaseModel):
#     trainNumber: str
#     pnrNumber: str
#     coachNumber: str
#     seatNumber: str
#     sourceStation: str
#     destinationStation: str
#     complaint: str
    
#     @validator('trainNumber')
#     def validate_train_number(cls, v):
#         v = v.strip()
#         if not v.isdigit():
#             raise ValueError("Train number must be numeric")
#         return v
    
#     @validator('pnrNumber')
#     def validate_pnr_number(cls, v):
#         v = v.strip()
#         if not v.isdigit() or len(v) != 10:
#             raise ValueError("PNR must be a 10-digit number")
#         return v
    
#     @validator('seatNumber')
#     def validate_seat_number(cls, v):
#         v = v.strip()
#         if not v.isdigit():
#             raise ValueError("Seat number must be numeric")
#         return v
    
#     @validator('complaint')
#     def validate_complaint(cls, v):
#         v = v.strip()
#         if len(v) < 20:
#             raise ValueError("Complaint description must be at least 20 characters")
#         return v
    
#     @validator('sourceStation', 'destinationStation')
#     def validate_stations(cls, v, values, **kwargs):
#         v = v.strip()
#         field = kwargs.get('field')
#         if field.name == 'destinationStation' and 'sourceStation' in values:
#             if v == values['sourceStation']:
#                 raise ValueError("Source and destination stations cannot be the same")
#         return v

#     class Config:
#         anystr_strip_whitespace = True

# class ComplaintUpdate(BaseModel):
#     status: Optional[str] = None
#     resolution: Optional[str] = None

# # Define valid statuses
# VALID_STATUSES = {"pending", "inProgress", "resolved"}

# # Background task for classification
# async def classify_in_background(user_id: str):
#     try:
#         print(f"Starting background classification for user {user_id}")
#         await classify_user_complaints(user_id)
#         print(f"Completed background classification for user {user_id}")
#     except Exception as e:
#         print(f"Error in background classification for user {user_id}: {e}")
#         traceback.print_exc()

# @complaint_router.post('/', status_code=201)
# async def create_complaint(complaint: ComplaintCreate, background_tasks: BackgroundTasks, Authorize: AuthJWT = Depends()):
    
#     try:
#         Authorize.jwt_required()
#         current_user = Authorize.get_jwt_subject()
        
#         # Make sure prisma is connected
#         if not prisma.is_connected():
#             await prisma.connect()
        
#         # Save complaint in Prisma
#         new_complaint = await prisma.complaint.create(data={
#             "userId": current_user,
#             "trainNumber": complaint.trainNumber,
#             "pnrNumber": complaint.pnrNumber,
#             "coachNumber": complaint.coachNumber,
#             "seatNumber": complaint.seatNumber,
#             "sourceStation": complaint.sourceStation,
#             "destinationStation": complaint.destinationStation,
#             "complaint": complaint.complaint,
#             "status": "pending"  # default enum value
#         })
        
#         # Schedule the classification in the background
#         background_tasks.add_task(classify_in_background, current_user)

#         return {
#             "message": "Complaint created successfully",
#             "complaint": new_complaint
#         }

#     except Exception as e:
#         traceback.print_exc()
#         raise HTTPException(status_code=400, detail=str(e))

# @complaint_router.get("/get-complaints")
# async def get_complaints(Authorize: AuthJWT = Depends()):
#     try:
#         Authorize.jwt_required()
#         user_id = Authorize.get_jwt_subject()

#         # Ensure prisma is connected
#         if not prisma.is_connected():
#             await prisma.connect()
            
#         complaints = await prisma.complaint.find_many(
#             where={
#                 "userId": user_id
#             },
#             include={
#                 "user": True
#             }
#         )

#         complaints = sorted(complaints, key=lambda c: c.createdAt, reverse=True)

#         complaints_list = [
#             {
#                 "id": c.id,
#                 "trainNumber": c.trainNumber,
#                 "pnrNumber": c.pnrNumber,
#                 "coachNumber": c.coachNumber,
#                 "seatNumber": c.seatNumber,
#                 "sourceStation": c.sourceStation,
#                 "destinationStation": c.destinationStation,
#                 "complaint": c.complaint,
#                 "status": c.status,
#                 "classification": c.classification,
#                 "sentiment": c.sentiment,
#                 "sentimentScore": c.sentimentScore,
#                 "createdAt": c.createdAt.isoformat()
#             } for c in complaints
#         ]

#         return {
#             "success": True,
#             "message": "Complaints fetched successfully",
#             "totalComplaints": len(complaints),
#             "complaints": complaints_list
#         }

#     except Exception as e:
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=str(e))

# @complaint_router.get("/get-all-complaints")
# async def get_all_complaints(Authorize: AuthJWT = Depends()):
#     try:
#         Authorize.jwt_required()
#         claims = Authorize.get_raw_jwt()
        
#         if claims["role"] != "admin":
#             raise HTTPException(status_code=403, detail="Unauthorized access")

#         # Ensure prisma is connected
#         if not prisma.is_connected():
#             await prisma.connect()
            
#         complaints = await prisma.complaint.find_many()

#         complaints = sorted(complaints, key=lambda c: c.createdAt, reverse=True)

#         if not complaints:
#             raise HTTPException(status_code=404, detail="No complaints found")

#         complaints_list = [
#             {
#                 "id": c.id,
#                 "trainNumber": c.trainNumber,
#                 "pnrNumber": c.pnrNumber,
#                 "coachNumber": c.coachNumber,
#                 "seatNumber": c.seatNumber,
#                 "sourceStation": c.sourceStation,
#                 "destinationStation": c.destinationStation,
#                 "complaint": c.complaint,
#                 "status": c.status,
#                 "createdAt": c.createdAt.isoformat(),
#                 "classification": c.classification,
#                 "sentiment": c.sentiment,
#                 "sentimentScore": c.sentimentScore,
#                 "resolution": c.resolution,
#             } for c in complaints
#         ]

#         return {
#             "success": True,
#             "message": "Complaints fetched successfully",
#             "totalComplaints": len(complaints),
#             "complaints": complaints_list
#         }

#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=f"Error fetching complaints {e}")

# @complaint_router.put("/update/{complaint_id}")
# async def update_complaint_status(complaint_id: str, update_data: ComplaintUpdate, Authorize: AuthJWT = Depends()):
#     try:
#         Authorize.jwt_required()
#         claims = Authorize.get_raw_jwt()
        
#         if claims["role"] != "admin":
#             raise HTTPException(status_code=403, detail="Unauthorized access")

#         # Validate status if provided
#         if update_data.status and update_data.status not in VALID_STATUSES:
#             raise HTTPException(status_code=400, detail="Invalid status")

#         # Build update payload dynamically
#         data_dict = update_data.dict(exclude_unset=True, exclude_none=True)
        
#         if not data_dict:
#             raise HTTPException(status_code=400, detail="No update data provided")
        
#         # Ensure prisma is connected
#         if not prisma.is_connected():
#             await prisma.connect()
            
#         # Update the complaint
#         updated_complaint = await prisma.complaint.update(
#             where={"id": complaint_id},
#             data=data_dict
#         )

#         return {
#             "message": "Complaint updated successfully",
#             "complaint": {
#                 "id": updated_complaint.id,
#                 "trainNumber": updated_complaint.trainNumber,
#                 "pnrNumber": updated_complaint.pnrNumber,
#                 "coachNumber": updated_complaint.coachNumber,
#                 "seatNumber": updated_complaint.seatNumber,
#                 "sourceStation": updated_complaint.sourceStation,
#                 "destinationStation": updated_complaint.destinationStation,
#                 "complaint": updated_complaint.complaint,
#                 "status": updated_complaint.status,
#                 "resolution": updated_complaint.resolution,
#                 "createdAt": updated_complaint.createdAt.isoformat()
#             }
#         }

#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         traceback.print_exc()
#         raise HTTPException(status_code=400, detail=str(e))

# # Add a manual endpoint to trigger classification for debugging
# @complaint_router.post("/trigger-classification")
# async def trigger_classification(Authorize: AuthJWT = Depends()):
#     try:
#         Authorize.jwt_required()
#         user_id = Authorize.get_jwt_subject()
        
#         # Run classification directly
#         await classify_user_complaints(user_id)
        
#         return {"message": "Classification triggered successfully"}
#     except Exception as e:
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=str(e))








import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..')))

from fastapi import APIRouter, Depends, HTTPException, Request, BackgroundTasks
from fastapi.responses import JSONResponse
import jwt
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime, timedelta
import traceback

# importing ml pipeline 
from utils.classifier import classify_user_complaints

from database.lib.prisma import get_prisma_client, prisma

# Define router
complaint_router = APIRouter()

# JWT Configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "eternity")
JWT_ALGORITHM = "HS256"

class AuthJWT:
    def __init__(self):
        pass
    
    def jwt_required(self):
        if hasattr(self, '_current_request'):
            token = self._get_token_from_request(self._current_request)
            try:
                self._current_payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            except jwt.ExpiredSignatureError:
                raise HTTPException(status_code=401, detail="Token has expired")
            except jwt.InvalidTokenError:
                raise HTTPException(status_code=401, detail="Invalid token")
    
    def get_jwt_subject(self):
        if hasattr(self, '_current_payload'):
            return self._current_payload.get("sub")
        return None
    
    def get_raw_jwt(self):
        if hasattr(self, '_current_payload'):
            return self._current_payload
        return {}
    
    def _get_token_from_request(self, request: Request):
        token = request.cookies.get("access_token")
        if not token:
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
        if not token:
            raise HTTPException(status_code=401, detail="Token required")
        return token

def get_auth_jwt(request: Request):
    auth_jwt = AuthJWT()
    auth_jwt._current_request = request
    return auth_jwt

# Pydantic models for request validation
class ComplaintCreate(BaseModel):
    trainNumber: str
    pnrNumber: str
    coachNumber: str
    seatNumber: str
    sourceStation: str
    destinationStation: str
    complaint: str
    
    @validator('trainNumber')
    def validate_train_number(cls, v):
        v = v.strip()
        if not v.isdigit():
            raise ValueError("Train number must be numeric")
        return v
    
    @validator('pnrNumber')
    def validate_pnr_number(cls, v):
        v = v.strip()
        if not v.isdigit() or len(v) != 10:
            raise ValueError("PNR must be a 10-digit number")
        return v
    
    @validator('seatNumber')
    def validate_seat_number(cls, v):
        v = v.strip()
        if not v.isdigit():
            raise ValueError("Seat number must be numeric")
        return v
    
    @validator('complaint')
    def validate_complaint(cls, v):
        v = v.strip()
        if len(v) < 20:
            raise ValueError("Complaint description must be at least 20 characters")
        return v
    
    @validator('sourceStation', 'destinationStation')
    def validate_stations(cls, v, values, **kwargs):
        v = v.strip()
        field = kwargs.get('field')
        if field.name == 'destinationStation' and 'sourceStation' in values:
            if v == values['sourceStation']:
                raise ValueError("Source and destination stations cannot be the same")
        return v

    class Config:
        anystr_strip_whitespace = True

class ComplaintUpdate(BaseModel):
    status: Optional[str] = None
    resolution: Optional[str] = None

# Define valid statuses
VALID_STATUSES = {"pending", "inProgress", "resolved"}

# Background task for classification
async def classify_in_background(user_id: str):
    try:
        print(f"Starting background classification for user {user_id}")
        await classify_user_complaints(user_id)
        print(f"Completed background classification for user {user_id}")
    except Exception as e:
        print(f"Error in background classification for user {user_id}: {e}")
        traceback.print_exc()

@complaint_router.post('/', status_code=201)
async def create_complaint(complaint: ComplaintCreate, background_tasks: BackgroundTasks, Authorize: AuthJWT = Depends(get_auth_jwt)):
    
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()
        
        # Make sure prisma is connected
        if not prisma.is_connected():
            await prisma.connect()
        
        # Save complaint in Prisma
        new_complaint = await prisma.complaint.create(data={
            "userId": current_user,
            "trainNumber": complaint.trainNumber,
            "pnrNumber": complaint.pnrNumber,
            "coachNumber": complaint.coachNumber,
            "seatNumber": complaint.seatNumber,
            "sourceStation": complaint.sourceStation,
            "destinationStation": complaint.destinationStation,
            "complaint": complaint.complaint,
            "status": "pending"  # default enum value
        })
        
        # Schedule the classification in the background
        background_tasks.add_task(classify_in_background, current_user)

        return {
            "message": "Complaint created successfully",
            "complaint": new_complaint
        }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

@complaint_router.get("/get-complaints")
async def get_complaints(Authorize: AuthJWT = Depends(get_auth_jwt)):
    try:
        Authorize.jwt_required()
        user_id = Authorize.get_jwt_subject()

        # Ensure prisma is connected
        if not prisma.is_connected():
            await prisma.connect()
            
        complaints = await prisma.complaint.find_many(
            where={
                "userId": user_id
            },
            include={
                "user": True
            }
        )

        complaints = sorted(complaints, key=lambda c: c.createdAt, reverse=True)

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
                "status": c.status,
                "classification": c.classification,
                "sentiment": c.sentiment,
                "sentimentScore": c.sentimentScore,
                "createdAt": c.createdAt.isoformat()
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
async def get_all_complaints(Authorize: AuthJWT = Depends(get_auth_jwt)):
    try:
        Authorize.jwt_required()
        claims = Authorize.get_raw_jwt()
        
        if claims["role"] != "admin":
            raise HTTPException(status_code=403, detail="Unauthorized access")

        # Ensure prisma is connected
        if not prisma.is_connected():
            await prisma.connect()
            
        complaints = await prisma.complaint.find_many()

        complaints = sorted(complaints, key=lambda c: c.createdAt, reverse=True)

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
                "status": c.status,
                "createdAt": c.createdAt.isoformat(),
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
async def update_complaint_status(complaint_id: str, update_data: ComplaintUpdate, Authorize: AuthJWT = Depends(get_auth_jwt)):
    try:
        Authorize.jwt_required()
        claims = Authorize.get_raw_jwt()
        
        if claims["role"] != "admin":
            raise HTTPException(status_code=403, detail="Unauthorized access")

        # Validate status if provided
        if update_data.status and update_data.status not in VALID_STATUSES:
            raise HTTPException(status_code=400, detail="Invalid status")

        # Build update payload dynamically
        data_dict = update_data.dict(exclude_unset=True, exclude_none=True)
        
        if not data_dict:
            raise HTTPException(status_code=400, detail="No update data provided")
        
        # Ensure prisma is connected
        if not prisma.is_connected():
            await prisma.connect()
            
        # Update the complaint
        updated_complaint = await prisma.complaint.update(
            where={"id": complaint_id},
            data=data_dict
        )

        return {
            "message": "Complaint updated successfully",
            "complaint": {
                "id": updated_complaint.id,
                "trainNumber": updated_complaint.trainNumber,
                "pnrNumber": updated_complaint.pnrNumber,
                "coachNumber": updated_complaint.coachNumber,
                "seatNumber": updated_complaint.seatNumber,
                "sourceStation": updated_complaint.sourceStation,
                "destinationStation": updated_complaint.destinationStation,
                "complaint": updated_complaint.complaint,
                "status": updated_complaint.status,
                "resolution": updated_complaint.resolution,
                "createdAt": updated_complaint.createdAt.isoformat()
            }
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

# Add a manual endpoint to trigger classification for debugging
@complaint_router.post("/trigger-classification")
async def trigger_classification(Authorize: AuthJWT = Depends(get_auth_jwt)):
    try:
        Authorize.jwt_required()
        user_id = Authorize.get_jwt_subject()
        
        # Run classification directly
        await classify_user_complaints(user_id)
        
        return {"message": "Classification triggered successfully"}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))