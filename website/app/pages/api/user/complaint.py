from flask import Blueprint, jsonify, request
from .models import Complaint, StatusEnum, db
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
# from .server import complaint_bp

complaint_bp = Blueprint('complaint', __name__)

@complaint_bp.route('/', methods=['POST'])
@jwt_required()
def createComplaint():

    try:
        current_user = get_jwt_identity()
        claims = get_jwt()

        data = request.get_json()
        user_id = current_user
        trainNumber = data.get('trainNumber').strip()
        pnrNumber = data.get('pnrNumber').strip()
        coachNumber = data.get('coachNumber').strip()
        seatNumber = data.get('seatNumber').strip()
        sourceStation = data.get('sourceStation').strip()
        destinationStation = data.get('destinationStation').strip()
        complaint = data.get('complaint').strip()

        if not all([trainNumber, pnrNumber, coachNumber, seatNumber, sourceStation, destinationStation, complaint]):
            return jsonify({"error": "All fields are required"}), 400

        new_complaint = Complaint(
            user_id=user_id,
            trainNumber=trainNumber,
            pnrNumber=pnrNumber,
            coachNumber=coachNumber,
            seatNumber=seatNumber,
            sourceStation=sourceStation,
            destinationStation=destinationStation,
            complaint=complaint)

        new_complaint.save()

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
                    "status": new_complaint.status.value
                }
            }), 201


    except Exception as e:
        return jsonify({"error": str(e)}), 400