from flask import request, jsonify, Blueprint
from app.models.member import Member
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    # Simulate admin credentials check
    member = Member.query.filter_by(email=email).first()

    if member and member.role == 'admin' and password == "deuces12345":  # Replace with real password check
        access_token = create_access_token(identity={"id": member.id, "role": member.role})
        return jsonify(access_token=access_token), 200

    return jsonify({"error": "Invalid credentials or admin access required"}), 401
