#importing os
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..')))

from flask import Blueprint, jsonify, request
from .models import Complaint, StatusEnum, db
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

# importing ml pipeline 
from utils.classifier import classify_user_complaints
import threading

complaint_bp = Blueprint('complaint', __name__)

@complaint_bp.route('/', methods=['POST'])
@jwt_required()
def createComplaint():
    try:
        current_user = get_jwt_identity()
        claims = get_jwt()

        data = request.get_json()
        user_id = current_user
        trainNumber = str(data.get('trainNumber', '')).strip()
        pnrNumber = str(data.get('pnrNumber', '')).strip()
        coachNumber = str(data.get('coachNumber', '')).strip()
        seatNumber = str(data.get('seatNumber', '')).strip()
        sourceStation = str(data.get('sourceStation', '')).strip()
        destinationStation = str(data.get('destinationStation', '')).strip()
        complaint = str(data.get('complaint', '')).strip()

        # Validate all required fields are present
        if not all([trainNumber, pnrNumber, coachNumber, seatNumber, sourceStation, destinationStation, complaint]):
            missing_fields = []
            if not trainNumber: missing_fields.append("trainNumber")
            if not pnrNumber: missing_fields.append("pnrNumber")
            if not coachNumber: missing_fields.append("coachNumber")
            if not seatNumber: missing_fields.append("seatNumber")
            if not sourceStation: missing_fields.append("sourceStation")
            if not destinationStation: missing_fields.append("destinationStation")
            if not complaint: missing_fields.append("complaint")
            
            return jsonify({"error": "Missing required fields", "fields": missing_fields}), 400

        # Additional validations
        if not trainNumber.isdigit():
            return jsonify({"error": "Train number must be numeric"}), 400
            
        if not pnrNumber.isdigit() or len(pnrNumber) != 10:
            return jsonify({"error": "PNR must be a 10-digit number"}), 400
            
        if not seatNumber.isdigit():
            return jsonify({"error": "Seat number must be numeric"}), 400
            
        if sourceStation == destinationStation:
            return jsonify({"error": "Source and destination stations cannot be the same"}), 400
            
        if len(complaint) < 20:
            return jsonify({"error": "Complaint description must be at least 20 characters"}), 400
        
        # Create the new complaint
        new_complaint = Complaint(
            user_id=user_id,
            trainNumber=trainNumber,
            pnrNumber=pnrNumber,
            coachNumber=coachNumber,
            seatNumber=seatNumber,
            sourceStation=sourceStation,
            destinationStation=destinationStation,
            complaint=complaint
        )
        
        # Save to database
        db.session.add(new_complaint)
        db.session.commit()
        
         # Classify only this user's complaints in a background thread
        threading.Thread(target=classify_user_complaints, args=(user_id,)).start()

        return jsonify(
            {
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
            }), 201

    except Exception as e:
        db.session.rollback()  # Rollback transaction on error
        return jsonify({"error": str(e)}), 400



@complaint_bp.route("/get-complaints", methods=["GET"])
@jwt_required()
def getComplaints():
    try:
        current_user = get_jwt_identity()

        # Get all complaints for the current user
        complaints = Complaint.query.filter_by(user_id=current_user).order_by(Complaint.created_at.desc()).all()

        if not complaints:
            return jsonify({"success": True, "complaints": []}), 200

        # Serialize the complaints
        complaints_list = [
            {
                "id": complaint.id,
                "trainNumber": complaint.trainNumber,
                "pnrNumber": complaint.pnrNumber,
                "coachNumber": complaint.coachNumber,
                "seatNumber": complaint.seatNumber,
                "sourceStation": complaint.sourceStation,
                "destinationStation": complaint.destinationStation,
                "complaint": complaint.complaint,
                "status": complaint.status.value,
                "createdAt": complaint.created_at.isoformat()
            } for complaint in complaints
        ]

        return jsonify(
            {
                "success": True,
                "message": "Complaints fetched successfully",
                "totalComplaints": len(complaints),
                "complaints": complaints_list
            }), 200

    except Exception as e:
        print(f"[ERROR] Fetching user complaints: {str(e)}")
        return jsonify({"success": False, "message": "An error occurred while fetching complaints"}), 500


@complaint_bp.route("/get-all-complaints", methods=["GET"])
@jwt_required()
def getAllComplaints():
    try:

        current_user = get_jwt_identity()

        if get_jwt()["role"] != "admin":
            return jsonify({"success": False, "message": "Unauthorized access"}), 403
        
        complaints = Complaint.query.order_by(Complaint.created_at.desc()).all()

        if not complaints:
            return jsonify({"success": True, "complaints": []}), 200

        # Serialize the complaints
        complaints_list = [
            {
                "id": complaint.id,
                "trainNumber": complaint.trainNumber,
                "pnrNumber": complaint.pnrNumber,
                "coachNumber": complaint.coachNumber,
                "seatNumber": complaint.seatNumber,
                "sourceStation": complaint.sourceStation,
                "destinationStation": complaint.destinationStation,
                "complaint": complaint.complaint,
                "status": complaint.status.value,
                "createdAt": complaint.created_at.isoformat(),
                "classification": complaint.classification,
                "sentiment": complaint.sentiment,
                "sentimentScore": complaint.sentimentScore,
                "resolution": complaint.resolution
            } for complaint in complaints
        ]

        return jsonify(
            {
                "success": True,
                "message": "Complaints fetched successfully",
                "totalComplaints": len(complaints),
                "complaints": complaints_list
            }), 200

    except Exception as e:
        print(f"[ERROR] Fetching all complaints: {str(e)}")
        return jsonify({"success": False, "message": "An error occurred while fetching complaints"}), 500



@complaint_bp.route("/update/<complaint_id>", methods=["PUT"])
@jwt_required()
def updateComplaintStatus(complaint_id):
    try:

        print("complaint_id", complaint_id)
        # Get the complaint to update
        complaint = Complaint.query.get(complaint_id)

        if not complaint:
            return jsonify({"error": "Complaint not found"}), 404
        
        if get_jwt()["role"] != "admin":
            return jsonify({"success": False, "message": "Unauthorized access"}), 403

        # Update the status and resolution
        data = request.get_json()
        status = data.get("status")
        resolution = data.get("resolution")
        print("resolution", resolution)
        print("status", status)

        if status:
            if status not in [status.value for status in StatusEnum]:
                return jsonify({"error": "Invalid status"}), 400
            complaint.status = StatusEnum(status)

        if resolution:
            complaint.resolution = resolution

        db.session.commit()

        return jsonify({
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
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400